"""Job storage: SQLite is the source of truth, each job also gets a folder.

- data/farm.db: one row per job (indexed columns + the full job as JSON).
- jobs/<id>/job.json: read-only mirror for humans, rewritten on every save.
- jobs/<id>/inbox/: where the human drops generated images and clips (manual mode).
"""

import os
import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from datetime import datetime
from pathlib import Path

from farm.core.jobs import CHANNEL_ID_RE, JOB_ID_RE, Job, JobStatus, StatusChange, utc_now
from farm.core.paths import project_root

SCHEMA_VERSION = 1

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id         TEXT PRIMARY KEY,
    channel    TEXT NOT NULL,
    series     TEXT,
    status     TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    cost_usd   REAL NOT NULL DEFAULT 0,
    data       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS jobs_channel_status ON jobs (channel, status);
"""


class JobNotFound(LookupError):
    pass


class JobStore:
    def __init__(self, root: Path | None = None):
        self.root = root or project_root()
        self.db_path = self.root / "data" / "farm.db"
        self.jobs_dir = self.root / "jobs"
        self._init_db()

    # --- low level -------------------------------------------------------

    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Connection]:
        """One write transaction, taking the lock up front so id allocation cannot race."""
        with closing(sqlite3.connect(self.db_path, isolation_level=None)) as con:
            con.execute("BEGIN IMMEDIATE")
            try:
                yield con
            except BaseException:
                con.execute("ROLLBACK")
                raise
            con.execute("COMMIT")

    def _init_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.db_path)) as con:
            version = con.execute("PRAGMA user_version").fetchone()[0]
            if version > SCHEMA_VERSION:
                raise RuntimeError(f"{self.db_path} was created by a newer version (schema {version})")
            con.executescript(SCHEMA)
            con.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")

    def _write(self, con: sqlite3.Connection, job: Job) -> None:
        con.execute(
            """INSERT INTO jobs (id, channel, series, status, created_at, updated_at, cost_usd, data)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT (id) DO UPDATE SET
                 series = excluded.series, status = excluded.status, updated_at = excluded.updated_at,
                 cost_usd = excluded.cost_usd, data = excluded.data""",
            (
                job.id, job.channel, job.series, job.status.value,
                job.created_at.isoformat(), job.updated_at.isoformat(),
                job.cost_usd, job.model_dump_json(),
            ),
        )

    def _mirror(self, job: Job) -> None:
        path = self.job_dir(job.id) / "job.json"
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(job.model_dump_json(indent=2), encoding="utf-8")
        os.replace(tmp, path)

    # --- paths -----------------------------------------------------------

    def job_dir(self, job_id: str) -> Path:
        if not JOB_ID_RE.match(job_id):
            raise ValueError(f"invalid job id: {job_id!r}")
        return self.jobs_dir / job_id

    def inbox_dir(self, job_id: str) -> Path:
        return self.job_dir(job_id) / "inbox"

    # --- API -------------------------------------------------------------

    def create(
        self,
        channel: str,
        *,
        series: str | None = None,
        idea: str = "",
        language: str | None = None,
        today: datetime | None = None,
    ) -> Job:
        """Create a job in status `idea`, with id <YYYYMMDD>-<channel>-<NNN> (local date)."""
        if not CHANNEL_ID_RE.match(channel):
            raise ValueError(f"invalid channel id: {channel!r}")
        prefix = f"{(today or datetime.now().astimezone()):%Y%m%d}-{channel}-"
        now = utc_now()
        with self._tx() as con:
            row = con.execute(
                "SELECT max(id) FROM jobs WHERE channel = ? AND substr(id, 1, ?) = ?",
                (channel, len(prefix), prefix),
            ).fetchone()
            seq = int(row[0][-3:]) + 1 if row[0] else 1
            if seq > 999:
                raise RuntimeError(f"more than 999 jobs for {prefix}")
            job = Job(
                id=f"{prefix}{seq:03d}", channel=channel, series=series, idea=idea, language=language,
                created_at=now, updated_at=now,
                history=[StatusChange(at=now, from_status=None, to_status=JobStatus.IDEA, note="created")],
            )
            self._write(con, job)
        self.inbox_dir(job.id).mkdir(parents=True, exist_ok=True)
        self._mirror(job)
        return job

    def get(self, job_id: str) -> Job:
        self.job_dir(job_id)  # validates the id
        with closing(sqlite3.connect(self.db_path)) as con:
            row = con.execute("SELECT data FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if row is None:
            raise JobNotFound(job_id)
        return Job.model_validate_json(row[0])

    def save(self, job: Job) -> None:
        with self._tx() as con:
            if con.execute("SELECT 1 FROM jobs WHERE id = ?", (job.id,)).fetchone() is None:
                raise JobNotFound(job.id)
            self._write(con, job)
        self.job_dir(job.id).mkdir(parents=True, exist_ok=True)
        self._mirror(job)

    def list(
        self, channel: str | None = None, status: JobStatus | str | None = None, limit: int | None = None
    ) -> list[Job]:
        """Most recent first."""
        query, args = "SELECT data FROM jobs WHERE 1=1", []
        if channel:
            query += " AND channel = ?"
            args.append(channel)
        if status:
            query += " AND status = ?"
            args.append(JobStatus(status).value)
        query += " ORDER BY created_at DESC, id DESC"
        if limit:
            query += " LIMIT ?"
            args.append(limit)
        with closing(sqlite3.connect(self.db_path)) as con:
            rows = con.execute(query, args).fetchall()
        return [Job.model_validate_json(r[0]) for r in rows]

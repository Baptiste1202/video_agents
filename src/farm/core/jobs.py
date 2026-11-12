"""Job model: one job = one video, moving through the pipeline statuses (BRIEF §3).

Every agent reads a Job and returns it updated. Status changes go through
`Job.transition` so that the history (who moved what, when, why) is always kept.
"""

import re
from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    IDEA = "idea"
    SCRIPTED = "scripted"
    AWAITING_ASSETS = "awaiting_assets"
    PRODUCED = "produced"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ANALYZED = "analyzed"
    REJECTED = "rejected"
    FAILED = "failed"


S = JobStatus

# Allowed moves. Anything else needs force=True (manual fix by the human).
TRANSITIONS: dict[JobStatus, frozenset[JobStatus]] = {
    S.IDEA: frozenset({S.SCRIPTED, S.REJECTED, S.FAILED}),
    # API providers go straight to `produced`; manual mode waits for the human first.
    S.SCRIPTED: frozenset({S.AWAITING_ASSETS, S.PRODUCED, S.REJECTED, S.FAILED}),
    S.AWAITING_ASSETS: frozenset({S.PRODUCED, S.REJECTED, S.FAILED}),
    S.PRODUCED: frozenset({S.IN_REVIEW, S.FAILED}),
    S.IN_REVIEW: frozenset({S.APPROVED, S.REJECTED}),
    S.APPROVED: frozenset({S.PUBLISHED, S.FAILED}),
    S.PUBLISHED: frozenset({S.ANALYZED}),
    S.ANALYZED: frozenset(),
    # "Redo": restart from scratch, from the script, or only the generation.
    S.REJECTED: frozenset({S.IDEA, S.SCRIPTED, S.AWAITING_ASSETS}),
    # Retry once the cause of the failure is fixed.
    S.FAILED: frozenset({S.IDEA, S.SCRIPTED, S.AWAITING_ASSETS, S.PRODUCED, S.APPROVED}),
}

JOB_ID_RE = re.compile(r"^\d{8}-[a-z0-9_]+-\d{3}$")
CHANNEL_ID_RE = re.compile(r"^[a-z0-9_]+$")


class InvalidTransition(ValueError):
    pass


def utc_now() -> datetime:
    return datetime.now(UTC)


class StatusChange(BaseModel):
    at: datetime
    from_status: JobStatus | None
    to_status: JobStatus
    note: str = ""
    forced: bool = False


class CostEntry(BaseModel):
    at: datetime
    provider: str
    model: str = ""
    usd: float = Field(ge=0)
    note: str = ""


class Post(BaseModel):
    platform: str
    url: str = ""                 # empty when posted by hand without a link yet
    at: datetime


class Job(BaseModel):
    id: str
    channel: str
    series: str | None = None     # recurring format, e.g. "hi_there"
    status: JobStatus = JobStatus.IDEA
    created_at: datetime
    updated_at: datetime

    # Content decisions (filled by the Trends / Scenario / Style agents)
    idea: str = ""
    language: Literal["fr", "en"] | None = None
    outfit_id: str | None = None
    spicy_level: int | None = Field(default=None, ge=0, le=2)
    script: dict = {}             # Scenario agent output; schema fixed when the agent is written
    caption: str = ""
    hashtags: list[str] = []

    # Traceability
    costs: list[CostEntry] = []
    history: list[StatusChange] = []
    posts: list[Post] = []
    metrics: dict = {}            # filled by the Analysis agent

    @property
    def cost_usd(self) -> float:
        return round(sum(c.usd for c in self.costs), 6)

    def can_transition(self, to: JobStatus) -> bool:
        return to in TRANSITIONS[self.status]

    def transition(self, to: JobStatus | str, note: str = "", force: bool = False) -> None:
        to = JobStatus(to)
        if to == self.status:
            raise InvalidTransition(f"job {self.id} is already {to}")
        if not force and not self.can_transition(to):
            allowed = ", ".join(sorted(TRANSITIONS[self.status])) or "none"
            raise InvalidTransition(f"job {self.id}: {self.status} -> {to} not allowed (allowed: {allowed})")
        now = utc_now()
        self.history.append(StatusChange(at=now, from_status=self.status, to_status=to, note=note, forced=force))
        self.status = to
        self.updated_at = now

    def add_cost(self, provider: str, usd: float, model: str = "", note: str = "") -> None:
        self.costs.append(CostEntry(at=utc_now(), provider=provider, model=model, usd=usd, note=note))
        self.updated_at = utc_now()

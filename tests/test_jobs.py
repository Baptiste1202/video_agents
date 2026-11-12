import json
import shutil
from datetime import datetime

import pytest
from typer.testing import CliRunner

from farm.core.jobs import InvalidTransition, JobStatus
from farm.core.paths import project_root
from farm.core.storage import JobNotFound, JobStore

DAY = datetime(2026, 11, 12, 10, 0).astimezone()


@pytest.fixture
def store(tmp_path) -> JobStore:
    return JobStore(root=tmp_path)


def test_create_allocates_sequential_ids_per_channel_and_day(store):
    a = store.create("ai_girl", today=DAY)
    b = store.create("ai_girl", today=DAY)
    c = store.create("rain", today=DAY)
    assert (a.id, b.id, c.id) == ("20261112-ai_girl-001", "20261112-ai_girl-002", "20261112-rain-001")


def test_underscore_in_channel_is_not_a_wildcard(store):
    store.create("aixgirl", today=DAY)
    assert store.create("ai_girl", today=DAY).id.endswith("-001")


def test_create_makes_inbox_and_mirror(store):
    job = store.create("ai_girl", series="hi_there", idea="black knit, wave", today=DAY)
    assert store.inbox_dir(job.id).is_dir()
    mirror = json.loads((store.job_dir(job.id) / "job.json").read_text(encoding="utf-8"))
    assert mirror["status"] == "idea"
    assert mirror["series"] == "hi_there"
    assert job.history[0].to_status == JobStatus.IDEA


def test_normal_path_is_traced(store):
    job = store.create("ai_girl", today=DAY)
    for status in ["scripted", "awaiting_assets", "produced", "in_review", "approved", "published", "analyzed"]:
        job.transition(status)
    store.save(job)
    loaded = store.get(job.id)
    assert loaded.status == JobStatus.ANALYZED
    assert [h.to_status for h in loaded.history][-1] == JobStatus.ANALYZED
    assert len(loaded.history) == 8


def test_invalid_transition_is_refused_unless_forced(store):
    job = store.create("ai_girl", today=DAY)
    with pytest.raises(InvalidTransition):
        job.transition("published")
    job.transition("published", note="posted by hand", force=True)
    assert job.history[-1].forced


def test_rejected_job_can_be_redone(store):
    job = store.create("ai_girl", today=DAY)
    for status in ["scripted", "awaiting_assets", "produced", "in_review"]:
        job.transition(status)
    job.transition("rejected", note="face not visible in the first second")
    job.transition("awaiting_assets", note="regenerate the clip")
    assert job.status == JobStatus.AWAITING_ASSETS


def test_costs_are_summed_and_indexed(store, tmp_path):
    job = store.create("ai_girl", today=DAY)
    job.add_cost("claude", 0.04, model="claude-opus-5-5")
    job.add_cost("claude", 0.02, model="claude-opus-5-5")
    store.save(job)
    assert store.get(job.id).cost_usd == pytest.approx(0.06)


def test_list_filters_by_channel_and_status(store):
    a = store.create("ai_girl", today=DAY)
    store.create("ai_girl", today=DAY)
    store.create("rain", today=DAY)
    a.transition("scripted")
    store.save(a)
    assert len(store.list(channel="ai_girl")) == 2
    assert [j.id for j in store.list(status="scripted")] == [a.id]


def test_bad_ids_are_rejected(store):
    with pytest.raises(ValueError):
        store.get("../../etc")
    with pytest.raises(JobNotFound):
        store.get("20261112-ai_girl-999")
    with pytest.raises(ValueError):
        store.create("AI Girl")


def test_cli_job_lifecycle(tmp_path, monkeypatch):
    shutil.copytree(project_root() / "config", tmp_path / "config")
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    monkeypatch.setenv("FARM_ROOT", str(tmp_path))
    project_root.cache_clear()
    try:
        from farm.cli import app

        runner = CliRunner()
        result = runner.invoke(app, ["job", "new", "ai_girl", "--series", "hi_there"])
        assert result.exit_code == 0, result.output
        job_id = JobStore(root=tmp_path).list()[0].id

        assert runner.invoke(app, ["job", "status", job_id, "scripted"]).exit_code == 0
        refused = runner.invoke(app, ["job", "status", job_id, "published"])
        assert refused.exit_code == 1
        assert "scripted" in runner.invoke(app, ["job", "list"]).output
        assert runner.invoke(app, ["job", "new", "unknown_channel"]).exit_code != 0
    finally:
        project_root.cache_clear()

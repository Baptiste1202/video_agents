import copy

import pytest
import yaml
from pydantic import ValidationError

from farm.core import config
from farm.core.paths import project_root


@pytest.fixture
def ai_girl_raw() -> dict:
    path = project_root() / "config" / "channels" / "ai_girl.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_real_channel_config_loads():
    cfg = config.load_channel("ai_girl")
    assert cfg.format.aspect == "9:16"
    assert cfg.providers.notifier == "cli"
    assert cfg.settings_for("claude")["model"] == "claude-opus-5-5"


def test_real_channel_has_no_missing_files():
    cfg = config.load_channel("ai_girl")
    problems = config.check_channel(cfg)
    # Only open decisions may remain, never broken paths.
    assert all("does not exist" not in p for p in problems), problems


def test_rules_cover_every_platform():
    cfg = config.load_channel("ai_girl")
    assert set(config.load_rules(cfg)) == set(cfg.platforms)


def test_unknown_key_is_rejected(ai_girl_raw):
    raw = copy.deepcopy(ai_girl_raw)
    raw["cadense"] = {"per_day": 1}
    with pytest.raises(ValidationError):
        config.ChannelConfig.model_validate(raw)


def test_spicy_mix_must_sum_to_one(ai_girl_raw):
    raw = copy.deepcopy(ai_girl_raw)
    raw["spicy_mix"] = {"level_0_1": 0.5, "level_2": 0.3}
    with pytest.raises(ValidationError):
        config.ChannelConfig.model_validate(raw)


def test_adult_channel_cannot_target_mainstream_platforms(ai_girl_raw):
    raw = copy.deepcopy(ai_girl_raw)
    raw["content_rating"] = "adult"
    with pytest.raises(ValidationError):
        config.ChannelConfig.model_validate(raw)


def test_unknown_provider_is_rejected(ai_girl_raw):
    raw = copy.deepcopy(ai_girl_raw)
    raw["providers"]["video"] = "sora_api"
    with pytest.raises(ValidationError):
        config.ChannelConfig.model_validate(raw)

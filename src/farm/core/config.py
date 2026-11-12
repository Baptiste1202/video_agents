"""Channel configs (config/channels/*.yaml) and platform rules (rules/*.yaml).

All channel-specific behaviour lives in these files: the engine code must not
special-case a channel. Models forbid unknown keys so that a typo in a YAML
file fails loudly instead of being silently ignored.
"""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from farm.core.paths import project_root

Platform = Literal["instagram_reels", "tiktok", "youtube", "youtube_shorts"]
AgentName = Literal["trends", "scenario", "production", "control", "publication", "analysis", "rules", "style"]
Audience = Literal["male", "female", "both"]

# Adult channels must never publish on these platforms (BRIEF §2, persona §7).
MAINSTREAM_PLATFORMS: set[str] = {"instagram_reels", "tiktok", "youtube", "youtube_shorts"}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class VideoFormat(StrictModel):
    aspect: Literal["9:16", "16:9"]
    min_seconds: float = Field(gt=0)
    max_seconds: float = Field(gt=0)
    subtitles: bool = False
    music: Literal["added_in_app", "royalty_free_baked_in", "none"] = "none"

    @model_validator(mode="after")
    def _check_range(self) -> "VideoFormat":
        if self.min_seconds > self.max_seconds:
            raise ValueError("format.min_seconds must be <= format.max_seconds")
        return self


class Cadence(StrictModel):
    per_day: float = Field(ge=0)
    preferred_hours: list[str] = []
    timezone: str = "Europe/Paris"


class Providers(StrictModel):
    llm: Literal["claude", "openai", "gemini"]
    image: Literal["manual", "nano_banana_api", "flux_lora", "comfyui_local"]
    video: Literal["manual", "comfyui_local", "wan_rented_gpu", "veo_api", "kling_api", "seedance_api", "gemini_omni_api"]
    voice: Literal["none", "elevenlabs"] = "none"
    publisher: Literal["manual", "meta_graph", "third_party"]
    notifier: Literal["cli", "telegram"] = "cli"


class Budget(StrictModel):
    daily_usd: float = Field(ge=0)
    monthly_usd: float = Field(ge=0)
    stop_on_exceed: bool = True


class SpicyMix(StrictModel):
    level_0_1: float = Field(ge=0, le=1)
    level_2: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def _check_sum(self) -> "SpicyMix":
        if abs(self.level_0_1 + self.level_2 - 1) > 1e-6:
            raise ValueError("spicy_mix shares must sum to 1")
        return self


class Trends(StrictModel):
    sources: list[str] = []
    country: str = "FR"
    ideas_per_day: int = Field(default=5, ge=0)
    competitors: list[str] = []


class Compliance(StrictModel):
    ai_profile_label: bool = True
    tiktok_ai_label: bool = True
    commercial_mentions: list[str] = []
    rules_files: list[str] = []


class Captions(StrictModel):
    max_chars: int = Field(gt=0)
    hashtags_max: int = Field(ge=0)
    link_in_bio: str = ""


class ChannelConfig(StrictModel):
    id: str
    enabled: bool = True
    display_name: str
    language: Literal["fr", "en", "both"]
    niche: str
    content_rating: Literal["public", "adult"]
    persona_file: str | None = None
    reference_images: str | None = None
    outfits_dir: str | None = None
    spicy_mix: SpicyMix | None = None
    audience_targets: dict[Audience, float] = {}
    platforms: list[Platform] = Field(min_length=1)
    format: VideoFormat
    cadence: Cadence
    agents: list[AgentName]
    human_review: Literal["required", "on_doubt", "off"]
    providers: Providers
    provider_settings: dict[str, dict] = {}
    budget: Budget
    trends: Trends | None = None
    compliance: Compliance = Compliance()
    captions: Captions

    @model_validator(mode="after")
    def _check_consistency(self) -> "ChannelConfig":
        if self.content_rating == "adult" and MAINSTREAM_PLATFORMS & set(self.platforms):
            raise ValueError("an adult channel must not publish on Instagram, TikTok or YouTube")
        if self.audience_targets and abs(sum(self.audience_targets.values()) - 1) > 1e-6:
            raise ValueError("audience_targets shares must sum to 1")
        return self

    def settings_for(self, provider: str) -> dict:
        return self.provider_settings.get(provider, {})


class VideoRules(StrictModel):
    aspect: str | None = None
    min_seconds: float | None = None
    max_seconds: float | None = None
    max_size_mb: float | None = None
    containers: list[str] = []
    codecs: list[str] = []


class PlatformRules(StrictModel):
    platform: Platform
    updated: str
    video: VideoRules = VideoRules()
    caption_max_chars: int | None = None
    max_api_posts_per_24h: int | None = None
    library_music_via_api: bool | None = None
    required_labels: list[str] = []
    banned_terms: list[str] = []
    notes: list[str] = []


def _read_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return data


def channels_dir(root: Path | None = None) -> Path:
    return (root or project_root()) / "config" / "channels"


def list_channels(root: Path | None = None) -> list[str]:
    return sorted(p.stem for p in channels_dir(root).glob("*.yaml"))


def load_channel(channel_id: str, root: Path | None = None) -> ChannelConfig:
    path = channels_dir(root) / f"{channel_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No channel config: {path}")
    cfg = ChannelConfig.model_validate(_read_yaml(path))
    if cfg.id != channel_id:
        raise ValueError(f"{path}: id '{cfg.id}' does not match the file name")
    return cfg


def load_rules(cfg: ChannelConfig, root: Path | None = None) -> dict[str, PlatformRules]:
    base = root or project_root()
    rules = {}
    for rel in cfg.compliance.rules_files:
        r = PlatformRules.model_validate(_read_yaml(base / rel))
        rules[r.platform] = r
    return rules


def check_channel(cfg: ChannelConfig, root: Path | None = None) -> list[str]:
    """Return human-readable problems that schema validation cannot catch (missing files, TODOs)."""
    base = root or project_root()
    problems = []
    for label, rel in [
        ("persona_file", cfg.persona_file),
        ("reference_images", cfg.reference_images),
        ("outfits_dir", cfg.outfits_dir),
        *(("rules_files", r) for r in cfg.compliance.rules_files),
    ]:
        if rel and not (base / rel).exists():
            problems.append(f"{label}: {rel} does not exist")
    missing_rules = set(cfg.platforms) - set(load_rules(cfg, base)) if not problems else set()
    for platform in sorted(missing_rules):
        problems.append(f"no rules file for platform {platform}")
    if cfg.captions.link_in_bio.upper() == "TO_DECIDE":
        problems.append("captions.link_in_bio is still TO_DECIDE")
    return problems

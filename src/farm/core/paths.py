"""Project root discovery: every path in configs is relative to this root."""

import os
from functools import cache
from pathlib import Path


@cache
def project_root() -> Path:
    override = os.environ.get("FARM_ROOT")
    if override:
        return Path(override).resolve()
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "config").is_dir():
            return parent
    raise RuntimeError("Project root not found: set FARM_ROOT")

"""XDG-compliant path resolution for herald.

Config: ~/.config/herald/ (or $XDG_CONFIG_HOME/herald/)
Data:   ~/.local/share/herald/ (or $XDG_DATA_HOME/herald/)
"""
from __future__ import annotations

import os
from pathlib import Path

_APP = "herald"


def config_dir() -> Path:
    """Return config directory (~/.config/herald/ or XDG override)."""
    base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(base) / _APP


def data_dir() -> Path:
    """Return data directory (~/.local/share/herald/ or XDG override)."""
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / _APP


def config_file() -> Path:
    """Return path to config.yaml."""
    return config_dir() / "config.yaml"


def venv_dir() -> Path:
    """Return path to Python venv."""
    return data_dir() / ".venv"


def raw_dir() -> Path:
    """Return path to raw JSONL data."""
    return data_dir() / "data" / "raw"


def digests_dir() -> Path:
    """Return path to digest markdown files."""
    return data_dir() / "data" / "digests"


def state_dir() -> Path:
    """Return path to state files (seen_urls, last_run, log)."""
    return data_dir() / "data" / "state"

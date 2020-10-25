"""
Configurations for the Lira app.

The XDG base directory specification is used for all data and configuration files.
See https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html.
"""

import os
from pathlib import Path

IS_WINDOWS = os.name == "nt"


def _get_config_dir():
    default_config_dir = "~/AppData/Local/" if IS_WINDOWS else "~/.config/"
    root_config_dir = os.environ.get("XDG_CONFIG_HOME", default_config_dir)
    return Path(root_config_dir).expanduser() / "lira"


def _get_data_dir():
    default_data_dir = "~/AppData/Local/" if IS_WINDOWS else "~/.local/share/"
    root_data_dir = os.environ.get("XDG_DATA_HOME", default_data_dir)
    dir = "lira-data" if IS_WINDOWS else "lira"
    return Path(root_data_dir).expanduser() / dir


CONFIG_DIR = _get_config_dir()
CONFIG_FILE = CONFIG_DIR / "config.yaml"
DATA_DIR = _get_data_dir()
LOG_DIR = DATA_DIR / "log"

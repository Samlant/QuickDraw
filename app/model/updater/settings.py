import logging
import os
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

# App info
APP_NAME = "QuickDraw"
APP_VERSION = "3.2.0"

# Current module dir (when frozen this equals sys._MEIPASS)
MODULE_DIR = Path(__file__).resolve().parents[2]

FROZEN = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
# For development
DEV_DIR = MODULE_DIR.parent / "repo"

# App directories

PER_USER_DATA_DIR = Path(os.getenv("LOCALAPPDATA"))
PER_MACHINE_PROGRAMS_DIR = Path(os.getenv("ProgramFiles"))


PROGRAMS_DIR = PER_MACHINE_PROGRAMS_DIR if FROZEN else DEV_DIR
DATA_DIR = PER_USER_DATA_DIR if FROZEN else DEV_DIR

INSTALL_DIR = PROGRAMS_DIR / APP_NAME
UPDATE_CACHE_DIR = DATA_DIR / APP_NAME / "update_cache"
METADATA_DIR = UPDATE_CACHE_DIR / "metadata"
TARGET_DIR = UPDATE_CACHE_DIR / "targets"

# Update-server urls
METADATA_BASE_URL = "https://raw.githubusercontent.com/Samlant/updater/main/metadata"
TARGET_BASE_URL = "https://raw.githubusercontent.com/Samlant/updater/main/targets"

# Location of trusted root metadata file
TRUSTED_ROOT_SRC = MODULE_DIR / "root.json"
if not FROZEN:
    # for development, get the root metadata directly from local repo
    sys.path.insert(0, str(MODULE_DIR.parent))
    from repo_settings import REPO_DIR

    TRUSTED_ROOT_SRC = REPO_DIR / "metadata" / "root.json"
TRUSTED_ROOT_DST = METADATA_DIR / "root.json"

import logging
import os
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

# App info
APP_NAME = "QuickDraw"
APP_VERSION = "3.0.1"

# Current module dir (when frozen this equals sys._MEIPASS)
# https://pyinstaller.org/en/stable/runtime-information.html#using-file
MODULE_DIR = Path(__file__).resolve().parents[2]

# Are we running in a PyInstaller bundle?
# https://pyinstaller.org/en/stable/runtime-information.html
FROZEN = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")
print("Are we frozen?")
print(FROZEN)
print(f"The MODULE_DIR is: {MODULE_DIR}")
# For development
DEV_DIR = MODULE_DIR.parent / "repo"
print(f"The DEV_DIR is: {DEV_DIR}")
# App directories

PER_USER_DATA_DIR = Path(os.getenv("LOCALAPPDATA"))
PER_USER_PROGRAMS_DIR = Path(os.getenv("LOCALAPPDATA")) / "Programs"


PROGRAMS_DIR = PER_USER_PROGRAMS_DIR if FROZEN else DEV_DIR
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

print(f"the trusted root SRC dir: {TRUSTED_ROOT_SRC}")
print(f"the trusted root DEST dir: {TRUSTED_ROOT_DST}")

import logging
import os
from pathlib import Path
import sys

from tufup.utils.platform_specific import ON_WINDOWS

logger = logging.getLogger(__name__)

# App info
APP_NAME = 'QuickDraw'
APP_VERSION = '3.0.0'

# Current module dir (when frozen this equals sys._MEIPASS)
# https://pyinstaller.org/en/stable/runtime-information.html#using-file
MODULE_DIR = Path(__file__).resolve().parent

# Are we running in a PyInstaller bundle?
# https://pyinstaller.org/en/stable/runtime-information.html
FROZEN = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# For development
DEV_DIR = MODULE_DIR.parent.parent / 'temp'

# App directories
if ON_WINDOWS:
    # Windows per-user paths
    PER_USER_DATA_DIR = Path(os.getenv('LOCALAPPDATA')) / "Work-Tools"
    PER_USER_PROGRAMS_DIR = PER_USER_DATA_DIR / 'QuickDraw'
else:
    raise NotImplementedError('Unsupported platform')

PROGRAMS_DIR = PER_USER_PROGRAMS_DIR if FROZEN else DEV_DIR
DATA_DIR = PER_USER_DATA_DIR if FROZEN else DEV_DIR

INSTALL_DIR = PROGRAMS_DIR / APP_NAME
UPDATE_CACHE_DIR = DATA_DIR / APP_NAME / 'update_cache'
METADATA_DIR = UPDATE_CACHE_DIR / 'metadata'
TARGET_DIR = UPDATE_CACHE_DIR / 'targets'

# Update-server urls
METADATA_BASE_URL = ''
TARGET_BASE_URL = ''

# Location of trusted root metadata file
TRUSTED_ROOT_SRC = MODULE_DIR.parent / 'root.json'
if not FROZEN:
    # for development, get the root metadata directly from local repo
    sys.path.insert(0, str(MODULE_DIR.parent.parent))
    from repo_settings import REPO_DIR
    TRUSTED_ROOT_SRC =  REPO_DIR / 'metadata' / 'root.json'
TRUSTED_ROOT_DST = METADATA_DIR / 'root.json'
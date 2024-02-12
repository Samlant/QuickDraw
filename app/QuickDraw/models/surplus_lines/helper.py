from pathlib import Path

from QuickDraw.helper import TEST

# from dotenv import load_dotenv
# from os import environ

# If testing: set to True:
INDIVIDUAL_MODULE = TEST

if INDIVIDUAL_MODULE:
    FSL_DOC_PATH = Path(__file__).parents[1] / "resources" / "fsl_stamp.pdf"
    ENV_PATH = Path(__file__).parents[1] / "resources" / ".env"
else:
    FSL_DOC_PATH = (
        Path(__file__).parents[2]
        / "resources"
        / "forms"
        / "east_coast_forms"
        / "fsl_stamp.pdf"
    )
    ENV_PATH = Path.home() / "AppData" / "Local" / "QuickDraw" / ".env"

# load_dotenv(
#     str(ENV_PATH),
#     verbose=True,
# )
# OUTPUT_DIR = environ.get("OUTPUT_DIR")

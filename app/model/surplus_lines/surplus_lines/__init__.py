from pathlib import Path

# from dotenv import load_dotenv
# from os import environ


INDIVIDUAL_MODULE = True

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
    ENV_PATH = Path.home() / "AppData" / "QuickDraw" / ".env"

# load_dotenv(
#     str(ENV_PATH),
#     verbose=True,
# )
# OUTPUT_DIR = environ.get("OUTPUT_DIR")

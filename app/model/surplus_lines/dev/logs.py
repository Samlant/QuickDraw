from pathlib import Path

log_file: Path = Path.home() / "AppData" / "Local" / "QuickDraw" / "sys.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            # "style": "$",
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": str(log_file),
            "mode": "w",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "__main__": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "model.surplus_lines.automation": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "model.surplus_lines.carriers.base": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "model.surplus_lines.carriers.builders.concept": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "model.surplus_lines.carriers.builders.kemah": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "model.surplus_lines.carriers.builders.yachtinsure": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "model.surplus_lines.doc.filler": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "model.surplus_lines.doc.parser": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "model.surplus_lines.web.scraper": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

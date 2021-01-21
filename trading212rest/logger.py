"""
https://stackoverflow.com/questions/38323810/does-pythons-logging-config-dictconfig-apply-the-loggers-configuration-setti
"""

import logging
from logging.config import dictConfig
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('selenium').setLevel(logging.WARNING)

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "formatter_fileFormatter": {
            "class": "logging.Formatter",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "%(asctime)s %(name)-25s - %(levelname)-15s: %(filename)s:%(lineno)-4s %(message)s"
        },
        "formatter_stdFormatter": {
            "class": "logging.Formatter",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": " %(asctime)s %(name)-25s - %(levelname)-15s:%(message)s"
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "formatter_stdFormatter",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "formatter_fileFormatter",
            "filename": "trading212.log",
            "mode": "w",
            "encoding": "utf-8"
        }
    },

    "loggers": {},

    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    }
}

dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger(__name__)
from enum import Enum

from logging import captureWarnings
from logging import getLogger
from logging.config import dictConfig

from pydantic_settings import BaseSettings

from .db.db_config import DBSettings, db_settings
from backend_config.environments import LOG_LEVEL


class LogLevel(str, Enum):
    """
    Explicit enumerated class for acceptable Uvicorn log levels.
    This type is primarily consumed by the core_logger setup.
    """
    critical = "critical"
    error = "error"
    warning = "warning"
    info = "info"
    debug = "debug"


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    LOGS_LEVEL: LogLevel = LOG_LEVEL

    db: DBSettings = db_settings


settings = Settings()


LOG_CONFIG = {
    "version": 1,
    # "disable_existing_loggers": True,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "'%(asctime)s' - %(levelname)s:\t [%(filename)s:%(funcName)s:%(lineno)d]:\t %(message)s"
            # "format": "'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
        }
    },
    "handlers": {
        "debug_file": {
            "formatter": "default",
            "level": settings.LOGS_LEVEL.upper(),
            "class": "logging.FileHandler",
            "filename": "././logs/debug.log",
        },
        "error_file": {
            "formatter": "default",
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "././logs/error.log",
        },
        # "console": {
        #     "formatter": "default",
        #     "class": "logging.StreamHandler",
        #     "stream": "ext://sys.stdout",
        #     "level": settings.LOG_LEVEL.upper(),
        # },
    },
    "root": {"handlers": ["debug_file", "error_file"], "level": settings.LOGS_LEVEL.upper()},
    "loggers": {
        "uvicorn": {
            "handlers": ["debug_file"],
            "level": settings.LOGS_LEVEL.upper(),
            "propagate": True, },
        "": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": True, },
    }

}


captureWarnings(True)
dictConfig(LOG_CONFIG)
core_logger = getLogger(__name__)
core_logger.debug(str(settings))

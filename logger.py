"""
BOT_V3 Logger
Professional logging system
"""

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

# ==========================================
# LOGS DIRECTORY
# ==========================================

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# ==========================================
# LOGGER
# ==========================================

logger = logging.getLogger("BOT_V3")
logger.setLevel(logging.INFO)

# Logger qayta yuklanganda handlerlar takror qo'shilmasligi uchun
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # INFO log
    info_handler = RotatingFileHandler(
        LOGS_DIR / "bot.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    # ERROR log
    error_handler = RotatingFileHandler(
        LOGS_DIR / "error.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Console log
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

# ==========================================
# FUNCTIONS
# ==========================================

def info(message):
    logger.info(message)


def warning(message):
    logger.warning(message)


def error(message):
    logger.error(message)


def critical(message):
    logger.critical(message)


def debug(message):
    logger.debug(message)


def exception(message):
    logger.exception(message)

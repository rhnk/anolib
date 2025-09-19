import logging
import os

from anolib.constants import LOGGER_MAX_LEN, LOGGER_NAMESPACE

logger = logging.getLogger(LOGGER_NAMESPACE)

LOGGER_LEVEL = logging.INFO

if _level_env := os.environ.get("ANOLIB_LOG_LEVEL"):
    _level_env = _level_env.upper().strip()
    logger_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARN,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "FATAL": logging.FATAL,
    }
    LOGGER_LEVEL = logger_levels.get(_level_env, logging.INFO)

logger.setLevel(LOGGER_LEVEL)


def __format(args):
    """Format arguments for logging with length limits."""
    return "\t".join(
        [
            (
                repr(arg)
                if len(str(arg)) <= LOGGER_MAX_LEN
                else f"{str(arg)[:LOGGER_MAX_LEN]}..."
            )
            for arg in args
        ]
    )


def debug(*args):
    logger.debug(__format(args))


def info(*args):
    logger.info(__format(args))


def warn(*args):
    logger.warning(__format(args))


def error(*args, exc_info=True):
    logger.error(__format(args), exc_info=exc_info)

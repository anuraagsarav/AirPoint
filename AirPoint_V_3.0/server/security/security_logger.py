import logging
from pathlib import Path

from server.config import (
    SECURITY_LOG_DETAILS,
    SECURITY_LOG_FILE
)


_logger = None


def get_security_logger():
    global _logger

    if _logger is not None:
        return _logger

    log_path = Path(SECURITY_LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("airpoint.security")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s"
            )
        )
        logger.addHandler(handler)

    _logger = logger
    return logger


def log_info(message, **details):
    get_security_logger().info(_format_message(message, details))


def log_warning(message, **details):
    get_security_logger().warning(_format_message(message, details))


def _format_message(message, details):
    if not SECURITY_LOG_DETAILS:
        return message

    if not details:
        return message

    fields = ", ".join(
        f"{key}={value}" for key, value in details.items()
    )

    return f"{message} ({fields})"

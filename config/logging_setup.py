"""
logging_setup.py
Fuzzinator — Logging Infrastructure

Configures structured logging throughout the application.
"""

import logging
import sys
from typing import Optional
from config import Config


def setup_logging(config: Config, name: str = "fuzzinator") -> logging.Logger:
    """
    Configure structured logging based on config.

    Args:
        config: Configuration object
        name: Logger name

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)

    # Clear any existing handlers
    logger.handlers = []

    # Get log level
    level_str = config.get("logging.level", "INFO")
    level = getattr(logging, level_str, logging.INFO)
    logger.setLevel(level)

    # Log format
    log_format = config.get(
        "logging.format",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    formatter = logging.Formatter(log_format)

    # Console handler (always enabled)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    log_file = config.get("logging.file")
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.info(f"Logging to file: {log_file}")
        except IOError as e:
            logger.warning(f"Could not create log file {log_file}: {e}")

    return logger

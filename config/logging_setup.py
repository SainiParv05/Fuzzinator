"""
logging_setup.py
Fuzzinator — Logging Infrastructure

Configures structured logging throughout the application.
"""

import logging
import os
import sys
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
    # Get log level
    level_str = config.get("logging.level", "INFO")
    level = getattr(logging, level_str, logging.INFO)

    # Log format
    log_format = config.get(
        "logging.format",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    formatter = logging.Formatter(log_format)

    # Configure the root logger so module-level loggers inherit handlers.
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(level)

    # Console handler (always enabled)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    log_file = config.get("logging.file")
    if log_file:
        try:
            if not os.path.isabs(log_file):
                log_file = os.path.join(config._project_root, log_file)
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except IOError as e:
            root_logger.warning(f"Could not create log file {log_file}: {e}")

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = True
    if log_file:
        logger.info(f"Logging to file: {log_file}")
    return logger

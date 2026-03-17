"""
crash_vault.py
Fuzzinator — Crash Input Storage

When a crash is detected, saves the crashing input to data/crashes/
with a filename that includes the input hash and the crash signal.
"""

import os
import hashlib
import logging
import re


logger = logging.getLogger(__name__)


def _sanitize_signal_name(signal_name: str) -> str:
    """
    Sanitize signal name for filesystem safety.

    Removes any characters that aren't alphanumeric, underscore, or hyphen.

    Args:
        signal_name: Original signal name

    Returns:
        Sanitized signal name
    """
    # Keep only alphanumeric, underscore, and hyphen
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "", signal_name)
    # Ensure non-empty
    return sanitized if sanitized else "UNKNOWN"


class CrashVault:
    """Stores crashing inputs for later analysis."""

    def __init__(self, output_dir: str = "data/crashes"):
        # Validate and normalize output directory
        self.output_dir = os.path.abspath(output_dir)
        self.crash_hashes = set()

        try:
            os.makedirs(self.output_dir, exist_ok=True)
            logger.debug(f"Crash vault output directory: {self.output_dir}")
        except OSError as e:
            logger.error(f"Failed to create crash vault directory {self.output_dir}: {e}")
            raise

    def save_crash(self, input_data: bytearray, signal_name: str) -> str:
        """
        Save a crashing input to disk.

        Args:
            input_data: The input that caused the crash
            signal_name: Name of the crash signal (e.g., SIGSEGV)

        Returns:
            Path to the saved crash file, or empty string if duplicate

        Raises:
            ValueError: If input_data or signal_name is invalid
        """
        if not isinstance(input_data, (bytes, bytearray)):
            raise ValueError("input_data must be bytes or bytearray")

        if not isinstance(signal_name, str):
            raise ValueError("signal_name must be a string")

        # Hash the input to avoid duplicates
        input_hash = hashlib.sha256(bytes(input_data)).hexdigest()[:16]

        if input_hash in self.crash_hashes:
            logger.debug(f"Duplicate crash detected (hash: {input_hash})")
            return ""  # Duplicate crash

        self.crash_hashes.add(input_hash)

        # Sanitize signal name for filesystem safety
        safe_signal_name = _sanitize_signal_name(signal_name)

        # Build filename: crash_<signal>_<hash>.bin
        filename = f"crash_{safe_signal_name}_{input_hash}.bin"
        filepath = os.path.join(self.output_dir, filename)

        # Verify filepath is within output_dir (prevent directory traversal)
        real_filepath = os.path.abspath(filepath)
        if not real_filepath.startswith(os.path.abspath(self.output_dir)):
            logger.error(f"Security check failed: attempted path {real_filepath}")
            raise ValueError("Invalid file path (directory traversal detected)")

        try:
            with open(real_filepath, "wb") as f:
                f.write(bytes(input_data))
            logger.info(f"New crash saved: {filename} (signal: {signal_name})")
        except OSError as e:
            logger.error(f"Failed to save crash {filename}: {e}")
            raise

        return real_filepath

    @property
    def total_crashes(self) -> int:
        """Return number of unique crashes found."""
        return len(self.crash_hashes)

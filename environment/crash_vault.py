"""
crash_vault.py
Fuzzinator — Crash Input Storage

When a crash is detected, saves the crashing input to data/crashes/
with a filename that includes the input hash and the crash signal.
"""

import os
import hashlib


class CrashVault:
    """Stores crashing inputs for later analysis."""

    def __init__(self, output_dir: str = "data/crashes"):
        self.output_dir = output_dir
        self.crash_hashes = set()
        os.makedirs(self.output_dir, exist_ok=True)

    def save_crash(self, input_data: bytearray, signal_name: str) -> str:
        """
        Save a crashing input to disk.

        Args:
            input_data: The input that caused the crash
            signal_name: Name of the crash signal (e.g., SIGSEGV)

        Returns:
            Path to the saved crash file, or empty string if duplicate
        """
        # Hash the input to avoid duplicates
        input_hash = hashlib.sha256(bytes(input_data)).hexdigest()[:16]

        if input_hash in self.crash_hashes:
            return ""  # Duplicate crash

        self.crash_hashes.add(input_hash)

        # Build filename: crash_<signal>_<hash>.bin
        filename = f"crash_{signal_name}_{input_hash}.bin"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(bytes(input_data))

        return filepath

    @property
    def total_crashes(self) -> int:
        """Return number of unique crashes found."""
        return len(self.crash_hashes)

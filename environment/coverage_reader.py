"""
coverage_reader.py
Fuzzinator — Coverage Bitmap Reader

Reads the shared memory coverage bitmap at /dev/shm/fuzz_bitmap,
counts edge hits, and detects new coverage.
"""

import os
import numpy as np

BITMAP_PATH = "/dev/shm/fuzz_bitmap"
BITMAP_SIZE = 65536
# Number of coverage buckets for the observation vector
OBS_BUCKETS = 64


class CoverageReader:
    """Reads and analyzes coverage bitmap from shared memory."""

    def __init__(self):
        self.global_coverage = np.zeros(BITMAP_SIZE, dtype=np.uint8)
        self.total_edges_seen = 0

    def reset_bitmap(self):
        """Zero out the shared memory bitmap before each execution."""
        try:
            with open(BITMAP_PATH, "r+b") as f:
                f.write(b"\x00" * BITMAP_SIZE)
        except FileNotFoundError:
            # Create if missing
            with open(BITMAP_PATH, "wb") as f:
                f.write(b"\x00" * BITMAP_SIZE)

    def read_bitmap(self) -> np.ndarray:
        """Read the current coverage bitmap from shared memory."""
        try:
            with open(BITMAP_PATH, "rb") as f:
                raw = f.read(BITMAP_SIZE)
            return np.frombuffer(raw, dtype=np.uint8).copy()
        except FileNotFoundError:
            return np.zeros(BITMAP_SIZE, dtype=np.uint8)

    def get_edge_count(self, bitmap: np.ndarray) -> int:
        """Count the number of edges hit in this bitmap."""
        return int(np.count_nonzero(bitmap))

    def get_new_edges(self, bitmap: np.ndarray) -> int:
        """
        Count edges in the bitmap that are NEW (not previously seen).
        Also updates the global coverage map.
        """
        new_edges = 0
        for i in range(BITMAP_SIZE):
            if bitmap[i] > 0 and self.global_coverage[i] == 0:
                new_edges += 1
                self.global_coverage[i] = bitmap[i]

        self.total_edges_seen = int(np.count_nonzero(self.global_coverage))
        return new_edges

    def get_coverage_vector(self, bitmap: np.ndarray) -> np.ndarray:
        """
        Compress the full bitmap into a fixed-size observation vector.

        Divides the 65536-byte bitmap into OBS_BUCKETS sections and
        computes the proportion of non-zero bytes in each section.
        Returns a float32 array of shape (OBS_BUCKETS,) in [0, 1].
        """
        section_size = BITMAP_SIZE // OBS_BUCKETS
        vector = np.zeros(OBS_BUCKETS, dtype=np.float32)

        for i in range(OBS_BUCKETS):
            start = i * section_size
            end = start + section_size
            section = bitmap[start:end]
            vector[i] = np.count_nonzero(section) / section_size

        return vector

    def reset(self):
        """Reset all global coverage tracking."""
        self.global_coverage = np.zeros(BITMAP_SIZE, dtype=np.uint8)
        self.total_edges_seen = 0

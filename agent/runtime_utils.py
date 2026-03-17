"""
runtime_utils.py
Utilities for reproducible RL fuzzing experiments.
"""

from __future__ import annotations

import random

import numpy as np


def set_random_seed(seed: int) -> None:
    """Seed Python, NumPy, and torch when available."""
    if seed < 0:
        raise ValueError("seed must be non-negative")

    random.seed(seed)
    np.random.seed(seed)

    try:
        import torch
    except ModuleNotFoundError:
        return

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    try:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except AttributeError:
        pass

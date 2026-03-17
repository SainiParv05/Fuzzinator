"""
fuzz_env_lstm.py
Fuzzinator — Fuzzing environment with sequence context for PPO+LSTM.
"""

from __future__ import annotations

import numpy as np

from environment.fuzz_env import FuzzEnv


class FuzzEnvLSTM(FuzzEnv):
    """Extend the base environment with action-history and raw-input helpers."""

    def __init__(self, *args, action_history_len: int = 8, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_history_len = action_history_len
        self.action_history = np.zeros(action_history_len, dtype=np.int64)

    def reset(self, seed=None, options=None):
        obs, info = super().reset(seed=seed, options=options)
        self.action_history.fill(0)
        info["raw_input"] = self.get_current_input_array()
        info["action_history"] = self.action_history.copy()
        return obs, info

    def step(self, action: int):
        obs, reward, terminated, truncated, info = super().step(action)
        self.action_history = np.roll(self.action_history, -1)
        self.action_history[-1] = action
        info["raw_input"] = self.get_current_input_array()
        info["action_history"] = self.action_history.copy()
        return obs, reward, terminated, truncated, info

    def get_current_input_array(self) -> np.ndarray:
        padded = np.zeros(self.max_input_len, dtype=np.int64)
        if not self.current_input:
            return padded

        clipped = bytes(self.current_input[:self.max_input_len])
        encoded = np.frombuffer(clipped, dtype=np.uint8).astype(np.int64) + 1
        padded[-len(encoded):] = encoded
        return padded

"""
replay_buffer_lstm.py
Fuzzinator — PPO rollout buffer with raw-input context for LSTM training.
"""

from __future__ import annotations

import numpy as np
import torch


class RolloutBufferLSTM:
    """Store PPO transitions including raw inputs and action history."""

    def __init__(self,
                 buffer_size: int,
                 obs_size: int,
                 max_input_len: int = 1024,
                 action_history_len: int = 8,
                 gamma: float = 0.99,
                 gae_lambda: float = 0.95):
        self.buffer_size = buffer_size
        self.gamma = gamma
        self.gae_lambda = gae_lambda

        self.obs = np.zeros((buffer_size, obs_size), dtype=np.float32)
        self.raw_inputs = np.zeros((buffer_size, max_input_len), dtype=np.int64)
        self.action_history = np.zeros((buffer_size, action_history_len), dtype=np.int64)
        self.actions = np.zeros(buffer_size, dtype=np.int64)
        self.rewards = np.zeros(buffer_size, dtype=np.float32)
        self.log_probs = np.zeros(buffer_size, dtype=np.float32)
        self.values = np.zeros(buffer_size, dtype=np.float32)
        self.dones = np.zeros(buffer_size, dtype=np.float32)
        self.advantages = np.zeros(buffer_size, dtype=np.float32)
        self.returns = np.zeros(buffer_size, dtype=np.float32)

        self.ptr = 0
        self.full = False

    def store(self,
              obs: np.ndarray,
              raw_input: np.ndarray,
              action_history: np.ndarray,
              action: int,
              reward: float,
              log_prob: float,
              value: float,
              done: bool):
        if self.ptr >= self.buffer_size:
            raise IndexError("rollout buffer is full")

        self.obs[self.ptr] = obs
        self.raw_inputs[self.ptr] = raw_input
        self.action_history[self.ptr] = action_history
        self.actions[self.ptr] = action
        self.rewards[self.ptr] = reward
        self.log_probs[self.ptr] = log_prob
        self.values[self.ptr] = value
        self.dones[self.ptr] = float(done)

        self.ptr += 1
        if self.ptr >= self.buffer_size:
            self.full = True

    def compute_advantages(self, last_value: float):
        size = self.ptr if not self.full else self.buffer_size
        last_gae = 0.0

        for t in reversed(range(size)):
            if t == size - 1:
                next_value = last_value
                next_done = 0.0
            else:
                next_value = self.values[t + 1]
                next_done = self.dones[t + 1]

            delta = self.rewards[t] + self.gamma * next_value * (1 - next_done) - self.values[t]
            last_gae = delta + self.gamma * self.gae_lambda * (1 - next_done) * last_gae
            self.advantages[t] = last_gae

        self.returns[:size] = self.advantages[:size] + self.values[:size]

    def get_batches(self, batch_size: int):
        size = self.ptr if not self.full else self.buffer_size
        indices = np.random.permutation(size)

        for start in range(0, size, batch_size):
            batch_idx = indices[start:start + batch_size]
            yield {
                "obs": torch.as_tensor(self.obs[batch_idx], dtype=torch.float32),
                "raw_input": torch.as_tensor(self.raw_inputs[batch_idx], dtype=torch.long),
                "action_history": torch.as_tensor(self.action_history[batch_idx], dtype=torch.long),
                "actions": torch.as_tensor(self.actions[batch_idx], dtype=torch.long),
                "log_probs": torch.as_tensor(self.log_probs[batch_idx], dtype=torch.float32),
                "advantages": torch.as_tensor(self.advantages[batch_idx], dtype=torch.float32),
                "returns": torch.as_tensor(self.returns[batch_idx], dtype=torch.float32),
            }

    def reset(self):
        self.ptr = 0
        self.full = False

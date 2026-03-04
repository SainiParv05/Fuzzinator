"""
replay_buffer.py
Fuzzinator — Rollout Buffer for PPO

Stores transitions (state, action, reward, log_prob, value, done)
collected during environment interaction. Used by the PPO agent
to compute advantages and perform policy updates.
"""

import numpy as np
import torch


class RolloutBuffer:
    """
    Fixed-size buffer for storing PPO rollout data.

    Stores transitions during environment interaction and computes
    Generalized Advantage Estimation (GAE) for policy updates.
    """

    def __init__(self, buffer_size: int, obs_size: int,
                 gamma: float = 0.99, gae_lambda: float = 0.95):
        self.buffer_size = buffer_size
        self.gamma = gamma
        self.gae_lambda = gae_lambda

        # Pre-allocate storage
        self.states = np.zeros((buffer_size, obs_size), dtype=np.float32)
        self.actions = np.zeros(buffer_size, dtype=np.int64)
        self.rewards = np.zeros(buffer_size, dtype=np.float32)
        self.log_probs = np.zeros(buffer_size, dtype=np.float32)
        self.values = np.zeros(buffer_size, dtype=np.float32)
        self.dones = np.zeros(buffer_size, dtype=np.float32)

        # Computed after rollout
        self.advantages = np.zeros(buffer_size, dtype=np.float32)
        self.returns = np.zeros(buffer_size, dtype=np.float32)

        self.ptr = 0
        self.full = False

    def store(self, state: np.ndarray, action: int, reward: float,
              log_prob: float, value: float, done: bool):
        """Store a single transition."""
        self.states[self.ptr] = state
        self.actions[self.ptr] = action
        self.rewards[self.ptr] = reward
        self.log_probs[self.ptr] = log_prob
        self.values[self.ptr] = value
        self.dones[self.ptr] = float(done)

        self.ptr += 1
        if self.ptr >= self.buffer_size:
            self.full = True

    def compute_advantages(self, last_value: float):
        """
        Compute GAE advantages and discounted returns.

        Args:
            last_value: Value estimate for the state after the last transition
        """
        size = self.ptr if not self.full else self.buffer_size
        last_gae = 0.0

        for t in reversed(range(size)):
            if t == size - 1:
                next_value = last_value
                next_done = 0.0
            else:
                next_value = self.values[t + 1]
                next_done = self.dones[t + 1]

            delta = (self.rewards[t]
                     + self.gamma * next_value * (1 - next_done)
                     - self.values[t])
            last_gae = delta + self.gamma * self.gae_lambda * (1 - next_done) * last_gae
            self.advantages[t] = last_gae

        self.returns[:size] = self.advantages[:size] + self.values[:size]

    def get_batches(self, batch_size: int):
        """
        Yield mini-batches of transitions as PyTorch tensors.

        Args:
            batch_size: Number of transitions per batch

        Yields:
            Dict with keys: states, actions, log_probs, advantages, returns
        """
        size = self.ptr if not self.full else self.buffer_size
        indices = np.random.permutation(size)

        for start in range(0, size, batch_size):
            end = start + batch_size
            batch_idx = indices[start:end]

            yield {
                "states": torch.FloatTensor(self.states[batch_idx]),
                "actions": torch.LongTensor(self.actions[batch_idx]),
                "log_probs": torch.FloatTensor(self.log_probs[batch_idx]),
                "advantages": torch.FloatTensor(self.advantages[batch_idx]),
                "returns": torch.FloatTensor(self.returns[batch_idx]),
            }

    def reset(self):
        """Clear the buffer for a new rollout."""
        self.ptr = 0
        self.full = False

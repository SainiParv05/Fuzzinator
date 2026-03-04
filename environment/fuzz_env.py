"""
fuzz_env.py
Fuzzinator — Gymnasium-compatible Fuzzing Environment

Wraps the entire fuzzing loop (mutate → execute → read coverage → reward)
as an OpenAI Gymnasium environment for RL training.

Observation space: 67 floats
  [0:64]  — compressed coverage bitmap (64 buckets)
  [64]    — last mutation action (normalized)
  [65]    — input length (normalized)
  [66]    — step count (normalized)

Action space: Discrete(4) — selects mutation strategy
"""

import os
import sys
import numpy as np
import gymnasium as gym
from gymnasium import spaces

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mutator.mutator import mutate, NUM_ACTIONS
from environment.execution_harness import ExecutionHarness
from environment.coverage_reader import CoverageReader
from environment.crash_vault import CrashVault
from agent.reward_engine import RewardEngine


# Observation size
OBS_SIZE = 67
MAX_INPUT_LEN = 1024
MAX_STEPS = 10000


class FuzzEnv(gym.Env):
    """
    Fuzzing environment for RL-guided mutation selection.

    The agent chooses which mutation strategy to apply at each step.
    The environment executes the mutated input, reads coverage,
    and returns a reward based on new coverage and crashes.
    """

    metadata = {"render_modes": ["human"]}

    def __init__(self, target_path: str, seed_path: str,
                 crash_dir: str = "data/crashes",
                 max_steps: int = MAX_STEPS):
        super().__init__()

        self.target_path = target_path
        self.seed_path = seed_path
        self.max_steps = max_steps

        # Components
        self.harness = ExecutionHarness(target_path)
        self.coverage = CoverageReader()
        self.crash_vault = CrashVault(crash_dir)
        self.reward_engine = RewardEngine()

        # Spaces
        self.action_space = spaces.Discrete(NUM_ACTIONS)
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(OBS_SIZE,), dtype=np.float32
        )

        # State
        self.current_input = bytearray()
        self.step_count = 0
        self.last_action = 0

    def reset(self, seed=None, options=None):
        """Reset the environment to the initial seed input."""
        super().reset(seed=seed)

        # Load seed file
        with open(self.seed_path, "rb") as f:
            self.current_input = bytearray(f.read())

        # Reset components
        self.coverage.reset()
        self.coverage.reset_bitmap()
        self.step_count = 0
        self.last_action = 0

        obs = self._get_observation(np.zeros(64, dtype=np.float32))
        return obs, {}

    def step(self, action: int):
        """
        Execute one fuzzing step:
          1. Mutate input using chosen strategy
          2. Execute target
          3. Read coverage
          4. Compute reward

        Returns:
            observation, reward, terminated, truncated, info
        """
        self.step_count += 1
        self.last_action = action

        # 1. Mutate
        mutated_input = mutate(self.current_input, action)

        # 2. Reset bitmap and execute
        self.coverage.reset_bitmap()
        exec_result = self.harness.run(mutated_input)

        # 3. Read coverage
        bitmap = self.coverage.read_bitmap()
        new_edges = self.coverage.get_new_edges(bitmap)
        edge_count = self.coverage.get_edge_count(bitmap)
        coverage_vector = self.coverage.get_coverage_vector(bitmap)

        # 4. Handle crash
        crash_path = ""
        if exec_result.crashed:
            crash_path = self.crash_vault.save_crash(
                mutated_input, exec_result.signal_name
            )

        # 5. Compute reward
        reward = self.reward_engine.compute(
            new_edges=new_edges,
            crashed=exec_result.crashed,
        )

        # 6. Update current input if we found new coverage
        if new_edges > 0:
            self.current_input = mutated_input

        # 7. Build observation
        obs = self._get_observation(coverage_vector)

        # Termination
        terminated = False
        truncated = self.step_count >= self.max_steps

        info = {
            "new_edges": new_edges,
            "total_edges": self.coverage.total_edges_seen,
            "edge_count": edge_count,
            "crashed": exec_result.crashed,
            "signal": exec_result.signal_name,
            "crash_path": crash_path,
            "total_crashes": self.crash_vault.total_crashes,
            "timed_out": exec_result.timed_out,
            "input_len": len(mutated_input),
        }

        return obs, reward, terminated, truncated, info

    def _get_observation(self, coverage_vector: np.ndarray) -> np.ndarray:
        """Build the 67-float observation vector."""
        obs = np.zeros(OBS_SIZE, dtype=np.float32)

        # Coverage buckets [0:64]
        obs[:64] = coverage_vector

        # Last action (normalized to [0, 1])
        obs[64] = self.last_action / max(NUM_ACTIONS - 1, 1)

        # Input length (normalized)
        obs[65] = min(len(self.current_input) / MAX_INPUT_LEN, 1.0)

        # Step count (normalized)
        obs[66] = min(self.step_count / self.max_steps, 1.0)

        return obs

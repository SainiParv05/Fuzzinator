"""
reward_engine.py
Fuzzinator — Reward Function

Simple reward system for RL-guided fuzzing:
  +10.0  for each new coverage edge
  +100.0 for a crash
  -0.1   if no new coverage
"""


class RewardEngine:
    """Computes rewards for the fuzzing RL agent."""

    # Reward constants
    NEW_EDGE_REWARD = 10.0
    CRASH_REWARD = 100.0
    NO_PROGRESS_PENALTY = -0.1

    def compute(self, new_edges: int, crashed: bool) -> float:
        """
        Compute the reward for a single fuzzing step.

        Args:
            new_edges: Number of newly discovered coverage edges
            crashed: Whether the target crashed

        Returns:
            Scalar reward value
        """
        reward = 0.0

        # Reward for new coverage
        if new_edges > 0:
            reward += self.NEW_EDGE_REWARD * new_edges
        else:
            reward += self.NO_PROGRESS_PENALTY

        # Bonus for crashes
        if crashed:
            reward += self.CRASH_REWARD

        return reward

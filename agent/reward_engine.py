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

    def __init__(self,
                 new_edge_reward: float = NEW_EDGE_REWARD,
                 crash_reward: float = CRASH_REWARD,
                 no_progress_penalty: float = NO_PROGRESS_PENALTY):
        if new_edge_reward <= 0:
            raise ValueError("new_edge_reward must be positive")
        if crash_reward < 0:
            raise ValueError("crash_reward must be non-negative")
        if no_progress_penalty > 0:
            raise ValueError("no_progress_penalty must be zero or negative")

        self.new_edge_reward = new_edge_reward
        self.crash_reward = crash_reward
        self.no_progress_penalty = no_progress_penalty

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
            reward += self.new_edge_reward * new_edges
        else:
            reward += self.no_progress_penalty

        # Bonus for crashes
        if crashed:
            reward += self.crash_reward

        return reward

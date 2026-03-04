"""
train.py
Fuzzinator — Main Training Loop

Runs the RL-guided fuzzing campaign:
  1. Load seed input
  2. Initialize PPO agent
  3. Run fuzzing environment
  4. Collect transitions into rollout buffer
  5. Update PPO policy every N steps
  6. Save checkpoints periodically

Usage:
    python agent/train.py
    python agent/train.py --target targets/target_maze
    python agent/train.py --steps 5000 --target targets/target_buffer_overflow
"""

import os
import sys
import argparse
import time
import numpy as np

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from agent.ppo_agent import PPOAgent
from agent.replay_buffer import RolloutBuffer
from environment.fuzz_env import FuzzEnv, OBS_SIZE
from mutator.mutator import NUM_ACTIONS, STRATEGY_NAMES


# ─── Configuration ───────────────────────────────────────────────

DEFAULT_TARGET = os.path.join(PROJECT_ROOT, "targets", "target_buffer_overflow")
DEFAULT_SEED = os.path.join(PROJECT_ROOT, "corpus", "seed.bin")
DEFAULT_CRASH_DIR = os.path.join(PROJECT_ROOT, "data", "crashes")
CHECKPOINT_DIR = os.path.join(PROJECT_ROOT, "data", "checkpoints")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fuzzinator — RL-Guided Fuzz Testing"
    )
    parser.add_argument("--target", type=str, default=DEFAULT_TARGET,
                        help="Path to target binary")
    parser.add_argument("--seed", type=str, default=DEFAULT_SEED,
                        help="Path to seed input file")
    parser.add_argument("--steps", type=int, default=2000,
                        help="Total fuzzing steps")
    parser.add_argument("--rollout-size", type=int, default=256,
                        help="Steps per rollout before PPO update")
    parser.add_argument("--lr", type=float, default=3e-4,
                        help="Learning rate")
    parser.add_argument("--checkpoint-interval", type=int, default=500,
                        help="Save checkpoint every N steps")
    return parser.parse_args()


def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ███████╗██╗   ██╗███████╗███████╗██╗███╗   ██╗ █████╗  ║
║   ██╔════╝██║   ██║╚══███╔╝╚══███╔╝██║████╗  ██║██╔══██╗ ║
║   █████╗  ██║   ██║  ███╔╝   ███╔╝ ██║██╔██╗ ██║███████║ ║
║   ██╔══╝  ██║   ██║ ███╔╝   ███╔╝  ██║██║╚██╗██║██╔══██║ ║
║   ██║     ╚██████╔╝███████╗███████╗██║██║ ╚████║██║  ██║  ║
║   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ║
║                                                          ║
║         Reinforcement Learning Guided Fuzz Testing       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def train(args):
    """Main training loop."""

    print_banner()

    print(f"[CONFIG] Target:        {args.target}")
    print(f"[CONFIG] Seed:          {args.seed}")
    print(f"[CONFIG] Total steps:   {args.steps}")
    print(f"[CONFIG] Rollout size:  {args.rollout_size}")
    print(f"[CONFIG] Learning rate: {args.lr}")
    print()

    # ─── Setup ────────────────────────────────────────────────

    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    os.makedirs(DEFAULT_CRASH_DIR, exist_ok=True)

    # Initialize environment
    env = FuzzEnv(
        target_path=args.target,
        seed_path=args.seed,
        crash_dir=DEFAULT_CRASH_DIR,
        max_steps=args.steps,
    )

    # Initialize PPO agent
    agent = PPOAgent(
        obs_size=OBS_SIZE,
        n_actions=NUM_ACTIONS,
        lr=args.lr,
    )

    # Initialize rollout buffer
    buffer = RolloutBuffer(
        buffer_size=args.rollout_size,
        obs_size=OBS_SIZE,
    )

    # ─── Training ─────────────────────────────────────────────

    print("=" * 60)
    print(" Starting Fuzzing Campaign")
    print("=" * 60)
    print()
    print(f"{'Step':>6} | {'Reward':>8} | {'New':>4} | {'Total':>6} | "
          f"{'Crashes':>7} | {'Action':>10} | {'Info'}")
    print("-" * 80)

    obs, _ = env.reset()
    total_reward = 0.0
    episode_rewards = []
    start_time = time.time()
    update_count = 0
    best_total_edges = 0
    best_total_crashes = 0

    try:
        for step in range(1, args.steps + 1):
            # Get action from PPO agent
            action, log_prob, value = agent.get_action(obs)

            # Step environment
            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            # Store transition
            buffer.store(obs, action, reward, log_prob, value, done)
            total_reward += reward

            # Track best stats (env resets clear these)
            best_total_edges = max(best_total_edges, info.get("total_edges", 0))
            best_total_crashes = max(best_total_crashes, info.get("total_crashes", 0))

            # Logging
            action_name = STRATEGY_NAMES.get(action, "unknown")
            crash_marker = ""
            if info["crashed"]:
                crash_marker = f"💥 CRASH ({info['signal']})"
                if info["crash_path"]:
                    crash_marker += f" → saved"

            if step % 10 == 0 or info["crashed"] or info["new_edges"] > 0:
                print(f"{step:>6} | {reward:>+8.1f} | {info['new_edges']:>4} | "
                      f"{info['total_edges']:>6} | {info['total_crashes']:>7} | "
                      f"{action_name:>10} | {crash_marker}")

            # PPO Update
            if buffer.full or done:
                last_value = agent.get_value(next_obs) if not done else 0.0
                buffer.compute_advantages(last_value)
                metrics = agent.update(buffer)
                buffer.reset()
                update_count += 1

                if update_count % 5 == 0:
                    print(f"       | {'[PPO UPDATE]':>8} | "
                          f"π_loss={metrics['policy_loss']:.4f} | "
                          f"v_loss={metrics['value_loss']:.4f} | "
                          f"entropy={metrics['entropy']:.4f}")

            # Checkpoint
            if step % args.checkpoint_interval == 0:
                ckpt_path = os.path.join(CHECKPOINT_DIR, f"ppo_step_{step}.pt")
                agent.save(ckpt_path)
                print(f"       | {'[SAVED]':>8} | checkpoint → {ckpt_path}")

            # Update state
            obs = next_obs

            if done:
                episode_rewards.append(total_reward)
                total_reward = 0.0
                obs, _ = env.reset()

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")

    # ─── Summary ──────────────────────────────────────────────

    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print(" Fuzzing Campaign Complete!")
    print("=" * 60)
    print(f"  Total steps:     {step}")
    print(f"  Total time:      {elapsed:.1f}s")
    print(f"  Exec speed:      {step / max(elapsed, 0.1):.1f} exec/sec")
    print(f"  Total edges:     {best_total_edges}")
    print(f"  Total crashes:   {best_total_crashes}")
    print(f"  PPO updates:     {update_count}")
    print(f"  Crash dir:       {DEFAULT_CRASH_DIR}")
    print()

    # Save final checkpoint
    final_path = os.path.join(CHECKPOINT_DIR, "ppo_final.pt")
    agent.save(final_path)
    print(f"  Final checkpoint: {final_path}")

    # List crashes
    if env.crash_vault.total_crashes > 0:
        print()
        print("  Crashes found:")
        for f in os.listdir(DEFAULT_CRASH_DIR):
            if f.startswith("crash_"):
                print(f"    • {f}")


if __name__ == "__main__":
    args = parse_args()
    train(args)

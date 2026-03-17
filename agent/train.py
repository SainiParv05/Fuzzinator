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
    python agent/train.py --config config/custom.yaml
"""

import os
import sys
import argparse
import time
import logging
import numpy as np

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from config import load_config
from config.logging_setup import setup_logging
from mutator.mutator import NUM_ACTIONS, STRATEGY_NAMES
from agent.reward_engine import RewardEngine
from agent.runtime_utils import set_random_seed


def validate_file_exists(filepath: str, description: str, logger: logging.Logger) -> bool:
    """
    Validate that a file exists.

    Args:
        filepath: Path to file to check
        description: Description of the file (for logging)
        logger: Logger instance

    Returns:
        True if file exists, False otherwise
    """
    if not os.path.isfile(filepath):
        logger.error(f"{description} not found: {filepath}")
        return False
    logger.debug(f"{description} validated: {filepath}")
    return True


def validate_binary_executable(filepath: str, logger: logging.Logger) -> bool:
    """
    Validate that a file is an executable binary.

    Args:
        filepath: Path to binary to check
        logger: Logger instance

    Returns:
        True if file is executable, False otherwise
    """
    if not os.path.isfile(filepath):
        logger.error(f"Binary not found: {filepath}")
        return False

    if not os.access(filepath, os.X_OK):
        logger.error(f"Binary is not executable: {filepath}")
        return False

    logger.debug(f"Binary validated: {filepath}")
    return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fuzzinator — RL-Guided Fuzz Testing"
    )
    parser.add_argument("--config", type=str, default=None,
                        help="Path to config YAML file (default: config/default.yaml)")
    parser.add_argument("--target", type=str, default=None,
                        help="Path to target binary (overrides config)")
    parser.add_argument("--seed", type=str, default=None,
                        help="Path to seed input file (overrides config)")
    parser.add_argument("--steps", type=int, default=None,
                        help="Total fuzzing steps (overrides config)")
    parser.add_argument("--rollout-size", type=int, default=None,
                        help="Steps per rollout before PPO update (overrides config)")
    parser.add_argument("--lr", type=float, default=None,
                        help="Learning rate (overrides config)")
    parser.add_argument("--checkpoint-interval", type=int, default=None,
                        help="Save checkpoint every N steps (overrides config)")
    parser.add_argument("--random-seed", type=int, default=None,
                        help="Random seed for reproducible training (overrides config)")
    parser.add_argument("--device", type=str, default=None,
                        help="Torch device: cpu, cuda, or auto (overrides config)")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose logging")
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

    # ─── Load Configuration ───────────────────────────────────

    try:
        config = load_config(args.config, PROJECT_ROOT)
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERROR] Failed to load configuration: {e}", file=sys.stderr)
        sys.exit(1)

    # ─── Setup Logging ────────────────────────────────────────

    # Override logging level if verbose
    if args.verbose:
        config.set("logging.level", "DEBUG")

    logger = setup_logging(config, "fuzzinator")
    logger.info("=" * 60)
    logger.info(" Fuzzinator — RL-Guided Fuzzing")
    logger.info("=" * 60)

    # ─── Apply CLI Overrides ──────────────────────────────────

    # Build effective configuration with CLI overrides
    target = args.target or config.get("environment.target_binary")
    seed = args.seed or config.get("environment.seed_file")
    steps = args.steps or config.get("environment.max_steps")
    rollout_size = args.rollout_size or config.get("fuzzing.buffer_size")
    lr = args.lr or config.get("agent.learning_rate")
    checkpoint_interval = args.checkpoint_interval or config.get("fuzzing.checkpoint_interval")
    random_seed = args.random_seed if args.random_seed is not None else config.get("fuzzing.random_seed")
    device = args.device or config.get("agent.device", "auto")
    timeout_ms = config.get("environment.timeout_ms")
    max_input_size = config.get("environment.max_input_size")
    new_edge_reward = config.get("fuzzing.new_edge_reward")
    crash_reward = config.get("fuzzing.crash_reward")
    timeout_penalty = config.get("fuzzing.timeout_penalty")
    ppo_epochs = config.get("agent.ppo_epochs", 4)
    entropy_coef = config.get("agent.entropy_coeff", 0.01)
    value_coef = config.get("agent.value_loss_coeff", 0.5)
    max_grad_norm = config.get("agent.max_grad_norm", 0.5)

    # Resolve paths relative to project root
    target = os.path.join(PROJECT_ROOT, target) if not os.path.isabs(target) else target
    seed = os.path.join(PROJECT_ROOT, seed) if not os.path.isabs(seed) else seed
    crash_dir = config.resolve_path("crash_dir")
    checkpoint_dir = config.resolve_path("checkpoint_dir")

    logger.info(f"Target binary: {target}")
    logger.info(f"Seed file: {seed}")
    logger.info(f"Total steps: {steps}")
    logger.info(f"Rollout size: {rollout_size}")
    logger.info(f"Learning rate: {lr}")
    logger.info(f"Random seed: {random_seed}")
    logger.info(f"Device: {device}")
    logger.info(f"Timeout: {timeout_ms}ms")
    logger.info(f"Max input size: {max_input_size}")
    logger.info(f"Checkpoint interval: {checkpoint_interval}")
    logger.info("")

    # ─── Input Validation ────────────────────────────────────

    logger.info("Validating inputs...")
    if not validate_binary_executable(target, logger):
        logger.error("Target binary validation failed. Exiting.")
        sys.exit(1)

    if not validate_file_exists(seed, "Seed file", logger):
        logger.error("Seed file validation failed. Exiting.")
        sys.exit(1)

    if steps <= 0:
        logger.error(f"Invalid steps: {steps} (must be positive)")
        sys.exit(1)

    if rollout_size <= 0:
        logger.error(f"Invalid rollout size: {rollout_size} (must be positive)")
        sys.exit(1)

    if lr <= 0:
        logger.error(f"Invalid learning rate: {lr} (must be positive)")
        sys.exit(1)

    if timeout_ms <= 0:
        logger.error(f"Invalid timeout: {timeout_ms}ms (must be positive)")
        sys.exit(1)

    if max_input_size <= 0:
        logger.error(f"Invalid max input size: {max_input_size} (must be positive)")
        sys.exit(1)

    if random_seed < 0:
        logger.error(f"Invalid random seed: {random_seed} (must be non-negative)")
        sys.exit(1)
    if device not in {"cpu", "cuda", "auto"}:
        logger.error(f"Invalid device: {device} (must be cpu, cuda, or auto)")
        sys.exit(1)

    logger.info("Input validation passed.")
    logger.info("")

    # ─── Setup ────────────────────────────────────────────────

    print_banner()
    logger.info(f"Creating output directories...")
    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(crash_dir, exist_ok=True)
    existing_crash_files = {
        filename for filename in os.listdir(crash_dir)
        if filename.startswith("crash_")
    }
    logger.debug(f"Checkpoint directory: {checkpoint_dir}")
    logger.debug(f"Crash directory: {crash_dir}")

    set_random_seed(random_seed)
    logger.info("Random generators seeded.")

    logger.info("Initializing fuzzing environment...")
    reward_engine = RewardEngine(
        new_edge_reward=new_edge_reward,
        crash_reward=crash_reward,
        no_progress_penalty=timeout_penalty,
    )

    try:
        from agent.ppo_agent import PPOAgent
        from agent.replay_buffer import RolloutBuffer
        from environment.fuzz_env import FuzzEnv, OBS_SIZE
    except ModuleNotFoundError as e:
        missing_module = getattr(e, "name", "unknown module")
        logger.error(
            "Missing dependency: %s. Install project requirements before running training.",
            missing_module
        )
        sys.exit(1)

    # Initialize environment
    env = FuzzEnv(
        target_path=target,
        seed_path=seed,
        crash_dir=crash_dir,
        max_steps=steps,
        timeout=timeout_ms / 1000.0,
        max_input_len=max_input_size,
        reward_engine=reward_engine,
    )

    logger.info("Initializing PPO agent...")
    # Initialize PPO agent
    agent = PPOAgent(
        obs_size=OBS_SIZE,
        n_actions=NUM_ACTIONS,
        lr=lr,
        entropy_coef=entropy_coef,
        value_coef=value_coef,
        max_grad_norm=max_grad_norm,
        ppo_epochs=ppo_epochs,
        device=device,
    )

    logger.info("Initializing rollout buffer...")
    # Initialize rollout buffer
    buffer = RolloutBuffer(
        buffer_size=rollout_size,
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

    logger.info("Starting training loop...")
    obs, _ = env.reset()
    total_reward = 0.0
    episode_rewards = []
    start_time = time.time()
    update_count = 0
    best_total_edges = 0
    best_total_crashes = 0

    try:
        for step in range(1, steps + 1):
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
                logger.warning(f"Crash detected: {info['signal']} (step {step})")

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
                    logger.debug(f"PPO update {update_count}: "
                                f"π_loss={metrics['policy_loss']:.4f}, "
                                f"v_loss={metrics['value_loss']:.4f}, "
                                f"entropy={metrics['entropy']:.4f}")
                    print(f"       | {'[PPO UPDATE]':>8} | "
                          f"π_loss={metrics['policy_loss']:.4f} | "
                          f"v_loss={metrics['value_loss']:.4f} | "
                          f"entropy={metrics['entropy']:.4f}")

            # Checkpoint
            if step % checkpoint_interval == 0:
                ckpt_path = os.path.join(checkpoint_dir, f"ppo_step_{step}.pt")
                agent.save(ckpt_path)
                logger.info(f"Checkpoint saved: {ckpt_path}")
                print(f"       | {'[SAVED]':>8} | checkpoint → {ckpt_path}")

            # Update state
            obs = next_obs

            if done:
                episode_rewards.append(total_reward)
                total_reward = 0.0
                obs, _ = env.reset()

    except KeyboardInterrupt:
        logger.warning("Training interrupted by user")
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
    print(f"  Crash dir:       {crash_dir}")
    print()

    logger.info("=" * 60)
    logger.info("Training complete!")
    logger.info(f"  Total steps: {step}")
    logger.info(f"  Total time: {elapsed:.1f}s")
    logger.info(f"  Exec speed: {step / max(elapsed, 0.1):.1f} exec/sec")
    logger.info(f"  Total edges: {best_total_edges}")
    logger.info(f"  Total crashes: {best_total_crashes}")

    # Save final checkpoint
    final_path = os.path.join(checkpoint_dir, "ppo_final.pt")
    agent.save(final_path)
    logger.info(f"Final checkpoint saved: {final_path}")
    print(f"  Final checkpoint: {final_path}")

    # List crashes
    new_crash_files = sorted(
        filename for filename in os.listdir(crash_dir)
        if filename.startswith("crash_") and filename not in existing_crash_files
    )
    if new_crash_files:
        print()
        print("  Crashes found:")
        logger.info(f"Found {len(new_crash_files)} new unique crashes:")
        for crash_file in new_crash_files:
            print(f"    • {crash_file}")
            logger.info(f"    • {crash_file}")


if __name__ == "__main__":
    args = parse_args()
    train(args)

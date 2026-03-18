"""
train_lstm.py
Fuzzinator — PPO+LSTM training loop for adaptive fuzzing.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from agent.ppo_agent_lstm import PPOAgentLSTM
from agent.replay_buffer_lstm import RolloutBufferLSTM
from agent.reward_engine import RewardEngine
from agent.run_report import write_run_report
from agent.runtime_utils import set_random_seed
from config import load_config
from config.logging_setup import setup_logging
from environment.fuzz_env import OBS_SIZE
from environment.fuzz_env_lstm import FuzzEnvLSTM
from mutator.mutator import NUM_ACTIONS, STRATEGY_NAMES


def validate_file_exists(filepath: str, description: str, logger: logging.Logger) -> bool:
    if not os.path.isfile(filepath):
        logger.error("%s not found: %s", description, filepath)
        return False
    return True


def validate_binary_executable(filepath: str, logger: logging.Logger) -> bool:
    if not os.path.isfile(filepath):
        logger.error("Binary not found: %s", filepath)
        return False
    if not os.access(filepath, os.X_OK):
        logger.error("Binary is not executable: %s", filepath)
        return False
    return True


def parse_args():
    parser = argparse.ArgumentParser(description="Fuzzinator — RL-Guided Fuzz Testing with PPO+LSTM")
    parser.add_argument("--config", type=str, default=None)
    parser.add_argument("--target", type=str, default=None)
    parser.add_argument("--seed", type=str, default=None)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--rollout-size", type=int, default=None)
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--checkpoint-interval", type=int, default=None)
    parser.add_argument("--random-seed", type=int, default=None)
    parser.add_argument("--lstm-hidden", type=int, default=None)
    parser.add_argument("--lstm-layers", type=int, default=None)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def train(args):
    config = load_config(args.config, PROJECT_ROOT)
    if args.verbose:
        config.set("logging.level", "DEBUG")

    logger = setup_logging(config, "fuzzinator.lstm")

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
    lstm_hidden = args.lstm_hidden or config.get("agent.lstm_hidden", 256)
    lstm_layers = args.lstm_layers or config.get("agent.lstm_layers", 2)

    target = os.path.join(PROJECT_ROOT, target) if not os.path.isabs(target) else target
    seed = os.path.join(PROJECT_ROOT, seed) if not os.path.isabs(seed) else seed
    crash_dir = config.resolve_path("crash_dir")
    checkpoint_dir = config.resolve_path("checkpoint_dir")
    report_dir = config.resolve_path("report_dir")

    logger.info("Target binary: %s", target)
    logger.info("Seed file: %s", seed)
    logger.info("Total steps: %s", steps)
    logger.info("Rollout size: %s", rollout_size)
    logger.info("Learning rate: %s", lr)
    logger.info("Random seed: %s", random_seed)
    logger.info("Device: %s", device)
    logger.info("Timeout: %sms", timeout_ms)
    logger.info("Max input size: %s", max_input_size)
    logger.info("LSTM hidden: %s", lstm_hidden)
    logger.info("LSTM layers: %s", lstm_layers)
    logger.info("Report directory: %s", report_dir)

    if not validate_binary_executable(target, logger):
        sys.exit(1)
    if not validate_file_exists(seed, "Seed file", logger):
        sys.exit(1)
    if random_seed < 0:
        logger.error("Random seed must be non-negative: %s", random_seed)
        sys.exit(1)
    if device not in {"cpu", "cuda", "auto"}:
        logger.error("Device must be cpu, cuda, or auto: %s", device)
        sys.exit(1)
    if lstm_hidden <= 0:
        logger.error("LSTM hidden size must be positive: %s", lstm_hidden)
        sys.exit(1)
    if lstm_layers <= 0:
        logger.error("LSTM layers must be positive: %s", lstm_layers)
        sys.exit(1)

    os.makedirs(checkpoint_dir, exist_ok=True)
    os.makedirs(crash_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    existing_crash_files = {
        filename for filename in os.listdir(crash_dir)
        if filename.startswith("crash_")
    }
    set_random_seed(random_seed)
    logger.info("Random generators seeded.")

    reward_engine = RewardEngine(
        new_edge_reward=new_edge_reward,
        crash_reward=crash_reward,
        no_progress_penalty=timeout_penalty,
    )

    env = FuzzEnvLSTM(
        target_path=target,
        seed_path=seed,
        crash_dir=crash_dir,
        max_steps=steps,
        timeout=timeout_ms / 1000.0,
        max_input_len=max_input_size,
        reward_engine=reward_engine,
    )

    agent = PPOAgentLSTM(
        obs_size=OBS_SIZE,
        n_actions=NUM_ACTIONS,
        lr=lr,
        entropy_coef=entropy_coef,
        value_coef=value_coef,
        max_grad_norm=max_grad_norm,
        ppo_epochs=ppo_epochs,
        lstm_hidden=lstm_hidden,
        lstm_layers=lstm_layers,
        device=device,
    )

    buffer = RolloutBufferLSTM(
        buffer_size=rollout_size,
        obs_size=OBS_SIZE,
        max_input_len=max_input_size,
    )

    print("=" * 60)
    print(" Starting Fuzzing Campaign (PPO+LSTM)")
    print("=" * 60)
    print()
    print(f"{'Step':>6} | {'Reward':>8} | {'New':>4} | {'Total':>6} | {'Crashes':>7} | {'Action':>10} | {'Info'}")
    print("-" * 80)

    obs, _ = env.reset()
    agent.reset_hidden_state()
    start_time = time.time()
    started_at = datetime.now().isoformat(timespec="seconds")
    total_reward = 0.0
    update_count = 0
    best_total_edges = 0
    best_total_crashes = 0
    status = "completed"
    events = []
    step = 0
    steps_since_last_edge = 0
    live_status_path = os.path.join(PROJECT_ROOT, "data", "live_status.json")

    try:
        while True:
            if steps > 0 and step >= steps:
                break
            step += 1
            current_input = env.get_current_input_array()
            current_history = env.action_history.copy()

            action, log_prob, value = agent.get_action(obs, current_input, current_history)
            next_obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            buffer.store(
                obs=obs,
                raw_input=current_input,
                action_history=current_history,
                action=action,
                reward=reward,
                log_prob=log_prob,
                value=value,
                done=done,
            )

            total_reward += reward
            best_total_edges = max(best_total_edges, info.get("total_edges", 0))
            best_total_crashes = max(best_total_crashes, info.get("total_crashes", 0))

            action_name = STRATEGY_NAMES.get(action, "unknown")
            crash_marker = ""
            if info["crashed"]:
                crash_marker = f"CRASH ({info['signal']})"
                events.append({
                    "step": step,
                    "type": "crash",
                    "signal": info["signal"],
                    "reward": round(reward, 3),
                    "total_crashes": info["total_crashes"],
                })

            if step % 10 == 0 or info["crashed"] or info["new_edges"] > 0:
                print(f"{step:>6} | {reward:>+8.1f} | {info['new_edges']:>4} | {info['total_edges']:>6} | "
                      f"{info['total_crashes']:>7} | {action_name:>10} | {crash_marker}")
            if info["new_edges"] > 0:
                steps_since_last_edge = 0
                events.append({
                    "step": step,
                    "type": "coverage_gain",
                    "new_edges": info["new_edges"],
                    "total_edges": info["total_edges"],
                    "action": action_name,
                })
            else:
                steps_since_last_edge += 1
                
            if steps <= 0 and steps_since_last_edge > 5000:
                print(f"[!] Auto-stopping: No new edges for 5000 steps.")
                break

            if step % 20 == 0:
                try:
                    with open(live_status_path, "w") as f:
                        json.dump({
                            "step": step,
                            "reward": round(total_reward, 3),
                            "edges": best_total_edges,
                            "crashes": best_total_crashes,
                            "bitmap": env.shared_coverage.tolist()[:512]
                        }, f)
                except Exception as e:
                    pass

            if buffer.full or done:
                if done:
                    last_value = 0.0
                else:
                    next_input = env.get_current_input_array()
                    next_history = env.action_history.copy()
                    last_value = agent.get_value(next_obs, next_input, next_history)

                buffer.compute_advantages(last_value)
                metrics = agent.update(buffer)
                buffer.reset()
                update_count += 1

                if update_count % 5 == 0:
                    print(f"       | {'[PPO UPDATE]':>8} | "
                          f"pi_loss={metrics['policy_loss']:.4f} | "
                          f"v_loss={metrics['value_loss']:.4f} | "
                          f"entropy={metrics['entropy']:.4f}")
                events.append({
                    "step": step,
                    "type": "ppo_update",
                    "update": update_count,
                    "policy_loss": round(metrics["policy_loss"], 4),
                    "value_loss": round(metrics["value_loss"], 4),
                    "entropy": round(metrics["entropy"], 4),
                })

            obs = next_obs
            if done:
                obs, _ = env.reset()
                agent.reset_hidden_state()

            if step % checkpoint_interval == 0:
                ckpt_path = os.path.join(checkpoint_dir, f"ppo_lstm_step_{step}.pt")
                agent.save(ckpt_path)
                print(f"       | {'[SAVED]':>8} | checkpoint -> {ckpt_path}")
                events.append({
                    "step": step,
                    "type": "checkpoint",
                    "path": ckpt_path,
                })

    except KeyboardInterrupt:
        status = "interrupted"
        print("\n[!] Interrupted by user")

    elapsed = time.time() - start_time
    final_path = os.path.join(checkpoint_dir, "ppo_lstm_final.pt")
    agent.save(final_path)

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
    print(f"  Final checkpoint: {final_path}")

    new_crash_files = sorted(
        filename for filename in os.listdir(crash_dir)
        if filename.startswith("crash_") and filename not in existing_crash_files
    )
    if new_crash_files:
        print()
        print("  Crashes found:")
        for crash_file in new_crash_files:
            print(f"    • {crash_file}")

    finished_at = datetime.now().isoformat(timespec="seconds")
    run_report = {
        "model": "PPO+LSTM",
        "status": status,
        "started_at": started_at,
        "finished_at": finished_at,
        "requested_steps": steps,
        "completed_steps": step,
        "completion_rule": "Run is done when completed_steps reaches requested_steps or the process is interrupted.",
        "target_path": target,
        "seed_path": seed,
        "target_name": os.path.basename(target),
        "config": {
            "rollout_size": rollout_size,
            "learning_rate": lr,
            "random_seed": random_seed,
            "device": device,
            "timeout_ms": timeout_ms,
            "max_input_size": max_input_size,
            "checkpoint_interval": checkpoint_interval,
            "lstm_hidden": lstm_hidden,
            "lstm_layers": lstm_layers,
        },
        "metrics": {
            "elapsed_seconds": round(elapsed, 3),
            "exec_speed": round(step / max(elapsed, 0.1), 3),
            "total_reward": round(total_reward, 3),
            "total_edges": best_total_edges,
            "total_crashes": best_total_crashes,
            "ppo_updates": update_count,
        },
        "events": events[:200],
        "new_crash_files": new_crash_files,
        "final_checkpoint": final_path,
        "crash_dir": crash_dir,
    }
    markdown_report_path, json_report_path = write_run_report(report_dir, run_report)
    run_report["markdown_report_path"] = markdown_report_path
    run_report["json_report_path"] = json_report_path
    markdown_report_path, json_report_path = write_run_report(report_dir, run_report)
    print(f"  Run report (md): {markdown_report_path}")
    print(f"  Run report (json): {json_report_path}")
    logger.info("Run report written: %s", markdown_report_path)
    logger.info("Run report written: %s", json_report_path)

    return {
        "steps": step,
        "elapsed": elapsed,
        "exec_speed": step / max(elapsed, 0.1),
        "total_edges": best_total_edges,
        "total_crashes": best_total_crashes,
        "ppo_updates": update_count,
        "checkpoint": final_path,
        "total_reward": total_reward,
        "report_markdown": markdown_report_path,
        "report_json": json_report_path,
    }


if __name__ == "__main__":
    train(parse_args())

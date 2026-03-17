#!/usr/bin/env python
"""Quick test of Phase 1 changes."""

import sys
import os
import logging
sys.path.insert(0, os.getcwd())

from config import load_config
from config.logging_setup import setup_logging
from agent.reward_engine import RewardEngine
from agent.runtime_utils import set_random_seed
from environment.execution_harness import ExecutionHarness

# Test 1: Config loading
print("=" * 60)
print("TEST 1: Config Loading")
print("=" * 60)

try:
    cfg = load_config(project_root=".")
    print("✓ Config loaded successfully")
    print(f"  Target: {cfg.get('environment.target_binary')}")
    print(f"  Seed: {cfg.get('environment.seed_file')}")
    print(f"  Max steps: {cfg.get('environment.max_steps')}")
    print(f"  Learning rate: {cfg.get('agent.learning_rate')}")
    print()
except Exception as e:
    print(f"✗ Config loading failed: {e}")
    sys.exit(1)

# Test 2: Logging setup
print("=" * 60)
print("TEST 2: Logging Setup")
print("=" * 60)

try:
    logger = setup_logging(cfg, "test_logger")
    logger.info("✓ Logging setup successful")
    logging.getLogger("environment.fuzz_env").info("Module logger propagation check")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    print()
except Exception as e:
    print(f"✗ Logging setup failed: {e}")
    sys.exit(1)

# Test 3: Path resolution
print("=" * 60)
print("TEST 3: Path Resolution")
print("=" * 60)

try:
    checkpoint_dir = cfg.resolve_path("checkpoint_dir")
    crash_dir = cfg.resolve_path("crash_dir")
    print(f"✓ Path resolution successful")
    print(f"  Checkpoint dir: {checkpoint_dir}")
    print(f"  Crash dir: {crash_dir}")
    print()
except Exception as e:
    print(f"✗ Path resolution failed: {e}")
    sys.exit(1)

# Test 3.5: Seed setup
print("=" * 60)
print("TEST 3.5: Seed Setup")
print("=" * 60)

try:
    set_random_seed(cfg.get("fuzzing.random_seed"))
    print(f"✓ Random seed configured: {cfg.get('fuzzing.random_seed')}")
    print()
except Exception as e:
    print(f"✗ Seed setup failed: {e}")
    sys.exit(1)

# Test 4: Security function
print("=" * 60)
print("TEST 4: Security Functions")
print("=" * 60)

try:
    from environment.crash_vault import _sanitize_signal_name
    
    test_signals = [
        "SIGSEGV",
        "SIGABRT(rc=1)",
        "SIG/PATH/TRAVERSAL",
        "SIG(../../../etc/passwd)",
    ]
    
    print("✓ Security function tests:")
    for sig in test_signals:
        sanitized = _sanitize_signal_name(sig)
        print(f"  {sig} → {sanitized}")
    print()
except Exception as e:
    print(f"✗ Security function test failed: {e}")
    sys.exit(1)

# Test 5: Reward engine config wiring
print("=" * 60)
print("TEST 5: Reward Engine")
print("=" * 60)

try:
    reward_engine = RewardEngine(
        new_edge_reward=cfg.get("fuzzing.new_edge_reward"),
        crash_reward=cfg.get("fuzzing.crash_reward"),
        no_progress_penalty=cfg.get("fuzzing.timeout_penalty"),
    )
    reward = reward_engine.compute(new_edges=2, crashed=True)
    print("✓ Reward engine wiring successful")
    print(f"  Reward for 2 edges + crash: {reward}")
    print()
except Exception as e:
    print(f"✗ Reward engine wiring failed: {e}")
    sys.exit(1)

# Test 6: Execution harness validation
print("=" * 60)
print("TEST 6: Execution Harness Validation")
print("=" * 60)

try:
    target_path = os.path.abspath(cfg.get("environment.target_binary"))
    harness = ExecutionHarness(target_path, timeout=cfg.get("environment.timeout_ms") / 1000.0)
    print("✓ Execution harness initialized successfully")
    print(f"  Target: {harness.target_path}")
    print(f"  Timeout: {harness.timeout}s")
    print()
except Exception as e:
    print(f"✗ Execution harness validation failed: {e}")
    sys.exit(1)

print("=" * 60)
print("PHASE 1 VERIFICATION: ALL TESTS PASSED ✓")
print("=" * 60)

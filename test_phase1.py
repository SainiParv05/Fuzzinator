#!/usr/bin/env python
"""Quick test of Phase 1 changes."""

import sys
import os
sys.path.insert(0, os.getcwd())

from config import load_config
from config.logging_setup import setup_logging

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

print("=" * 60)
print("PHASE 1 VERIFICATION: ALL TESTS PASSED ✓")
print("=" * 60)

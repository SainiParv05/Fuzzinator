#!/usr/bin/env python
"""Smoke tests for the PPO+LSTM implementation."""

import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.getcwd())

from agent.input_encoder import ActionSequenceEncoder, InputEncoder
from agent.ppo_agent_lstm import PPOAgentLSTM
from environment.fuzz_env import OBS_SIZE
from environment.fuzz_env_lstm import FuzzEnvLSTM


print("=" * 60)
print("TEST 1: Input Encoder Shapes")
print("=" * 60)
encoder = InputEncoder()
batch = torch.randint(0, 257, (4, 256))
encoded = encoder(batch)
print(f"✓ InputEncoder output shape: {tuple(encoded.shape)}")

action_encoder = ActionSequenceEncoder()
action_batch = torch.randint(0, 4, (4, 8))
action_encoded = action_encoder(action_batch)
print(f"✓ ActionSequenceEncoder output shape: {tuple(action_encoded.shape)}")
print()

print("=" * 60)
print("TEST 2: PPO+LSTM Action Selection")
print("=" * 60)
agent = PPOAgentLSTM(obs_size=OBS_SIZE)
obs = np.zeros(OBS_SIZE, dtype=np.float32)
raw_input = np.zeros(1024, dtype=np.int64)
action_history = np.zeros(8, dtype=np.int64)
action, log_prob, value = agent.get_action(obs, raw_input, action_history)
print(f"✓ Action: {action}")
print(f"✓ Log prob: {log_prob:.4f}")
print(f"✓ Value: {value:.4f}")
print()

print("=" * 60)
print("TEST 3: LSTM Environment Context")
print("=" * 60)
env = FuzzEnvLSTM(
    target_path="targets/target_buffer_overflow",
    seed_path="corpus/seed.bin",
    crash_dir="data/crashes",
    max_steps=5,
)
obs, info = env.reset()
print(f"✓ Reset obs shape: {obs.shape}")
print(f"✓ Raw input shape: {info['raw_input'].shape}")
print(f"✓ Action history shape: {info['action_history'].shape}")
next_obs, reward, terminated, truncated, info = env.step(1)
print(f"✓ Step obs shape: {next_obs.shape}")
print(f"✓ Updated action history tail: {info['action_history'][-1]}")
print()

print("=" * 60)
print("PHASE 2 VERIFICATION: ALL TESTS PASSED ✓")
print("=" * 60)

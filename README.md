# Fuzzinator — Reinforcement Learning Guided Fuzz Testing

<p align="center">
  <strong>An ML-guided fuzzer that uses PPO reinforcement learning to optimize mutation strategies</strong>
</p>

---

## Overview

Fuzzinator is a minimal proof-of-concept demonstrating how **reinforcement learning** can improve software fuzzing. Instead of randomly mutating inputs, a PPO (Proximal Policy Optimization) agent learns which mutation strategies are most effective at discovering new code paths and triggering crashes in target programs.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Training Loop                          │
│                                                             │
│   Seed Input                                                │
│       │                                                     │
│       ▼                                                     │
│   ┌──────────┐    action     ┌────────────────┐             │
│   │ PPO Agent │──────────────▶│    Mutator     │             │
│   │ (PyTorch) │              │  (4 strategies) │             │
│   └────▲─────┘              └───────┬────────┘             │
│        │                            │                       │
│        │ reward                     ▼ mutated input         │
│        │                   ┌─────────────────┐              │
│   ┌────┴──────┐           │  Exec Harness    │              │
│   │  Reward   │           │  (subprocess)    │              │
│   │  Engine   │           └────────┬─────────┘              │
│   └────▲──────┘                    │                        │
│        │                           ▼                        │
│        │ new_edges        ┌──────────────────┐              │
│        │ + crash          │ Coverage Reader   │              │
│        └──────────────────│ (shared memory)   │              │
│                           └────────┬─────────┘              │
│                                    │ crash?                  │
│                                    ▼                        │
│                           ┌──────────────────┐              │
│                           │  Crash Vault     │              │
│                           │ (data/crashes/)  │              │
│                           └──────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

## Components

| Component | File | Description |
|-----------|------|-------------|
| **PPO Agent** | `agent/ppo_agent.py` | Actor-Critic MLP network with clipped PPO |
| **Rollout Buffer** | `agent/replay_buffer.py` | Stores transitions, computes GAE advantages |
| **Reward Engine** | `agent/reward_engine.py` | +10 new edge, +100 crash, -0.1 no progress |
| **Training Loop** | `agent/train.py` | Main entry point for fuzzing campaigns |
| **Fuzz Environment** | `environment/fuzz_env.py` | Gymnasium env wrapping the fuzz loop |
| **Exec Harness** | `environment/execution_harness.py` | Runs targets via subprocess (50ms timeout) |
| **Coverage Reader** | `environment/coverage_reader.py` | Reads shared memory bitmap, tracks edges |
| **Crash Vault** | `environment/crash_vault.py` | Saves unique crashing inputs |
| **Mutator** | `mutator/mutator.py` | 4 strategies: bit_flip, byte_flip, byte_insert, havoc |

## Target Programs

| Target | Vulnerability | Crash Difficulty |
|--------|--------------|-----------------|
| `target_buffer_overflow` | Stack buffer overflow via `memcpy` | Easy |
| `target_format_string` | Format string via `printf(user_input)` | Medium |
| `target_maze` | Maze requiring specific byte sequence | Hard |

## Installation

### Prerequisites

- **Python 3.8+**
- **Clang** (for instrumenting targets)
- **Linux** (for shared memory and signal handling)

### Setup

```bash
# Clone or download the project
cd fuzzinator/

# Install Python dependencies
pip install -r requirements.txt

# Build the instrumented targets
bash instrumentation/build_target.sh
```

### Install Clang (if needed)

```bash
# Debian/Ubuntu/Kali
sudo apt install clang
```

## Usage

### Quick Start

```bash
# Build targets
bash instrumentation/build_target.sh

# Run the fuzzer (default: target_buffer_overflow, 2000 steps)
python agent/train.py
```

### Options

```bash
python agent/train.py --help

# Fuzz a specific target
python agent/train.py --target targets/target_maze

# Run more steps
python agent/train.py --steps 5000

# Change learning rate
python agent/train.py --lr 1e-3
```

### Example Output

```
═══════════════════════════════════════════════════════════
 Starting Fuzzing Campaign
═══════════════════════════════════════════════════════════

  Step |   Reward | New  | Total  | Crashes |     Action | Info
--------------------------------------------------------------------------------
    10 |    +10.0 |    1 |     12 |       0 |   bit_flip |
    20 |    -0.1  |    0 |     12 |       0 |      havoc |
    30 |    +20.0 |    2 |     14 |       0 |  byte_flip |
    42 |   +110.0 |    1 |     18 |       1 | byte_insert| 💥 CRASH (SIGSEGV) → saved
       | [PPO UPDATE] | π_loss=0.0234 | v_loss=0.1502 | entropy=1.3412
   ...

═══════════════════════════════════════════════════════════
 Fuzzing Campaign Complete!
═══════════════════════════════════════════════════════════
  Total steps:     2000
  Total time:      45.2s
  Exec speed:      44.2 exec/sec
  Total edges:     47
  Total crashes:   3
  Crash dir:       data/crashes/

  Crashes found:
    • crash_SIGSEGV_a1b2c3d4e5f6g7h8.bin
    • crash_ASAN_f8e7d6c5b4a39281.bin
```

## How It Works

1. **Seed Loading**: The fuzzer starts with an initial seed input (`corpus/seed.bin`)
2. **Mutation Selection**: The PPO agent observes the coverage state and selects one of 4 mutation strategies
3. **Input Mutation**: The selected strategy mutates the current input
4. **Target Execution**: The mutated input is fed to the instrumented target via subprocess
5. **Coverage Collection**: Edge coverage is read from the shared memory bitmap
6. **Reward Computation**: The agent receives rewards for new coverage (+10/edge) and crashes (+100)
7. **Policy Update**: Every N steps, PPO updates the policy using collected experience
8. **Crash Storage**: Crashing inputs are saved to `data/crashes/` for later analysis

## Observation Space

The RL agent receives a 67-dimensional observation vector:

| Index | Description |
|-------|-------------|
| 0–63 | Compressed coverage bitmap (64 buckets) |
| 64 | Last mutation action (normalized) |
| 65 | Current input length (normalized) |
| 66 | Step count (normalized) |

## Reward Function

| Event | Reward |
|-------|--------|
| New coverage edge | +10.0 per edge |
| Crash detected | +100.0 |
| No new coverage | -0.1 |

## Project Structure

```
fuzzinator/
├── agent/                    # RL agent
│   ├── ppo_agent.py          # PPO actor-critic network
│   ├── replay_buffer.py      # Rollout buffer with GAE
│   ├── reward_engine.py      # Reward computation
│   └── train.py              # Main training loop
├── environment/              # Fuzzing environment
│   ├── fuzz_env.py           # Gymnasium environment
│   ├── execution_harness.py  # Target execution
│   ├── coverage_reader.py    # Coverage bitmap reader
│   └── crash_vault.py        # Crash input storage
├── mutator/                  # Input mutations
│   └── mutator.py            # 4 mutation strategies
├── instrumentation/          # Build tools
│   ├── build_target.sh       # Target compilation script
│   └── shm_init.c            # Coverage instrumentation
├── targets/                  # Vulnerable programs
│   ├── target_buffer_overflow.c
│   ├── target_format_string.c
│   └── target_maze.c
├── corpus/                   # Seed inputs
│   └── seed.bin
├── data/                     # Output
│   ├── crashes/              # Crashing inputs
│   └── checkpoints/          # Model checkpoints
├── requirements.txt
└── README.md
```

## License

This project is for educational purposes — a college minor project demonstrating RL-guided fuzz testing.

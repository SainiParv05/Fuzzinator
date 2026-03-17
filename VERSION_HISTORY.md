# Fuzzinator Version History

This document tracks meaningful project updates, what changed, and the result of each update.

## Versioning Approach

- `v0.x.y` is used while the project is still in active prototype/research mode.
- `x` increases for major capability additions.
- `y` increases for smaller feature or stabilization updates.

## Update Template

Use this format for future work:

```md
## v0.x.y - YYYY-MM-DD

### What Changed
- Short list of code or architecture updates

### Files
- Main files added/updated

### Result
- Functional result
- Benchmark/test result
- Known tradeoff or risk
```

---

## v0.2.2 - 2026-03-17

### What Changed
- Added automatic per-run report generation for baseline PPO and PPO+LSTM training runs.
- Added a shared report writer that saves both markdown and JSON artifacts after each run.
- Added a dedicated report directory so run outputs are preserved independently from checkpoints and crashes.
- Made the run completion state explicit in the report with requested steps, completed steps, and completion rule.

### Files
- Added [agent/run_report.py](/home/kali/Fuzzi/Fuzzinator/agent/run_report.py)
- Updated [agent/train.py](/home/kali/Fuzzi/Fuzzinator/agent/train.py)
- Updated [agent/train_lstm.py](/home/kali/Fuzzi/Fuzzinator/agent/train_lstm.py)
- Updated [config/default.yaml](/home/kali/Fuzzi/Fuzzinator/config/default.yaml)

### Result
- Every completed run now writes:
- a markdown report in `data/reports/`
- a JSON report in `data/reports/`
- The console now prints the report paths at the end of the run.
- Run completion is now visible in three places:
- the final `Fuzzing Campaign Complete!` summary
- the printed report paths
- the `status`, `requested_steps`, and `completed_steps` fields inside the report

---

## v0.2.1 - 2026-03-17

### What Changed
- Added explicit random-seed support for reproducible PPO and PPO+LSTM experiments.
- Added device selection support to baseline training, LSTM training, and benchmark runs.
- Upgraded benchmark reporting to aggregate across multiple seeds and include per-seed results.
- Tuned the LSTM defaults based on multi-seed maze benchmarks.
- Added a dedicated tuning report documenting the tuning decision and remaining bottlenecks.

### Files
- Added [agent/runtime_utils.py](/home/kali/Fuzzi/Fuzzinator/agent/runtime_utils.py)
- Added [LSTM_TUNING_REPORT.md](/home/kali/Fuzzi/Fuzzinator/LSTM_TUNING_REPORT.md)
- Updated [agent/train.py](/home/kali/Fuzzi/Fuzzinator/agent/train.py)
- Updated [agent/train_lstm.py](/home/kali/Fuzzi/Fuzzinator/agent/train_lstm.py)
- Updated [agent/ppo_agent.py](/home/kali/Fuzzi/Fuzzinator/agent/ppo_agent.py)
- Updated [agent/ppo_agent_lstm.py](/home/kali/Fuzzi/Fuzzinator/agent/ppo_agent_lstm.py)
- Updated [benchmark_models.py](/home/kali/Fuzzi/Fuzzinator/benchmark_models.py)
- Updated [config/default.yaml](/home/kali/Fuzzi/Fuzzinator/config/default.yaml)
- Updated [config/__init__.py](/home/kali/Fuzzi/Fuzzinator/config/__init__.py)
- Updated [test_phase1.py](/home/kali/Fuzzi/Fuzzinator/test_phase1.py)
- Updated [BENCHMARK_REPORT.md](/home/kali/Fuzzi/Fuzzinator/BENCHMARK_REPORT.md)
- Updated [BENCHMARK_REPORT_TUNED_128x1.md](/home/kali/Fuzzi/Fuzzinator/BENCHMARK_REPORT_TUNED_128x1.md)

### Result
- Benchmarks are now reproducible and aggregated across seeds.
- Tuned default LSTM config is now `device=cpu`, `lstm_hidden=128`, `lstm_layers=1`.
- Multi-seed maze result:
- PPO baseline average: `129.0` edges at `81.233` exec/s
- PPO+LSTM `256x2` average: `127.667` edges at `0.467` exec/s
- PPO+LSTM `128x1` average: `139.667` edges at `0.467` exec/s
- Main conclusion: the lighter LSTM is a better default, but the real performance bottleneck is still the input encoding path.

---

## v0.2.0 - 2026-03-17

### What Changed
- Added PPO+LSTM training path to improve adaptability on sequence-sensitive targets.
- Added semantic raw-input encoding with embeddings, Conv1D, and BiLSTM.
- Added action-history encoding so the agent can learn mutation sequences.
- Added an LSTM-aware rollout buffer and environment context handling.
- Added baseline PPO vs PPO+LSTM benchmark automation and report generation.
- Added Phase 2 smoke tests for the new LSTM stack.

### Files
- Added [agent/input_encoder.py](/home/kali/Fuzzi/Fuzzinator/agent/input_encoder.py)
- Added [agent/ppo_agent_lstm.py](/home/kali/Fuzzi/Fuzzinator/agent/ppo_agent_lstm.py)
- Added [agent/replay_buffer_lstm.py](/home/kali/Fuzzi/Fuzzinator/agent/replay_buffer_lstm.py)
- Added [environment/fuzz_env_lstm.py](/home/kali/Fuzzi/Fuzzinator/environment/fuzz_env_lstm.py)
- Added [agent/train_lstm.py](/home/kali/Fuzzi/Fuzzinator/agent/train_lstm.py)
- Added [benchmark_models.py](/home/kali/Fuzzi/Fuzzinator/benchmark_models.py)
- Added [test_lstm_phase2.py](/home/kali/Fuzzi/Fuzzinator/test_lstm_phase2.py)
- Added [BENCHMARK_REPORT.md](/home/kali/Fuzzi/Fuzzinator/BENCHMARK_REPORT.md)
- Added [benchmark_results.json](/home/kali/Fuzzi/Fuzzinator/benchmark_results.json)
- Updated [config/default.yaml](/home/kali/Fuzzi/Fuzzinator/config/default.yaml)

### Result
- PPO+LSTM is now runnable through `./.venv/bin/python agent/train_lstm.py`.
- Benchmark comparison is now reproducible through `./.venv/bin/python benchmark_models.py --steps 60`.
- Smoke tests passed with `./.venv/bin/python test_lstm_phase2.py`.
- Short benchmark result:
- `target_buffer_overflow`: PPO `171` edges vs PPO+LSTM `172`
- `target_format_string`: PPO `221` edges / `16` crashes vs PPO+LSTM `222` edges / `4` crashes
- `target_maze`: PPO `172` edges vs PPO+LSTM `196`
- Main tradeoff: PPO+LSTM is currently much slower per step than baseline PPO.

---

## v0.1.1 - 2026-03-17

### What Changed
- Finished stabilization integration so config values drive the runtime instead of staying partially hardcoded.
- Wired reward values, timeout, max input size, PPO settings, and logging behavior into the active codepath.
- Improved logging setup so module-level loggers propagate correctly.
- Improved validation and Phase 1 verification coverage.
- Reduced noisy crash listing in baseline training output to only newly created crash files.

### Files
- Updated [agent/train.py](/home/kali/Fuzzi/Fuzzinator/agent/train.py)
- Updated [agent/reward_engine.py](/home/kali/Fuzzi/Fuzzinator/agent/reward_engine.py)
- Updated [environment/fuzz_env.py](/home/kali/Fuzzi/Fuzzinator/environment/fuzz_env.py)
- Updated [config/__init__.py](/home/kali/Fuzzi/Fuzzinator/config/__init__.py)
- Updated [config/logging_setup.py](/home/kali/Fuzzi/Fuzzinator/config/logging_setup.py)
- Updated [test_phase1.py](/home/kali/Fuzzi/Fuzzinator/test_phase1.py)

### Result
- Phase 1 stabilization became functionally integrated, not just documented.
- `python agent/train.py --help` works cleanly.
- `python agent/train.py --steps 1` now fails gracefully with a dependency message if `torch` is missing.
- Phase 1 verification passed with `python test_phase1.py`.

---

## v0.1.0 - 2026-03-17

### What Changed
- Introduced the first stabilization pass.
- Added configuration loading and YAML defaults.
- Added basic logging setup.
- Added input validation for seed files and target binaries.
- Added crash filename sanitization and safer crash output handling.

### Files
- Added [config/default.yaml](/home/kali/Fuzzi/Fuzzinator/config/default.yaml)
- Added [config/__init__.py](/home/kali/Fuzzi/Fuzzinator/config/__init__.py)
- Added [config/logging_setup.py](/home/kali/Fuzzi/Fuzzinator/config/logging_setup.py)
- Updated [agent/train.py](/home/kali/Fuzzi/Fuzzinator/agent/train.py)
- Updated [environment/crash_vault.py](/home/kali/Fuzzi/Fuzzinator/environment/crash_vault.py)
- Updated [environment/execution_harness.py](/home/kali/Fuzzi/Fuzzinator/environment/execution_harness.py)
- Updated [environment/fuzz_env.py](/home/kali/Fuzzi/Fuzzinator/environment/fuzz_env.py)
- Added [test_phase1.py](/home/kali/Fuzzi/Fuzzinator/test_phase1.py)

### Result
- The project moved from a purely hardcoded prototype toward a configurable training system.
- Stabilization groundwork was introduced and later completed in `v0.1.1`.

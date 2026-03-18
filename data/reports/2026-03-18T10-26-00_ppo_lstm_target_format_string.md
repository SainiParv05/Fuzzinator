# Run Report: PPO+LSTM

Started: 2026-03-18T10:26:00
Finished: 2026-03-18T10:26:28
Status: `completed`

## Completion

- Requested steps: `200`
- Completed steps: `200`
- Completion rule: `Run is done when completed_steps reaches requested_steps or the process is interrupted.`

## Target

- Target binary: `/home/kali/Fuzzi/Fuzzinator/targets/target_format_string`
- Seed file: `/home/kali/Fuzzi/Fuzzinator/corpus/seed.bin`
- Target name: `target_format_string`

## Configuration

- rollout_size: `256`
- learning_rate: `0.0003`
- random_seed: `1337`
- device: `cpu`
- timeout_ms: `500`
- max_input_size: `1024`
- checkpoint_interval: `500`
- lstm_hidden: `128`
- lstm_layers: `1`

## Final Metrics

- elapsed_seconds: `28.697`
- exec_speed: `6.969`
- total_reward: `3474.7`
- total_edges: `249`
- total_crashes: `9`
- ppo_updates: `1`

## Crashes Created In This Run

- `crash_SIGABRT_186172923aedad94.bin`
- `crash_SIGABRT_3de536e243493008.bin`
- `crash_SIGABRT_3eef8322d9b8d75b.bin`
- `crash_SIGABRT_a95b1194a3df8cc7.bin`
- `crash_SIGABRT_b9ee24bd827d0b36.bin`
- `crash_SIGABRT_befb9f2aa294177a.bin`
- `crash_SIGABRT_e94de9ca2210bb3c.bin`
- `crash_SIGABRT_f7aa9b78143c0c5a.bin`
- `crash_SIGABRT_fca1204fb37ac782.bin`

## Notable Events

- step=1, type=crash, signal=SIGABRT, reward=160.0, total_crashes=1
- step=1, type=coverage_gain, new_edges=6, total_edges=6, action=bit_flip
- step=2, type=crash, signal=SIGABRT, reward=160.0, total_crashes=2
- step=2, type=coverage_gain, new_edges=6, total_edges=12, action=byte_flip
- step=3, type=crash, signal=SIGABRT, reward=160.0, total_crashes=2
- step=3, type=coverage_gain, new_edges=6, total_edges=18, action=byte_flip
- step=4, type=crash, signal=SIGABRT, reward=160.0, total_crashes=3
- step=4, type=coverage_gain, new_edges=6, total_edges=24, action=byte_flip
- step=5, type=crash, signal=SIGABRT, reward=150.0, total_crashes=4
- step=5, type=coverage_gain, new_edges=5, total_edges=29, action=byte_insert
- step=6, type=crash, signal=SIGABRT, reward=160.0, total_crashes=5
- step=6, type=coverage_gain, new_edges=6, total_edges=35, action=byte_insert
- step=7, type=crash, signal=SIGABRT, reward=99.9, total_crashes=6
- step=8, type=crash, signal=SIGABRT, reward=150.0, total_crashes=7
- step=8, type=coverage_gain, new_edges=5, total_edges=40, action=byte_insert
- step=9, type=crash, signal=SIGABRT, reward=99.9, total_crashes=8
- step=10, type=crash, signal=SIGABRT, reward=160.0, total_crashes=9
- step=10, type=coverage_gain, new_edges=6, total_edges=46, action=byte_flip
- step=11, type=coverage_gain, new_edges=8, total_edges=54, action=havoc
- step=12, type=coverage_gain, new_edges=2, total_edges=56, action=havoc
- step=13, type=coverage_gain, new_edges=2, total_edges=58, action=havoc
- step=14, type=coverage_gain, new_edges=8, total_edges=66, action=bit_flip
- step=15, type=coverage_gain, new_edges=8, total_edges=74, action=bit_flip
- step=17, type=coverage_gain, new_edges=8, total_edges=82, action=bit_flip
- step=18, type=coverage_gain, new_edges=8, total_edges=90, action=bit_flip
- step=19, type=coverage_gain, new_edges=2, total_edges=92, action=byte_flip
- step=20, type=coverage_gain, new_edges=7, total_edges=99, action=byte_insert
- step=22, type=coverage_gain, new_edges=7, total_edges=106, action=havoc
- step=23, type=coverage_gain, new_edges=2, total_edges=108, action=bit_flip
- step=24, type=coverage_gain, new_edges=7, total_edges=115, action=byte_flip
- step=25, type=coverage_gain, new_edges=8, total_edges=123, action=byte_insert
- step=26, type=coverage_gain, new_edges=2, total_edges=125, action=bit_flip
- step=27, type=coverage_gain, new_edges=2, total_edges=127, action=bit_flip
- step=29, type=coverage_gain, new_edges=8, total_edges=135, action=byte_flip
- step=30, type=coverage_gain, new_edges=2, total_edges=137, action=byte_flip
- step=32, type=coverage_gain, new_edges=8, total_edges=145, action=bit_flip
- step=33, type=coverage_gain, new_edges=8, total_edges=153, action=bit_flip
- step=34, type=coverage_gain, new_edges=8, total_edges=161, action=havoc
- step=35, type=coverage_gain, new_edges=7, total_edges=168, action=havoc
- step=37, type=coverage_gain, new_edges=2, total_edges=170, action=byte_flip
- step=39, type=coverage_gain, new_edges=7, total_edges=177, action=byte_insert
- step=41, type=coverage_gain, new_edges=7, total_edges=184, action=havoc
- step=42, type=coverage_gain, new_edges=2, total_edges=186, action=bit_flip
- step=43, type=coverage_gain, new_edges=2, total_edges=188, action=bit_flip
- step=45, type=coverage_gain, new_edges=7, total_edges=195, action=havoc
- step=46, type=coverage_gain, new_edges=7, total_edges=202, action=havoc
- step=49, type=coverage_gain, new_edges=2, total_edges=204, action=byte_flip
- step=52, type=coverage_gain, new_edges=7, total_edges=211, action=byte_flip
- step=53, type=coverage_gain, new_edges=2, total_edges=213, action=byte_insert
- step=54, type=coverage_gain, new_edges=7, total_edges=220, action=byte_flip
- step=58, type=coverage_gain, new_edges=7, total_edges=227, action=byte_insert
- step=61, type=coverage_gain, new_edges=2, total_edges=229, action=byte_flip
- step=65, type=coverage_gain, new_edges=2, total_edges=231, action=byte_flip
- step=67, type=coverage_gain, new_edges=2, total_edges=233, action=havoc
- step=76, type=coverage_gain, new_edges=7, total_edges=240, action=havoc
- step=88, type=coverage_gain, new_edges=2, total_edges=242, action=havoc
- step=136, type=coverage_gain, new_edges=7, total_edges=249, action=havoc
- step=200, type=ppo_update, update=1, policy_loss=0.0003, value_loss=111348.6183, entropy=1.3841

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T10-26-00_ppo_lstm_target_format_string.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T10-26-00_ppo_lstm_target_format_string.json`

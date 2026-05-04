# Run Report: PPO+LSTM

Started: 2026-05-04T17:13:50
Finished: 2026-05-04T17:13:51
Status: `completed`

## Completion

- Requested steps: `200`
- Completed steps: `44`
- Completion rule: `Run is done when completed_steps reaches requested_steps or the process is interrupted.`

## Target

- Target binary: `/home/kali/Fuzzi/Fuzzinator/targets/target_buffer_overflow`
- Seed file: `/home/kali/Fuzzi/Fuzzinator/corpus/seed.bin`
- Target name: `target_buffer_overflow`

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

- elapsed_seconds: `1.858`
- exec_speed: `23.686`
- total_reward: `1958.6`
- total_edges: `186`
- total_crashes: `1`
- ppo_updates: `0`

## Crashes Created In This Run

- `crash_SIGABRT_2edf5883aa2d1061.bin`

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=bit_flip
- step=2, type=coverage_gain, new_edges=7, total_edges=14, action=byte_flip
- step=3, type=coverage_gain, new_edges=7, total_edges=21, action=byte_flip
- step=4, type=coverage_gain, new_edges=7, total_edges=28, action=byte_flip
- step=5, type=coverage_gain, new_edges=7, total_edges=35, action=byte_insert
- step=6, type=coverage_gain, new_edges=6, total_edges=41, action=byte_insert
- step=7, type=coverage_gain, new_edges=7, total_edges=48, action=byte_insert
- step=8, type=coverage_gain, new_edges=7, total_edges=55, action=byte_insert
- step=9, type=coverage_gain, new_edges=6, total_edges=61, action=byte_insert
- step=11, type=coverage_gain, new_edges=7, total_edges=68, action=havoc
- step=12, type=coverage_gain, new_edges=7, total_edges=75, action=havoc
- step=13, type=coverage_gain, new_edges=6, total_edges=81, action=havoc
- step=14, type=coverage_gain, new_edges=6, total_edges=87, action=bit_flip
- step=16, type=coverage_gain, new_edges=7, total_edges=94, action=byte_insert
- step=18, type=coverage_gain, new_edges=7, total_edges=101, action=bit_flip
- step=19, type=coverage_gain, new_edges=7, total_edges=108, action=byte_flip
- step=20, type=coverage_gain, new_edges=7, total_edges=115, action=byte_insert
- step=21, type=coverage_gain, new_edges=6, total_edges=121, action=byte_flip
- step=23, type=coverage_gain, new_edges=6, total_edges=127, action=bit_flip
- step=24, type=coverage_gain, new_edges=6, total_edges=133, action=byte_flip
- step=26, type=coverage_gain, new_edges=7, total_edges=140, action=bit_flip
- step=28, type=coverage_gain, new_edges=7, total_edges=147, action=bit_flip
- step=31, type=coverage_gain, new_edges=6, total_edges=153, action=byte_insert
- step=33, type=coverage_gain, new_edges=6, total_edges=159, action=bit_flip
- step=35, type=coverage_gain, new_edges=6, total_edges=165, action=havoc
- step=38, type=coverage_gain, new_edges=6, total_edges=171, action=byte_insert
- step=41, type=coverage_gain, new_edges=2, total_edges=173, action=havoc
- step=42, type=coverage_gain, new_edges=7, total_edges=180, action=bit_flip
- step=43, type=coverage_gain, new_edges=2, total_edges=182, action=bit_flip
- step=44, type=crash, signal=SIGABRT, reward=140.0, total_crashes=1
- step=44, type=coverage_gain, new_edges=4, total_edges=186, action=havoc

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-05-04T17-13-50_ppo_lstm_target_buffer_overflow.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-05-04T17-13-50_ppo_lstm_target_buffer_overflow.json`

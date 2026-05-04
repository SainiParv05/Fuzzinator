# Run Report: PPO+LSTM

Started: 2026-05-04T17:15:27
Finished: 2026-05-04T17:15:27
Status: `completed`

## Completion

- Requested steps: `-1`
- Completed steps: `1`
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

- elapsed_seconds: `0.05`
- exec_speed: `10.0`
- total_reward: `140.0`
- total_edges: `4`
- total_crashes: `1`
- ppo_updates: `0`

## Crashes Created In This Run

- `crash_ASANrc1_98985585fbee009a.bin`

## Notable Events

- step=1, type=crash, signal=ASAN(rc=1), reward=140.0, total_crashes=1
- step=1, type=coverage_gain, new_edges=4, total_edges=4, action=bit_flip

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-05-04T17-15-27_ppo_lstm_target_format_string.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-05-04T17-15-27_ppo_lstm_target_format_string.json`

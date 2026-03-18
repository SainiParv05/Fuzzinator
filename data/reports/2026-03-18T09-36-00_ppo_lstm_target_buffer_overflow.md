# Run Report: PPO+LSTM

Started: 2026-03-18T09:36:00
Finished: 2026-03-18T09:36:03
Status: `completed`

## Completion

- Requested steps: `20`
- Completed steps: `20`
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

- elapsed_seconds: `3.173`
- exec_speed: `6.303`
- total_reward: `1259.9`
- total_edges: `126`
- total_crashes: `0`
- ppo_updates: `1`

## Crashes Created In This Run

- None

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=bit_flip
- step=2, type=coverage_gain, new_edges=7, total_edges=14, action=byte_flip
- step=3, type=coverage_gain, new_edges=7, total_edges=21, action=byte_flip
- step=4, type=coverage_gain, new_edges=7, total_edges=28, action=byte_flip
- step=5, type=coverage_gain, new_edges=7, total_edges=35, action=byte_insert
- step=6, type=coverage_gain, new_edges=7, total_edges=42, action=byte_insert
- step=7, type=coverage_gain, new_edges=7, total_edges=49, action=byte_insert
- step=9, type=coverage_gain, new_edges=6, total_edges=55, action=byte_insert
- step=10, type=coverage_gain, new_edges=7, total_edges=62, action=byte_flip
- step=11, type=coverage_gain, new_edges=6, total_edges=68, action=havoc
- step=12, type=coverage_gain, new_edges=6, total_edges=74, action=havoc
- step=13, type=coverage_gain, new_edges=7, total_edges=81, action=havoc
- step=14, type=coverage_gain, new_edges=6, total_edges=87, action=bit_flip
- step=15, type=coverage_gain, new_edges=6, total_edges=93, action=bit_flip
- step=16, type=coverage_gain, new_edges=7, total_edges=100, action=byte_insert
- step=17, type=coverage_gain, new_edges=6, total_edges=106, action=bit_flip
- step=18, type=coverage_gain, new_edges=7, total_edges=113, action=bit_flip
- step=19, type=coverage_gain, new_edges=7, total_edges=120, action=byte_flip
- step=20, type=coverage_gain, new_edges=6, total_edges=126, action=byte_insert
- step=20, type=ppo_update, update=1, policy_loss=-0.0006, value_loss=227227.1719, entropy=1.3849

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T09-36-00_ppo_lstm_target_buffer_overflow.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T09-36-00_ppo_lstm_target_buffer_overflow.json`

# Run Report: PPO+LSTM

Started: 2026-03-18T19:24:19
Finished: 2026-03-18T19:24:50
Status: `completed`

## Completion

- Requested steps: `200`
- Completed steps: `200`
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

- elapsed_seconds: `31.181`
- exec_speed: `6.414`
- total_reward: `2063.2`
- total_edges: `208`
- total_crashes: `0`
- ppo_updates: `1`

## Crashes Created In This Run

- None

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=bit_flip
- step=2, type=coverage_gain, new_edges=7, total_edges=14, action=byte_flip
- step=3, type=coverage_gain, new_edges=6, total_edges=20, action=byte_flip
- step=4, type=coverage_gain, new_edges=7, total_edges=27, action=byte_flip
- step=5, type=coverage_gain, new_edges=7, total_edges=34, action=byte_insert
- step=6, type=coverage_gain, new_edges=7, total_edges=41, action=byte_insert
- step=7, type=coverage_gain, new_edges=7, total_edges=48, action=byte_insert
- step=8, type=coverage_gain, new_edges=7, total_edges=55, action=byte_insert
- step=9, type=coverage_gain, new_edges=7, total_edges=62, action=byte_insert
- step=11, type=coverage_gain, new_edges=7, total_edges=69, action=havoc
- step=12, type=coverage_gain, new_edges=6, total_edges=75, action=havoc
- step=14, type=coverage_gain, new_edges=6, total_edges=81, action=bit_flip
- step=15, type=coverage_gain, new_edges=7, total_edges=88, action=bit_flip
- step=16, type=coverage_gain, new_edges=7, total_edges=95, action=byte_insert
- step=18, type=coverage_gain, new_edges=6, total_edges=101, action=bit_flip
- step=20, type=coverage_gain, new_edges=7, total_edges=108, action=byte_insert
- step=21, type=coverage_gain, new_edges=6, total_edges=114, action=byte_flip
- step=24, type=coverage_gain, new_edges=7, total_edges=121, action=byte_flip
- step=25, type=coverage_gain, new_edges=6, total_edges=127, action=byte_insert
- step=26, type=coverage_gain, new_edges=7, total_edges=134, action=bit_flip
- step=27, type=coverage_gain, new_edges=6, total_edges=140, action=bit_flip
- step=28, type=coverage_gain, new_edges=7, total_edges=147, action=bit_flip
- step=29, type=coverage_gain, new_edges=6, total_edges=153, action=byte_flip
- step=32, type=coverage_gain, new_edges=7, total_edges=160, action=bit_flip
- step=37, type=coverage_gain, new_edges=6, total_edges=166, action=byte_flip
- step=46, type=coverage_gain, new_edges=6, total_edges=172, action=havoc
- step=47, type=coverage_gain, new_edges=6, total_edges=178, action=byte_insert
- step=54, type=coverage_gain, new_edges=6, total_edges=184, action=byte_flip
- step=60, type=coverage_gain, new_edges=6, total_edges=190, action=byte_insert
- step=62, type=coverage_gain, new_edges=6, total_edges=196, action=byte_flip
- step=71, type=coverage_gain, new_edges=6, total_edges=202, action=byte_flip
- step=85, type=coverage_gain, new_edges=6, total_edges=208, action=byte_insert
- step=200, type=ppo_update, update=1, policy_loss=-0.0012, value_loss=46144.739, entropy=1.3842

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T19-24-19_ppo_lstm_target_buffer_overflow.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T19-24-19_ppo_lstm_target_buffer_overflow.json`

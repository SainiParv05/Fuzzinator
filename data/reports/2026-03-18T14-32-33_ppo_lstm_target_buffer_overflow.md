# Run Report: PPO+LSTM

Started: 2026-03-18T14:32:33
Finished: 2026-03-18T14:33:52
Status: `completed`

## Completion

- Requested steps: `500`
- Completed steps: `500`
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

- elapsed_seconds: `78.53`
- exec_speed: `6.367`
- total_reward: `2033.2`
- total_edges: `208`
- total_crashes: `0`
- ppo_updates: `2`

## Crashes Created In This Run

- None

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=bit_flip
- step=2, type=coverage_gain, new_edges=7, total_edges=14, action=byte_flip
- step=3, type=coverage_gain, new_edges=7, total_edges=21, action=byte_flip
- step=4, type=coverage_gain, new_edges=7, total_edges=28, action=byte_flip
- step=5, type=coverage_gain, new_edges=7, total_edges=35, action=byte_insert
- step=6, type=coverage_gain, new_edges=6, total_edges=41, action=byte_insert
- step=7, type=coverage_gain, new_edges=7, total_edges=48, action=byte_insert
- step=8, type=coverage_gain, new_edges=7, total_edges=55, action=byte_insert
- step=9, type=coverage_gain, new_edges=7, total_edges=62, action=byte_insert
- step=10, type=coverage_gain, new_edges=6, total_edges=68, action=byte_flip
- step=13, type=coverage_gain, new_edges=7, total_edges=75, action=havoc
- step=14, type=coverage_gain, new_edges=7, total_edges=82, action=bit_flip
- step=15, type=coverage_gain, new_edges=7, total_edges=89, action=bit_flip
- step=17, type=coverage_gain, new_edges=6, total_edges=95, action=bit_flip
- step=20, type=coverage_gain, new_edges=6, total_edges=101, action=byte_insert
- step=21, type=coverage_gain, new_edges=7, total_edges=108, action=byte_flip
- step=24, type=coverage_gain, new_edges=6, total_edges=114, action=byte_flip
- step=26, type=coverage_gain, new_edges=6, total_edges=120, action=bit_flip
- step=29, type=coverage_gain, new_edges=7, total_edges=127, action=byte_flip
- step=31, type=coverage_gain, new_edges=7, total_edges=134, action=byte_insert
- step=33, type=coverage_gain, new_edges=6, total_edges=140, action=bit_flip
- step=34, type=coverage_gain, new_edges=7, total_edges=147, action=havoc
- step=38, type=coverage_gain, new_edges=6, total_edges=153, action=byte_insert
- step=40, type=coverage_gain, new_edges=6, total_edges=159, action=byte_insert
- step=42, type=coverage_gain, new_edges=6, total_edges=165, action=bit_flip
- step=47, type=coverage_gain, new_edges=6, total_edges=171, action=byte_insert
- step=48, type=coverage_gain, new_edges=6, total_edges=177, action=byte_flip
- step=49, type=coverage_gain, new_edges=6, total_edges=183, action=byte_flip
- step=69, type=coverage_gain, new_edges=6, total_edges=189, action=byte_flip
- step=75, type=coverage_gain, new_edges=7, total_edges=196, action=havoc
- step=113, type=coverage_gain, new_edges=6, total_edges=202, action=byte_insert
- step=126, type=coverage_gain, new_edges=6, total_edges=208, action=byte_insert
- step=256, type=ppo_update, update=1, policy_loss=-0.0027, value_loss=34889.7894, entropy=1.3841
- step=500, type=ppo_update, update=2, policy_loss=-0.0085, value_loss=1.9071, entropy=1.3845
- step=500, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_500.pt

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T14-32-33_ppo_lstm_target_buffer_overflow.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T14-32-33_ppo_lstm_target_buffer_overflow.json`

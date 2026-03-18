# Run Report: PPO+LSTM

Started: 2026-03-18T17:43:34
Finished: 2026-03-18T17:44:06
Status: `completed`

## Completion

- Requested steps: `200`
- Completed steps: `200`
- Completion rule: `Run is done when completed_steps reaches requested_steps or the process is interrupted.`

## Target

- Target binary: `/home/kali/Fuzzi/Fuzzinator/targets/target_dashboard_smoke`
- Seed file: `/home/kali/Fuzzi/Fuzzinator/corpus/seed.bin`
- Target name: `target_dashboard_smoke`

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

- elapsed_seconds: `31.745`
- exec_speed: `6.3`
- total_reward: `2063.2`
- total_edges: `208`
- total_crashes: `0`
- ppo_updates: `1`

## Crashes Created In This Run

- None

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=bit_flip
- step=2, type=coverage_gain, new_edges=7, total_edges=14, action=byte_flip
- step=3, type=coverage_gain, new_edges=7, total_edges=21, action=byte_flip
- step=6, type=coverage_gain, new_edges=7, total_edges=28, action=byte_insert
- step=7, type=coverage_gain, new_edges=7, total_edges=35, action=byte_insert
- step=8, type=coverage_gain, new_edges=6, total_edges=41, action=byte_insert
- step=9, type=coverage_gain, new_edges=7, total_edges=48, action=byte_insert
- step=10, type=coverage_gain, new_edges=7, total_edges=55, action=byte_flip
- step=12, type=coverage_gain, new_edges=7, total_edges=62, action=havoc
- step=13, type=coverage_gain, new_edges=7, total_edges=69, action=havoc
- step=14, type=coverage_gain, new_edges=7, total_edges=76, action=bit_flip
- step=15, type=coverage_gain, new_edges=6, total_edges=82, action=bit_flip
- step=16, type=coverage_gain, new_edges=6, total_edges=88, action=byte_insert
- step=19, type=coverage_gain, new_edges=7, total_edges=95, action=byte_flip
- step=27, type=coverage_gain, new_edges=7, total_edges=102, action=bit_flip
- step=29, type=coverage_gain, new_edges=7, total_edges=109, action=byte_flip
- step=30, type=coverage_gain, new_edges=7, total_edges=116, action=byte_flip
- step=32, type=coverage_gain, new_edges=6, total_edges=122, action=bit_flip
- step=35, type=coverage_gain, new_edges=7, total_edges=129, action=havoc
- step=36, type=coverage_gain, new_edges=6, total_edges=135, action=bit_flip
- step=40, type=coverage_gain, new_edges=6, total_edges=141, action=byte_insert
- step=42, type=coverage_gain, new_edges=6, total_edges=147, action=bit_flip
- step=48, type=coverage_gain, new_edges=6, total_edges=153, action=byte_flip
- step=49, type=coverage_gain, new_edges=6, total_edges=159, action=byte_flip
- step=59, type=coverage_gain, new_edges=7, total_edges=166, action=byte_insert
- step=62, type=coverage_gain, new_edges=6, total_edges=172, action=byte_flip
- step=65, type=coverage_gain, new_edges=6, total_edges=178, action=byte_flip
- step=66, type=coverage_gain, new_edges=6, total_edges=184, action=byte_flip
- step=67, type=coverage_gain, new_edges=6, total_edges=190, action=havoc
- step=74, type=coverage_gain, new_edges=6, total_edges=196, action=havoc
- step=136, type=coverage_gain, new_edges=6, total_edges=202, action=havoc
- step=158, type=coverage_gain, new_edges=6, total_edges=208, action=bit_flip
- step=200, type=ppo_update, update=1, policy_loss=-0.0025, value_loss=39892.0956, entropy=1.384

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T17-43-34_ppo_lstm_target_dashboard_smoke.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T17-43-34_ppo_lstm_target_dashboard_smoke.json`

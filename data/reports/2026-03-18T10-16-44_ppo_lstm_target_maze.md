# Run Report: PPO+LSTM

Started: 2026-03-18T10:16:44
Finished: 2026-03-18T10:20:46
Status: `completed`

## Completion

- Requested steps: `1000`
- Completed steps: `1000`
- Completion rule: `Run is done when completed_steps reaches requested_steps or the process is interrupted.`

## Target

- Target binary: `/home/kali/Fuzzi/Fuzzinator/targets/target_maze`
- Seed file: `/home/kali/Fuzzi/Fuzzinator/corpus/seed.bin`
- Target name: `target_maze`

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

- elapsed_seconds: `241.846`
- exec_speed: `4.135`
- total_reward: `1983.2`
- total_edges: `208`
- total_crashes: `0`
- ppo_updates: `4`

## Crashes Created In This Run

- None

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=bit_flip
- step=2, type=coverage_gain, new_edges=7, total_edges=14, action=byte_flip
- step=3, type=coverage_gain, new_edges=7, total_edges=21, action=byte_flip
- step=4, type=coverage_gain, new_edges=7, total_edges=28, action=byte_flip
- step=5, type=coverage_gain, new_edges=6, total_edges=34, action=byte_insert
- step=6, type=coverage_gain, new_edges=7, total_edges=41, action=byte_insert
- step=7, type=coverage_gain, new_edges=7, total_edges=48, action=byte_insert
- step=8, type=coverage_gain, new_edges=7, total_edges=55, action=byte_insert
- step=9, type=coverage_gain, new_edges=7, total_edges=62, action=byte_insert
- step=12, type=coverage_gain, new_edges=7, total_edges=69, action=havoc
- step=13, type=coverage_gain, new_edges=6, total_edges=75, action=havoc
- step=16, type=coverage_gain, new_edges=6, total_edges=81, action=byte_insert
- step=17, type=coverage_gain, new_edges=7, total_edges=88, action=bit_flip
- step=18, type=coverage_gain, new_edges=6, total_edges=94, action=bit_flip
- step=19, type=coverage_gain, new_edges=7, total_edges=101, action=byte_flip
- step=20, type=coverage_gain, new_edges=6, total_edges=107, action=byte_insert
- step=21, type=coverage_gain, new_edges=7, total_edges=114, action=byte_flip
- step=23, type=coverage_gain, new_edges=6, total_edges=120, action=bit_flip
- step=24, type=coverage_gain, new_edges=7, total_edges=127, action=byte_flip
- step=30, type=coverage_gain, new_edges=7, total_edges=134, action=byte_flip
- step=32, type=coverage_gain, new_edges=6, total_edges=140, action=bit_flip
- step=37, type=coverage_gain, new_edges=7, total_edges=147, action=byte_flip
- step=43, type=coverage_gain, new_edges=6, total_edges=153, action=bit_flip
- step=46, type=coverage_gain, new_edges=6, total_edges=159, action=havoc
- step=51, type=coverage_gain, new_edges=7, total_edges=166, action=havoc
- step=54, type=coverage_gain, new_edges=6, total_edges=172, action=byte_flip
- step=59, type=coverage_gain, new_edges=6, total_edges=178, action=byte_insert
- step=61, type=coverage_gain, new_edges=6, total_edges=184, action=byte_flip
- step=62, type=coverage_gain, new_edges=6, total_edges=190, action=byte_flip
- step=67, type=coverage_gain, new_edges=6, total_edges=196, action=havoc
- step=68, type=coverage_gain, new_edges=6, total_edges=202, action=havoc
- step=69, type=coverage_gain, new_edges=6, total_edges=208, action=byte_flip
- step=256, type=ppo_update, update=1, policy_loss=-0.0033, value_loss=36608.6436, entropy=1.3844
- step=500, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_500.pt
- step=512, type=ppo_update, update=2, policy_loss=-0.0022, value_loss=1.8462, entropy=1.3838
- step=768, type=ppo_update, update=3, policy_loss=0.0005, value_loss=1.9686, entropy=1.3852
- step=1000, type=ppo_update, update=4, policy_loss=-0.0041, value_loss=1.099, entropy=1.3436
- step=1000, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_1000.pt

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T10-16-44_ppo_lstm_target_maze.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T10-16-44_ppo_lstm_target_maze.json`

# Run Report: PPO+LSTM

Started: 2026-03-18T10:21:09
Finished: 2026-03-18T10:25:00
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

- elapsed_seconds: `231.916`
- exec_speed: `4.312`
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
- step=5, type=coverage_gain, new_edges=7, total_edges=35, action=byte_insert
- step=6, type=coverage_gain, new_edges=7, total_edges=42, action=byte_insert
- step=7, type=coverage_gain, new_edges=7, total_edges=49, action=byte_insert
- step=8, type=coverage_gain, new_edges=7, total_edges=56, action=byte_insert
- step=9, type=coverage_gain, new_edges=6, total_edges=62, action=byte_insert
- step=10, type=coverage_gain, new_edges=7, total_edges=69, action=byte_flip
- step=12, type=coverage_gain, new_edges=7, total_edges=76, action=havoc
- step=13, type=coverage_gain, new_edges=6, total_edges=82, action=havoc
- step=15, type=coverage_gain, new_edges=7, total_edges=89, action=bit_flip
- step=16, type=coverage_gain, new_edges=7, total_edges=96, action=byte_insert
- step=17, type=coverage_gain, new_edges=7, total_edges=103, action=bit_flip
- step=18, type=coverage_gain, new_edges=7, total_edges=110, action=bit_flip
- step=19, type=coverage_gain, new_edges=7, total_edges=117, action=byte_flip
- step=28, type=coverage_gain, new_edges=7, total_edges=124, action=bit_flip
- step=32, type=coverage_gain, new_edges=6, total_edges=130, action=bit_flip
- step=37, type=coverage_gain, new_edges=6, total_edges=136, action=byte_flip
- step=38, type=coverage_gain, new_edges=6, total_edges=142, action=byte_insert
- step=39, type=coverage_gain, new_edges=6, total_edges=148, action=byte_insert
- step=40, type=coverage_gain, new_edges=6, total_edges=154, action=byte_insert
- step=41, type=coverage_gain, new_edges=6, total_edges=160, action=havoc
- step=43, type=coverage_gain, new_edges=6, total_edges=166, action=bit_flip
- step=50, type=coverage_gain, new_edges=6, total_edges=172, action=byte_insert
- step=51, type=coverage_gain, new_edges=6, total_edges=178, action=havoc
- step=61, type=coverage_gain, new_edges=6, total_edges=184, action=byte_flip
- step=64, type=coverage_gain, new_edges=6, total_edges=190, action=bit_flip
- step=65, type=coverage_gain, new_edges=6, total_edges=196, action=byte_flip
- step=94, type=coverage_gain, new_edges=6, total_edges=202, action=havoc
- step=100, type=coverage_gain, new_edges=6, total_edges=208, action=bit_flip
- step=256, type=ppo_update, update=1, policy_loss=-0.0027, value_loss=34564.5461, entropy=1.3842
- step=500, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_500.pt
- step=512, type=ppo_update, update=2, policy_loss=-0.0034, value_loss=1.8318, entropy=1.3837
- step=768, type=ppo_update, update=3, policy_loss=0.0004, value_loss=1.9726, entropy=1.3851
- step=1000, type=ppo_update, update=4, policy_loss=-0.0042, value_loss=1.1615, entropy=1.3419
- step=1000, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_1000.pt

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T10-21-09_ppo_lstm_target_maze.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T10-21-09_ppo_lstm_target_maze.json`

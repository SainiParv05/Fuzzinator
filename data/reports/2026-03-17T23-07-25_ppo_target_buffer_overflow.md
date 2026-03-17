# Run Report: PPO

Started: 2026-03-17T23:07:25
Finished: 2026-03-17T23:07:26
Status: `completed`

## Completion

- Requested steps: `5`
- Completed steps: `5`
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

## Final Metrics

- elapsed_seconds: `0.812`
- exec_speed: `6.16`
- total_reward: `350.0`
- total_edges: `35`
- total_crashes: `0`
- ppo_updates: `1`

## Crashes Created In This Run

- None

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=byte_flip
- step=2, type=coverage_gain, new_edges=7, total_edges=14, action=byte_flip
- step=3, type=coverage_gain, new_edges=7, total_edges=21, action=byte_insert
- step=4, type=coverage_gain, new_edges=7, total_edges=28, action=bit_flip
- step=5, type=coverage_gain, new_edges=7, total_edges=35, action=byte_flip
- step=5, type=ppo_update, update=1, policy_loss=-0.0013, value_loss=26546.5103, entropy=1.3856

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-17T23-07-25_ppo_target_buffer_overflow.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-17T23-07-25_ppo_target_buffer_overflow.json`

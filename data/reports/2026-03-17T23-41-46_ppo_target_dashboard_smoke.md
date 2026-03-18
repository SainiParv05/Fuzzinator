# Run Report: PPO

Started: 2026-03-17T23:41:46
Finished: 2026-03-17T23:41:47
Status: `completed`

## Completion

- Requested steps: `1`
- Completed steps: `1`
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

## Final Metrics

- elapsed_seconds: `1.036`
- exec_speed: `0.965`
- total_reward: `70.0`
- total_edges: `7`
- total_crashes: `0`
- ppo_updates: `1`

## Crashes Created In This Run

- None

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=byte_flip
- step=1, type=ppo_update, update=1, policy_loss=-70.2701, value_loss=4883.9663, entropy=1.3856

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-17T23-41-46_ppo_target_dashboard_smoke.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-17T23-41-46_ppo_target_dashboard_smoke.json`

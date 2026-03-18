# Run Report: PPO+LSTM

Started: 2026-03-18T10:32:37
Finished: 2026-03-18T10:33:05
Status: `completed`

## Completion

- Requested steps: `200`
- Completed steps: `200`
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

- elapsed_seconds: `28.18`
- exec_speed: `7.097`
- total_reward: `3705.6`
- total_edges: `272`
- total_crashes: `9`
- ppo_updates: `1`

## Crashes Created In This Run

- `crash_SIGABRT_118bc7e9bd9e5cc1.bin`
- `crash_SIGABRT_120044aac52128d7.bin`
- `crash_SIGABRT_4792b06a64fe0740.bin`
- `crash_SIGABRT_7ba21d407eb7ef29.bin`
- `crash_SIGABRT_c1676d4d2fae751a.bin`

## Notable Events

- step=1, type=crash, signal=SIGABRT, reward=160.0, total_crashes=1
- step=1, type=coverage_gain, new_edges=6, total_edges=6, action=bit_flip
- step=2, type=crash, signal=SIGABRT, reward=160.0, total_crashes=2
- step=2, type=coverage_gain, new_edges=6, total_edges=12, action=byte_flip
- step=3, type=crash, signal=SIGABRT, reward=160.0, total_crashes=2
- step=3, type=coverage_gain, new_edges=6, total_edges=18, action=byte_flip
- step=4, type=crash, signal=SIGABRT, reward=160.0, total_crashes=3
- step=4, type=coverage_gain, new_edges=6, total_edges=24, action=byte_flip
- step=5, type=crash, signal=SIGABRT, reward=99.9, total_crashes=4
- step=6, type=crash, signal=SIGABRT, reward=99.9, total_crashes=5
- step=7, type=crash, signal=SIGABRT, reward=160.0, total_crashes=6
- step=7, type=coverage_gain, new_edges=6, total_edges=30, action=byte_insert
- step=8, type=crash, signal=SIGABRT, reward=160.0, total_crashes=7
- step=8, type=coverage_gain, new_edges=6, total_edges=36, action=byte_insert
- step=9, type=crash, signal=SIGABRT, reward=160.0, total_crashes=8
- step=9, type=coverage_gain, new_edges=6, total_edges=42, action=byte_insert
- step=10, type=crash, signal=SIGABRT, reward=160.0, total_crashes=9
- step=10, type=coverage_gain, new_edges=6, total_edges=48, action=byte_flip
- step=11, type=coverage_gain, new_edges=8, total_edges=56, action=havoc
- step=12, type=coverage_gain, new_edges=8, total_edges=64, action=havoc
- step=13, type=coverage_gain, new_edges=8, total_edges=72, action=havoc
- step=14, type=coverage_gain, new_edges=8, total_edges=80, action=bit_flip
- step=15, type=coverage_gain, new_edges=2, total_edges=82, action=bit_flip
- step=16, type=coverage_gain, new_edges=2, total_edges=84, action=byte_insert
- step=18, type=coverage_gain, new_edges=8, total_edges=92, action=bit_flip
- step=23, type=coverage_gain, new_edges=2, total_edges=94, action=bit_flip
- step=24, type=coverage_gain, new_edges=2, total_edges=96, action=byte_flip
- step=25, type=coverage_gain, new_edges=2, total_edges=98, action=byte_insert
- step=26, type=coverage_gain, new_edges=8, total_edges=106, action=bit_flip
- step=27, type=coverage_gain, new_edges=7, total_edges=113, action=bit_flip
- step=28, type=coverage_gain, new_edges=2, total_edges=115, action=bit_flip
- step=30, type=coverage_gain, new_edges=2, total_edges=117, action=byte_flip
- step=31, type=coverage_gain, new_edges=7, total_edges=124, action=byte_insert
- step=32, type=coverage_gain, new_edges=7, total_edges=131, action=bit_flip
- step=35, type=coverage_gain, new_edges=2, total_edges=133, action=havoc
- step=36, type=coverage_gain, new_edges=2, total_edges=135, action=bit_flip
- step=37, type=coverage_gain, new_edges=7, total_edges=142, action=byte_flip
- step=38, type=coverage_gain, new_edges=2, total_edges=144, action=byte_insert
- step=39, type=coverage_gain, new_edges=2, total_edges=146, action=byte_insert
- step=40, type=coverage_gain, new_edges=2, total_edges=148, action=byte_insert
- step=41, type=coverage_gain, new_edges=7, total_edges=155, action=havoc
- step=43, type=coverage_gain, new_edges=8, total_edges=163, action=bit_flip
- step=44, type=coverage_gain, new_edges=2, total_edges=165, action=havoc
- step=45, type=coverage_gain, new_edges=7, total_edges=172, action=havoc
- step=47, type=coverage_gain, new_edges=7, total_edges=179, action=byte_insert
- step=49, type=coverage_gain, new_edges=7, total_edges=186, action=byte_flip
- step=51, type=coverage_gain, new_edges=2, total_edges=188, action=havoc
- step=52, type=coverage_gain, new_edges=2, total_edges=190, action=byte_flip
- step=54, type=coverage_gain, new_edges=7, total_edges=197, action=byte_flip
- step=55, type=coverage_gain, new_edges=7, total_edges=204, action=byte_flip
- step=58, type=coverage_gain, new_edges=2, total_edges=206, action=byte_insert
- step=59, type=coverage_gain, new_edges=2, total_edges=208, action=byte_insert
- step=60, type=coverage_gain, new_edges=7, total_edges=215, action=byte_insert
- step=63, type=coverage_gain, new_edges=2, total_edges=217, action=byte_insert
- step=67, type=coverage_gain, new_edges=7, total_edges=224, action=havoc
- step=68, type=coverage_gain, new_edges=2, total_edges=226, action=havoc
- step=69, type=coverage_gain, new_edges=2, total_edges=228, action=byte_flip
- step=72, type=coverage_gain, new_edges=8, total_edges=236, action=bit_flip
- step=76, type=coverage_gain, new_edges=7, total_edges=243, action=havoc
- step=83, type=coverage_gain, new_edges=2, total_edges=245, action=byte_flip
- step=90, type=coverage_gain, new_edges=2, total_edges=247, action=byte_flip
- step=92, type=coverage_gain, new_edges=2, total_edges=249, action=byte_flip
- step=93, type=coverage_gain, new_edges=7, total_edges=256, action=bit_flip
- step=112, type=coverage_gain, new_edges=2, total_edges=258, action=byte_flip
- step=141, type=coverage_gain, new_edges=7, total_edges=265, action=byte_insert
- step=178, type=coverage_gain, new_edges=7, total_edges=272, action=havoc
- step=200, type=ppo_update, update=1, policy_loss=-0.0013, value_loss=108039.4091, entropy=1.3843

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T10-32-37_ppo_lstm_target_format_string.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T10-32-37_ppo_lstm_target_format_string.json`

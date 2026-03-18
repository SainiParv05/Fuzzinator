# Run Report: PPO+LSTM

Started: 2026-03-18T15:23:06
Finished: 2026-03-18T15:23:34
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

- elapsed_seconds: `27.281`
- exec_speed: `7.331`
- total_reward: `5305.4`
- total_edges: `252`
- total_crashes: `28`
- ppo_updates: `1`

## Crashes Created In This Run

- `crash_SIGABRT_0b6a888368223aa2.bin`
- `crash_SIGABRT_0dc219053d11ccea.bin`
- `crash_SIGABRT_0f1c737e72109796.bin`
- `crash_SIGABRT_339c76b26db46792.bin`
- `crash_SIGABRT_40197cd5aebf3222.bin`
- `crash_SIGABRT_42efa3dbd39cb7ef.bin`
- `crash_SIGABRT_4d96db05b63732bf.bin`
- `crash_SIGABRT_55dc3b37fe74bc0b.bin`
- `crash_SIGABRT_5a4a8855bcc6af77.bin`
- `crash_SIGABRT_66fd14b6f7d3bf9d.bin`
- `crash_SIGABRT_6d63b2bf64227720.bin`
- `crash_SIGABRT_7580582f2f5817b1.bin`
- `crash_SIGABRT_7c7455818fdcf771.bin`
- `crash_SIGABRT_8470af65f5729ff6.bin`
- `crash_SIGABRT_87cf8d7ac7f8d0de.bin`
- `crash_SIGABRT_92c8a0405483be85.bin`
- `crash_SIGABRT_96db0b10a7781f63.bin`
- `crash_SIGABRT_a1998c8dfe82c1eb.bin`
- `crash_SIGABRT_a3428cdede16624c.bin`
- `crash_SIGABRT_a721f77fe3bfa1d7.bin`
- `crash_SIGABRT_c07d00e0af2d567d.bin`
- `crash_SIGABRT_ca5e03e0464661f7.bin`
- `crash_SIGABRT_cb89efa6104437b7.bin`
- `crash_SIGABRT_d38d92df14872be1.bin`
- `crash_SIGABRT_ec2fa6072e2a6061.bin`
- `crash_SIGABRT_f34d7f8464a3a746.bin`
- `crash_SIGABRT_f67ee94f2235d5b3.bin`
- `crash_SIGABRT_f8676d6af35e25ee.bin`

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=bit_flip
- step=2, type=coverage_gain, new_edges=7, total_edges=14, action=byte_flip
- step=3, type=coverage_gain, new_edges=7, total_edges=21, action=byte_flip
- step=4, type=coverage_gain, new_edges=7, total_edges=28, action=byte_flip
- step=5, type=coverage_gain, new_edges=7, total_edges=35, action=byte_insert
- step=6, type=coverage_gain, new_edges=7, total_edges=42, action=byte_insert
- step=7, type=coverage_gain, new_edges=7, total_edges=49, action=byte_insert
- step=8, type=coverage_gain, new_edges=6, total_edges=55, action=byte_insert
- step=9, type=coverage_gain, new_edges=6, total_edges=61, action=byte_insert
- step=10, type=coverage_gain, new_edges=7, total_edges=68, action=byte_flip
- step=12, type=coverage_gain, new_edges=7, total_edges=75, action=havoc
- step=14, type=coverage_gain, new_edges=7, total_edges=82, action=bit_flip
- step=17, type=coverage_gain, new_edges=6, total_edges=88, action=bit_flip
- step=18, type=coverage_gain, new_edges=7, total_edges=95, action=bit_flip
- step=20, type=coverage_gain, new_edges=6, total_edges=101, action=byte_insert
- step=22, type=coverage_gain, new_edges=6, total_edges=107, action=havoc
- step=23, type=coverage_gain, new_edges=6, total_edges=113, action=bit_flip
- step=24, type=coverage_gain, new_edges=6, total_edges=119, action=byte_flip
- step=25, type=coverage_gain, new_edges=7, total_edges=126, action=byte_insert
- step=26, type=coverage_gain, new_edges=7, total_edges=133, action=bit_flip
- step=28, type=coverage_gain, new_edges=7, total_edges=140, action=bit_flip
- step=30, type=coverage_gain, new_edges=6, total_edges=146, action=byte_flip
- step=31, type=coverage_gain, new_edges=7, total_edges=153, action=byte_insert
- step=45, type=coverage_gain, new_edges=6, total_edges=159, action=havoc
- step=47, type=coverage_gain, new_edges=6, total_edges=165, action=byte_insert
- step=48, type=coverage_gain, new_edges=7, total_edges=172, action=byte_flip
- step=49, type=coverage_gain, new_edges=6, total_edges=178, action=byte_flip
- step=71, type=coverage_gain, new_edges=6, total_edges=184, action=byte_flip
- step=75, type=coverage_gain, new_edges=6, total_edges=190, action=havoc
- step=78, type=coverage_gain, new_edges=6, total_edges=196, action=bit_flip
- step=86, type=coverage_gain, new_edges=6, total_edges=202, action=byte_insert
- step=88, type=coverage_gain, new_edges=6, total_edges=208, action=havoc
- step=96, type=crash, signal=SIGABRT, reward=99.9, total_crashes=1
- step=103, type=crash, signal=SIGABRT, reward=99.9, total_crashes=2
- step=136, type=coverage_gain, new_edges=2, total_edges=210, action=havoc
- step=137, type=crash, signal=SIGABRT, reward=99.9, total_crashes=3
- step=138, type=coverage_gain, new_edges=2, total_edges=212, action=bit_flip
- step=139, type=coverage_gain, new_edges=2, total_edges=214, action=byte_flip
- step=140, type=coverage_gain, new_edges=2, total_edges=216, action=havoc
- step=141, type=crash, signal=SIGABRT, reward=99.9, total_crashes=4
- step=142, type=crash, signal=SIGABRT, reward=99.9, total_crashes=5
- step=143, type=crash, signal=SIGABRT, reward=99.9, total_crashes=6
- step=144, type=coverage_gain, new_edges=2, total_edges=218, action=bit_flip
- step=145, type=coverage_gain, new_edges=2, total_edges=220, action=bit_flip
- step=146, type=coverage_gain, new_edges=2, total_edges=222, action=bit_flip
- step=147, type=coverage_gain, new_edges=2, total_edges=224, action=byte_flip
- step=148, type=coverage_gain, new_edges=2, total_edges=226, action=byte_flip
- step=150, type=coverage_gain, new_edges=2, total_edges=228, action=byte_flip
- step=151, type=coverage_gain, new_edges=2, total_edges=230, action=bit_flip
- step=153, type=crash, signal=SIGABRT, reward=99.9, total_crashes=7
- step=154, type=crash, signal=SIGABRT, reward=99.9, total_crashes=8
- step=155, type=crash, signal=SIGABRT, reward=99.9, total_crashes=9
- step=157, type=crash, signal=SIGABRT, reward=99.9, total_crashes=10
- step=158, type=coverage_gain, new_edges=2, total_edges=232, action=bit_flip
- step=159, type=crash, signal=SIGABRT, reward=99.9, total_crashes=11
- step=160, type=crash, signal=SIGABRT, reward=99.9, total_crashes=12
- step=161, type=crash, signal=SIGABRT, reward=99.9, total_crashes=13
- step=163, type=crash, signal=SIGABRT, reward=99.9, total_crashes=14
- step=165, type=coverage_gain, new_edges=2, total_edges=234, action=byte_flip
- step=166, type=coverage_gain, new_edges=2, total_edges=236, action=bit_flip
- step=167, type=crash, signal=SIGABRT, reward=99.9, total_crashes=15
- step=170, type=crash, signal=SIGABRT, reward=99.9, total_crashes=16
- step=171, type=crash, signal=SIGABRT, reward=99.9, total_crashes=17
- step=172, type=crash, signal=SIGABRT, reward=99.9, total_crashes=18
- step=173, type=coverage_gain, new_edges=2, total_edges=238, action=bit_flip
- step=174, type=coverage_gain, new_edges=2, total_edges=240, action=byte_flip
- step=175, type=crash, signal=SIGABRT, reward=99.9, total_crashes=19
- step=176, type=crash, signal=SIGABRT, reward=99.9, total_crashes=20
- step=178, type=coverage_gain, new_edges=2, total_edges=242, action=havoc
- step=180, type=crash, signal=SIGABRT, reward=99.9, total_crashes=21
- step=182, type=crash, signal=SIGABRT, reward=99.9, total_crashes=22
- step=185, type=crash, signal=SIGABRT, reward=99.9, total_crashes=23
- step=187, type=crash, signal=SIGABRT, reward=99.9, total_crashes=24
- step=188, type=coverage_gain, new_edges=2, total_edges=244, action=bit_flip
- step=191, type=crash, signal=SIGABRT, reward=99.9, total_crashes=25
- step=192, type=crash, signal=SIGABRT, reward=99.9, total_crashes=26
- step=193, type=crash, signal=SIGABRT, reward=99.9, total_crashes=27
- step=194, type=coverage_gain, new_edges=2, total_edges=246, action=bit_flip
- step=195, type=coverage_gain, new_edges=2, total_edges=248, action=bit_flip
- step=196, type=crash, signal=SIGABRT, reward=99.9, total_crashes=28
- step=197, type=coverage_gain, new_edges=2, total_edges=250, action=havoc
- step=198, type=coverage_gain, new_edges=2, total_edges=252, action=byte_flip
- step=200, type=ppo_update, update=1, policy_loss=-0.0025, value_loss=203327.75, entropy=1.3845

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T15-23-06_ppo_lstm_target_buffer_overflow.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T15-23-06_ppo_lstm_target_buffer_overflow.json`

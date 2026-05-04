# Run Report: PPO+LSTM

Started: 2026-03-18T18:10:30
Finished: 2026-03-18T18:23:26
Status: `interrupted`

## Completion

- Requested steps: `10000`
- Completed steps: `3141`
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

- elapsed_seconds: `776.546`
- exec_speed: `4.045`
- total_reward: `3055.6`
- total_edges: `336`
- total_crashes: `0`
- ppo_updates: `12`

## Crashes Created In This Run

- None

## Notable Events

- step=1, type=coverage_gain, new_edges=7, total_edges=7, action=bit_flip
- step=3, type=coverage_gain, new_edges=7, total_edges=14, action=byte_flip
- step=4, type=coverage_gain, new_edges=7, total_edges=21, action=byte_flip
- step=5, type=coverage_gain, new_edges=7, total_edges=28, action=byte_insert
- step=6, type=coverage_gain, new_edges=7, total_edges=35, action=byte_insert
- step=7, type=coverage_gain, new_edges=7, total_edges=42, action=byte_insert
- step=8, type=coverage_gain, new_edges=6, total_edges=48, action=byte_insert
- step=10, type=coverage_gain, new_edges=6, total_edges=54, action=byte_flip
- step=11, type=coverage_gain, new_edges=7, total_edges=61, action=havoc
- step=13, type=coverage_gain, new_edges=7, total_edges=68, action=havoc
- step=14, type=coverage_gain, new_edges=7, total_edges=75, action=bit_flip
- step=16, type=coverage_gain, new_edges=7, total_edges=82, action=byte_insert
- step=17, type=coverage_gain, new_edges=6, total_edges=88, action=bit_flip
- step=21, type=coverage_gain, new_edges=7, total_edges=95, action=byte_flip
- step=22, type=coverage_gain, new_edges=6, total_edges=101, action=havoc
- step=23, type=coverage_gain, new_edges=7, total_edges=108, action=bit_flip
- step=24, type=coverage_gain, new_edges=6, total_edges=114, action=byte_flip
- step=28, type=coverage_gain, new_edges=6, total_edges=120, action=bit_flip
- step=29, type=coverage_gain, new_edges=6, total_edges=126, action=byte_flip
- step=33, type=coverage_gain, new_edges=7, total_edges=133, action=bit_flip
- step=36, type=coverage_gain, new_edges=7, total_edges=140, action=bit_flip
- step=44, type=coverage_gain, new_edges=6, total_edges=146, action=havoc
- step=45, type=coverage_gain, new_edges=7, total_edges=153, action=havoc
- step=48, type=coverage_gain, new_edges=6, total_edges=159, action=byte_flip
- step=52, type=coverage_gain, new_edges=6, total_edges=165, action=byte_flip
- step=60, type=coverage_gain, new_edges=6, total_edges=171, action=byte_insert
- step=61, type=coverage_gain, new_edges=6, total_edges=177, action=byte_flip
- step=63, type=coverage_gain, new_edges=7, total_edges=184, action=byte_insert
- step=66, type=coverage_gain, new_edges=6, total_edges=190, action=byte_flip
- step=73, type=coverage_gain, new_edges=6, total_edges=196, action=byte_flip
- step=77, type=coverage_gain, new_edges=6, total_edges=202, action=byte_flip
- step=120, type=coverage_gain, new_edges=6, total_edges=208, action=bit_flip
- step=256, type=ppo_update, update=1, policy_loss=-0.003, value_loss=35214.9436, entropy=1.3842
- step=272, type=coverage_gain, new_edges=1, total_edges=209, action=byte_insert
- step=273, type=coverage_gain, new_edges=1, total_edges=210, action=havoc
- step=274, type=coverage_gain, new_edges=1, total_edges=211, action=bit_flip
- step=275, type=coverage_gain, new_edges=1, total_edges=212, action=havoc
- step=276, type=coverage_gain, new_edges=1, total_edges=213, action=byte_insert
- step=278, type=coverage_gain, new_edges=1, total_edges=214, action=byte_flip
- step=279, type=coverage_gain, new_edges=1, total_edges=215, action=bit_flip
- step=280, type=coverage_gain, new_edges=1, total_edges=216, action=byte_insert
- step=281, type=coverage_gain, new_edges=1, total_edges=217, action=byte_flip
- step=282, type=coverage_gain, new_edges=1, total_edges=218, action=byte_flip
- step=283, type=coverage_gain, new_edges=1, total_edges=219, action=byte_insert
- step=285, type=coverage_gain, new_edges=1, total_edges=220, action=bit_flip
- step=286, type=coverage_gain, new_edges=1, total_edges=221, action=havoc
- step=288, type=coverage_gain, new_edges=1, total_edges=222, action=byte_flip
- step=293, type=coverage_gain, new_edges=1, total_edges=223, action=byte_insert
- step=294, type=coverage_gain, new_edges=1, total_edges=224, action=byte_flip
- step=295, type=coverage_gain, new_edges=1, total_edges=225, action=bit_flip
- step=296, type=coverage_gain, new_edges=1, total_edges=226, action=byte_insert
- step=297, type=coverage_gain, new_edges=1, total_edges=227, action=byte_flip
- step=300, type=coverage_gain, new_edges=1, total_edges=228, action=byte_insert
- step=304, type=coverage_gain, new_edges=1, total_edges=229, action=byte_insert
- step=310, type=coverage_gain, new_edges=1, total_edges=230, action=byte_insert
- step=314, type=coverage_gain, new_edges=1, total_edges=231, action=byte_insert
- step=320, type=coverage_gain, new_edges=1, total_edges=232, action=byte_flip
- step=330, type=coverage_gain, new_edges=1, total_edges=233, action=bit_flip
- step=332, type=coverage_gain, new_edges=1, total_edges=234, action=bit_flip
- step=335, type=coverage_gain, new_edges=1, total_edges=235, action=byte_flip
- step=338, type=coverage_gain, new_edges=1, total_edges=236, action=byte_insert
- step=341, type=coverage_gain, new_edges=1, total_edges=237, action=byte_insert
- step=343, type=coverage_gain, new_edges=1, total_edges=238, action=bit_flip
- step=350, type=coverage_gain, new_edges=1, total_edges=239, action=byte_insert
- step=369, type=coverage_gain, new_edges=1, total_edges=240, action=byte_flip
- step=500, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_500.pt
- step=512, type=ppo_update, update=2, policy_loss=-0.0029, value_loss=1055.9924, entropy=1.3811
- step=768, type=ppo_update, update=3, policy_loss=-0.0062, value_loss=2.6376, entropy=1.3591
- step=1000, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_1000.pt
- step=1024, type=ppo_update, update=4, policy_loss=-0.0077, value_loss=0.222, entropy=1.3489
- step=1280, type=ppo_update, update=5, policy_loss=0.0061, value_loss=0.888, entropy=1.3444
- step=1500, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_1500.pt
- step=1536, type=ppo_update, update=6, policy_loss=-0.0023, value_loss=1.7594, entropy=1.2771
- step=1792, type=ppo_update, update=7, policy_loss=0.0026, value_loss=0.9547, entropy=1.0695
- step=2000, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_2000.pt
- step=2048, type=ppo_update, update=8, policy_loss=0.0177, value_loss=1.5937, entropy=1.0186
- step=2304, type=ppo_update, update=9, policy_loss=0.0114, value_loss=1.3958, entropy=0.7366
- step=2473, type=coverage_gain, new_edges=3, total_edges=243, action=havoc
- step=2474, type=coverage_gain, new_edges=3, total_edges=246, action=byte_insert
- step=2475, type=coverage_gain, new_edges=3, total_edges=249, action=byte_insert
- step=2476, type=coverage_gain, new_edges=3, total_edges=252, action=byte_insert
- step=2477, type=coverage_gain, new_edges=3, total_edges=255, action=byte_insert
- step=2478, type=coverage_gain, new_edges=3, total_edges=258, action=byte_insert
- step=2479, type=coverage_gain, new_edges=3, total_edges=261, action=byte_insert
- step=2480, type=coverage_gain, new_edges=3, total_edges=264, action=byte_insert
- step=2481, type=coverage_gain, new_edges=3, total_edges=267, action=byte_insert
- step=2482, type=coverage_gain, new_edges=3, total_edges=270, action=byte_insert
- step=2483, type=coverage_gain, new_edges=3, total_edges=273, action=byte_insert
- step=2486, type=coverage_gain, new_edges=3, total_edges=276, action=byte_insert
- step=2487, type=coverage_gain, new_edges=3, total_edges=279, action=byte_insert
- step=2490, type=coverage_gain, new_edges=3, total_edges=282, action=byte_insert
- step=2493, type=coverage_gain, new_edges=3, total_edges=285, action=byte_insert
- step=2494, type=coverage_gain, new_edges=3, total_edges=288, action=byte_insert
- step=2495, type=coverage_gain, new_edges=3, total_edges=291, action=byte_insert
- step=2497, type=coverage_gain, new_edges=3, total_edges=294, action=bit_flip
- step=2498, type=coverage_gain, new_edges=3, total_edges=297, action=byte_insert
- step=2500, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_2500.pt
- step=2502, type=coverage_gain, new_edges=3, total_edges=300, action=byte_insert
- step=2504, type=coverage_gain, new_edges=3, total_edges=303, action=byte_insert
- step=2506, type=coverage_gain, new_edges=3, total_edges=306, action=byte_insert
- step=2507, type=coverage_gain, new_edges=3, total_edges=309, action=byte_insert
- step=2513, type=coverage_gain, new_edges=3, total_edges=312, action=byte_insert
- step=2518, type=coverage_gain, new_edges=3, total_edges=315, action=byte_insert
- step=2521, type=coverage_gain, new_edges=3, total_edges=318, action=byte_insert
- step=2527, type=coverage_gain, new_edges=3, total_edges=321, action=byte_insert
- step=2530, type=coverage_gain, new_edges=3, total_edges=324, action=byte_insert
- step=2540, type=coverage_gain, new_edges=3, total_edges=327, action=byte_insert
- step=2541, type=coverage_gain, new_edges=3, total_edges=330, action=byte_insert
- step=2546, type=coverage_gain, new_edges=3, total_edges=333, action=byte_insert
- step=2548, type=coverage_gain, new_edges=3, total_edges=336, action=byte_insert
- step=2560, type=ppo_update, update=10, policy_loss=0.0231, value_loss=11022.7482, entropy=0.615
- step=2816, type=ppo_update, update=11, policy_loss=0.0141, value_loss=4.0577, entropy=0.6051
- step=3000, type=checkpoint, path=/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_step_3000.pt
- step=3072, type=ppo_update, update=12, policy_loss=0.0132, value_loss=1.2247, entropy=0.4326

## Artifacts

- Final checkpoint: `/home/kali/Fuzzi/Fuzzinator/data/checkpoints/ppo_lstm_final.pt`
- Crash dir: `/home/kali/Fuzzi/Fuzzinator/data/crashes`
- Markdown report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T18-10-30_ppo_lstm_target_maze.md`
- JSON report: `/home/kali/Fuzzi/Fuzzinator/data/reports/2026-03-18T18-10-30_ppo_lstm_target_maze.json`

# PPO vs PPO+LSTM Benchmark Report

Generated on: 2026-03-17 22:44:46
Steps per target: 30
Seeds per target: [1337, 2027, 4242]

## Baseline PPO

| Target | Runs | Avg Time (s) | Avg Exec/s | Avg Edges | Avg Crashes | Avg Updates |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `targets/target_maze` | 3 | 0.6 | 94.3 | 123.667 | 0.0 | 1.0 |

## PPO+LSTM

| Target | Runs | Avg Time (s) | Avg Exec/s | Avg Edges | Avg Crashes | Avg Updates |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `targets/target_maze` | 3 | 68.133 | 0.467 | 139.667 | 0.0 | 1.0 |

## Comparison Summary

- `targets/target_maze`: edge delta +16.0, crash delta +0.0, exec/s delta -93.8.

## Per-Seed Results

### `targets/target_maze`

| Model | Seed | Time (s) | Exec/s | Edges | Crashes |
| --- | ---: | ---: | ---: | ---: | ---: |
| PPO | 1337 | 1.4 | 20.9 | 121 | 0 |
| PPO | 2027 | 0.2 | 130.2 | 115 | 0 |
| PPO | 4242 | 0.2 | 131.8 | 135 | 0 |
| PPO+LSTM | 1337 | 96.9 | 0.3 | 146 | 0 |
| PPO+LSTM | 2027 | 55.9 | 0.5 | 133 | 0 |
| PPO+LSTM | 4242 | 51.6 | 0.6 | 140 | 0 |


## Notes

- These benchmarks now aggregate multiple seeds for each target.
- Baseline PPO uses `agent/train.py`.
- PPO+LSTM uses `agent/train_lstm.py`.
- For stronger statistical confidence, rerun with longer campaigns and more seeds.

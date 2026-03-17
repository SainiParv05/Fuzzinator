# PPO vs PPO+LSTM Benchmark Report

Generated on: 2026-03-17 22:44:43
Steps per target: 30
Seeds per target: [1337, 2027, 4242]

## Baseline PPO

| Target | Runs | Avg Time (s) | Avg Exec/s | Avg Edges | Avg Crashes | Avg Updates |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `targets/target_maze` | 3 | 0.733 | 81.233 | 129.0 | 0.0 | 1.0 |

## PPO+LSTM

| Target | Runs | Avg Time (s) | Avg Exec/s | Avg Edges | Avg Crashes | Avg Updates |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `targets/target_maze` | 3 | 67.0 | 0.467 | 127.667 | 0.0 | 1.0 |

## Comparison Summary

- `targets/target_maze`: edge delta -1.3329999999999984, crash delta +0.0, exec/s delta -80.8.

## Per-Seed Results

### `targets/target_maze`

| Model | Seed | Time (s) | Exec/s | Edges | Crashes |
| --- | ---: | ---: | ---: | ---: | ---: |
| PPO | 1337 | 1.6 | 18.5 | 133 | 0 |
| PPO | 2027 | 0.3 | 118.4 | 134 | 0 |
| PPO | 4242 | 0.3 | 106.8 | 120 | 0 |
| PPO+LSTM | 1337 | 95.5 | 0.3 | 115 | 0 |
| PPO+LSTM | 2027 | 55.0 | 0.5 | 141 | 0 |
| PPO+LSTM | 4242 | 50.5 | 0.6 | 127 | 0 |


## Notes

- These benchmarks now aggregate multiple seeds for each target.
- Baseline PPO uses `agent/train.py`.
- PPO+LSTM uses `agent/train_lstm.py`.
- For stronger statistical confidence, rerun with longer campaigns and more seeds.

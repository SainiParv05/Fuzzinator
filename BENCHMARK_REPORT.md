# PPO vs PPO+LSTM Benchmark Report

Generated on: 2026-03-17 22:21:54
Steps per target: 60

## Baseline PPO

| Target | Steps | Time (s) | Exec/s | Edges | Crashes | Updates |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `targets/target_buffer_overflow` | 60 | 0.5 | 112.7 | 171 | 0 | 1 |
| `targets/target_format_string` | 60 | 1.6 | 37.7 | 221 | 16 | 1 |
| `targets/target_maze` | 60 | 0.5 | 119.3 | 172 | 0 | 1 |

## PPO+LSTM

| Target | Steps | Time (s) | Exec/s | Edges | Crashes | Updates |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `targets/target_buffer_overflow` | 60 | 7.6 | 7.9 | 172 | 0 | 1 |
| `targets/target_format_string` | 60 | 8.0 | 7.5 | 222 | 4 | 1 |
| `targets/target_maze` | 60 | 7.6 | 7.9 | 196 | 0 | 1 |

## Comparison Summary

- `targets/target_buffer_overflow`: edge delta +1, crash delta +0, exec/s delta -104.8.
- `targets/target_format_string`: edge delta +1, crash delta -12, exec/s delta -30.2.
- `targets/target_maze`: edge delta +24, crash delta +0, exec/s delta -111.4.

## Notes

- These are short smoke benchmarks intended for apples-to-apples comparison on the same targets.
- Baseline PPO uses `agent/train.py`.
- PPO+LSTM uses `agent/train_lstm.py`.
- For stronger statistical confidence, rerun with multiple seeds and longer campaigns.

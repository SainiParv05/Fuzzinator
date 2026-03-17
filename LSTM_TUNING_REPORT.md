# LSTM Tuning Report

Generated on: 2026-03-17

## Goal

Improve PPO+LSTM practicality by:
- making experiments reproducible
- comparing results across multiple seeds
- testing lighter LSTM settings for better speed/quality tradeoff

## Changes Made

- Added explicit random seeding to both PPO and PPO+LSTM training flows.
- Added device selection support (`cpu`, `cuda`, `auto`) to training and benchmark runs.
- Upgraded benchmark aggregation to support multiple seeds and per-seed reporting.
- Compared current LSTM settings against a lighter configuration.

## Configurations Compared

### Previous LSTM Default
- device: `cpu`
- `lstm_hidden: 256`
- `lstm_layers: 2`

### Tuned LSTM Default
- device: `cpu`
- `lstm_hidden: 128`
- `lstm_layers: 1`

## Multi-Seed Benchmark

Target: `targets/target_maze`  
Steps: `30`  
Seeds: `1337, 2027, 4242`

### PPO Baseline vs Previous LSTM Default

Source: [BENCHMARK_REPORT.md](/home/kali/Fuzzi/Fuzzinator/BENCHMARK_REPORT.md)

| Model | Avg Exec/s | Avg Edges | Avg Crashes |
| --- | ---: | ---: | ---: |
| PPO | 81.233 | 129.0 | 0.0 |
| PPO+LSTM `256x2` | 0.467 | 127.667 | 0.0 |

### PPO Baseline vs Tuned LSTM

Source: [BENCHMARK_REPORT_TUNED_128x1.md](/home/kali/Fuzzi/Fuzzinator/BENCHMARK_REPORT_TUNED_128x1.md)

| Model | Avg Exec/s | Avg Edges | Avg Crashes |
| --- | ---: | ---: | ---: |
| PPO | 94.3 | 123.667 | 0.0 |
| PPO+LSTM `128x1` | 0.467 | 139.667 | 0.0 |

## Findings

- `128x1` performs better than `256x2` on the maze target in average edge discovery.
- Reducing LSTM size did not materially improve throughput.
- The main bottleneck is likely the semantic input encoder path rather than the recurrent head size.
- PPO baseline remains dramatically faster per step.
- PPO+LSTM still looks more promising for harder sequence-sensitive behavior than for raw throughput.

## Tuning Decision

The project default is now:
- `agent.device: cpu`
- `agent.lstm_hidden: 128`
- `agent.lstm_layers: 1`

This is the best current balance because:
- it preserves the stronger maze performance
- it avoids keeping a larger recurrent model that did not deliver better results

## What Still Needs Tuning

- profile `agent/input_encoder.py` to identify slow layers
- test shorter input lengths or more aggressive truncation
- compare CNN-only encoding vs CNN+BiLSTM input encoding
- run longer multi-seed benchmarks on `target_format_string` and `target_maze`
- decide whether PPO+LSTM should remain a research mode rather than the default training mode

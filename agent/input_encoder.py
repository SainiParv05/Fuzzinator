"""
input_encoder.py
Fuzzinator — Semantic input encoders for PPO+LSTM fuzzing.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class InputEncoder(nn.Module):
    """
    Encode raw input bytes into a fixed-size semantic feature vector.

    Byte value 0 is reserved for padding, so callers should offset real
    byte values into the [1, 256] range.
    """

    def __init__(self,
                 input_vocab_size: int = 257,
                 embedding_dim: int = 32,
                 conv_channels: list[int] | None = None,
                 lstm_hidden: int = 128,
                 output_dim: int = 256,
                 dropout: float = 0.1):
        super().__init__()

        if conv_channels is None:
            conv_channels = [64, 64, 32]

        self.embedding = nn.Embedding(
            num_embeddings=input_vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=0,
        )

        self.conv_layers = nn.ModuleList()
        kernel_sizes = [3, 5, 7]
        in_channels = embedding_dim

        for out_channels, kernel_size in zip(conv_channels, kernel_sizes):
            self.conv_layers.append(
                nn.Conv1d(
                    in_channels=in_channels,
                    out_channels=out_channels,
                    kernel_size=kernel_size,
                    padding=kernel_size // 2,
                )
            )
            in_channels = out_channels

        self.lstm = nn.LSTM(
            input_size=conv_channels[-1],
            hidden_size=lstm_hidden,
            num_layers=2,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if dropout > 0 else 0.0,
        )

        self.projection = nn.Linear(2 * lstm_hidden, output_dim)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(output_dim)

    def forward(self, raw_input: torch.Tensor) -> torch.Tensor:
        x = self.embedding(raw_input)
        x = self.dropout(x)
        x = x.transpose(1, 2)

        for conv in self.conv_layers:
            x = self.dropout(F.relu(conv(x)))

        x = x.transpose(1, 2)
        lstm_out, _ = self.lstm(x)
        pooled = torch.max(lstm_out, dim=1).values
        encoded = self.projection(pooled)
        return self.layer_norm(encoded)


class ActionSequenceEncoder(nn.Module):
    """Encode recent mutation actions into a compact feature vector."""

    def __init__(self,
                 num_actions: int = 4,
                 embedding_dim: int = 8,
                 output_dim: int = 64):
        super().__init__()

        self.action_embedding = nn.Embedding(
            num_embeddings=num_actions,
            embedding_dim=embedding_dim,
        )
        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=output_dim // 2,
            num_layers=1,
            batch_first=True,
            bidirectional=True,
        )

    def forward(self, actions: torch.Tensor) -> torch.Tensor:
        x = self.action_embedding(actions)
        lstm_out, _ = self.lstm(x)
        return lstm_out[:, -1, :]

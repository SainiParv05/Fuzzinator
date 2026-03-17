"""
ppo_agent_lstm.py
Fuzzinator — PPO agent with input semantics and temporal memory.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from agent.input_encoder import ActionSequenceEncoder, InputEncoder


class LSTMActorCritic(nn.Module):
    """Actor-critic with semantic input encoding and recurrent memory."""

    def __init__(self,
                 obs_size: int = 67,
                 n_actions: int = 4,
                 lstm_hidden: int = 256,
                 lstm_layers: int = 2,
                 dropout: float = 0.1):
        super().__init__()

        self.input_encoder = InputEncoder(output_dim=256, dropout=dropout)
        self.action_encoder = ActionSequenceEncoder(
            num_actions=n_actions,
            output_dim=64,
        )

        total_feature_size = obs_size + 256 + 64

        self.lstm = nn.LSTM(
            input_size=total_feature_size,
            hidden_size=lstm_hidden,
            num_layers=lstm_layers,
            batch_first=True,
            dropout=dropout if lstm_layers > 1 else 0.0,
        )

        self.actor = nn.Sequential(
            nn.Linear(lstm_hidden, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, n_actions),
        )

        self.critic = nn.Sequential(
            nn.Linear(lstm_hidden, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 1),
        )

    def forward(self,
                obs: torch.Tensor,
                raw_input: torch.Tensor,
                action_history: torch.Tensor,
                hidden_state: tuple[torch.Tensor, torch.Tensor] | None = None):
        encoded_input = self.input_encoder(raw_input)
        encoded_actions = self.action_encoder(action_history)
        combined = torch.cat([obs, encoded_input, encoded_actions], dim=1).unsqueeze(1)

        lstm_out, new_hidden_state = self.lstm(combined, hidden_state)
        features = lstm_out[:, -1, :]
        return self.actor(features), self.critic(features), new_hidden_state


class PPOAgentLSTM:
    """PPO agent that preserves hidden state during rollout collection."""

    def __init__(self,
                 obs_size: int = 67,
                 n_actions: int = 4,
                 lr: float = 3e-4,
                 gamma: float = 0.99,
                 clip_epsilon: float = 0.2,
                 entropy_coef: float = 0.01,
                 value_coef: float = 0.5,
                 max_grad_norm: float = 0.5,
                 ppo_epochs: int = 4,
                 batch_size: int = 64,
                 lstm_hidden: int = 256,
                 lstm_layers: int = 2,
                 device: str = "auto"):
        self.gamma = gamma
        self.clip_epsilon = clip_epsilon
        self.entropy_coef = entropy_coef
        self.value_coef = value_coef
        self.max_grad_norm = max_grad_norm
        self.ppo_epochs = ppo_epochs
        self.batch_size = batch_size
        if device == "auto":
            resolved_device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            resolved_device = device
        self.device = torch.device(resolved_device)

        self.network = LSTMActorCritic(
            obs_size=obs_size,
            n_actions=n_actions,
            lstm_hidden=lstm_hidden,
            lstm_layers=lstm_layers,
        ).to(self.device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=lr)
        self.hidden_state = None

    def reset_hidden_state(self):
        self.hidden_state = None

    def _detach_hidden_state(self):
        if self.hidden_state is None:
            return
        self.hidden_state = tuple(state.detach() for state in self.hidden_state)

    def get_action(self,
                   obs: np.ndarray,
                   raw_input: np.ndarray,
                   action_history: np.ndarray):
        obs_tensor = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
        input_tensor = torch.as_tensor(raw_input, dtype=torch.long, device=self.device).unsqueeze(0)
        action_tensor = torch.as_tensor(action_history, dtype=torch.long, device=self.device).unsqueeze(0)

        with torch.no_grad():
            logits, value, self.hidden_state = self.network(
                obs_tensor,
                input_tensor,
                action_tensor,
                self.hidden_state,
            )
            self._detach_hidden_state()
            probs = torch.softmax(logits, dim=-1)
            dist = torch.distributions.Categorical(probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)

        return action.item(), log_prob.item(), value.item()

    def get_value(self,
                  obs: np.ndarray,
                  raw_input: np.ndarray,
                  action_history: np.ndarray) -> float:
        obs_tensor = torch.as_tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
        input_tensor = torch.as_tensor(raw_input, dtype=torch.long, device=self.device).unsqueeze(0)
        action_tensor = torch.as_tensor(action_history, dtype=torch.long, device=self.device).unsqueeze(0)

        with torch.no_grad():
            _, value, _ = self.network(obs_tensor, input_tensor, action_tensor)

        return value.item()

    def update(self, rollout_buffer):
        total_policy_loss = 0.0
        total_value_loss = 0.0
        total_entropy = 0.0
        n_updates = 0

        for _ in range(self.ppo_epochs):
            for batch in rollout_buffer.get_batches(self.batch_size):
                obs = batch["obs"].to(self.device)
                raw_input = batch["raw_input"].to(self.device)
                action_history = batch["action_history"].to(self.device)
                actions = batch["actions"].to(self.device)
                old_log_probs = batch["log_probs"].to(self.device)
                advantages = batch["advantages"].to(self.device)
                returns = batch["returns"].to(self.device)

                if len(advantages) > 1:
                    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

                logits, values, _ = self.network(obs, raw_input, action_history)
                probs = torch.softmax(logits, dim=-1)
                dist = torch.distributions.Categorical(probs)
                new_log_probs = dist.log_prob(actions)
                entropy = dist.entropy().mean()

                ratio = torch.exp(new_log_probs - old_log_probs)
                surr1 = ratio * advantages
                surr2 = torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * advantages
                policy_loss = -torch.min(surr1, surr2).mean()
                value_loss = nn.functional.mse_loss(values.squeeze(-1), returns)
                loss = policy_loss + self.value_coef * value_loss - self.entropy_coef * entropy

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.network.parameters(), self.max_grad_norm)
                self.optimizer.step()

                total_policy_loss += policy_loss.item()
                total_value_loss += value_loss.item()
                total_entropy += entropy.item()
                n_updates += 1

        return {
            "policy_loss": total_policy_loss / max(n_updates, 1),
            "value_loss": total_value_loss / max(n_updates, 1),
            "entropy": total_entropy / max(n_updates, 1),
        }

    def save(self, path: str):
        torch.save(
            {
                "network": self.network.state_dict(),
                "optimizer": self.optimizer.state_dict(),
            },
            path,
        )

    def load(self, path: str):
        checkpoint = torch.load(path, map_location=self.device)
        self.network.load_state_dict(checkpoint["network"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])

# Fuzzinator: LSTM + GUI Implementation Guide

**Quick Start Implementation Checklist**  
**Target Duration:** 2-3 weeks for full implementation

---

## SECTION 1: LSTM IMPLEMENTATION

### Step 1.1: Create Input Encoder (`agent/input_encoder.py`)

This module learns semantic patterns in the raw input bytes through embeddings and convolutions.

```python
"""
input_encoder.py
Semantic Input Encoding for Vulnerability-Aware Fuzzing

Converts raw input bytes (0-256 range) into learned semantic features
using character embeddings + 1D CNNs + bidirectional LSTM.

This allows the agent to understand structural patterns in inputs
(e.g., "this looks like a format string", "this is binary code").
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class InputEncoder(nn.Module):
    """
    Encodes raw input bytes into fixed-size semantic features.
    
    Architecture:
    - Embedding layer: byte value (0-255) → 32-dim vector
    - Conv1D stack: extract local patterns (3-grams, 5-grams, 7-grams)
    - Bidirectional LSTM: capture long-range dependencies
    - Global pooling: reduce to fixed size (256)
    
    Input: (batch_size, max_input_len)
    Output: (batch_size, 256)
    """
    
    def __init__(self, 
                 input_vocab_size: int = 256,
                 embedding_dim: int = 32,
                 conv_channels: list = [64, 64, 32],
                 lstm_hidden: int = 128,
                 output_dim: int = 256,
                 dropout: float = 0.2):
        super().__init__()
        
        self.embedding_dim = embedding_dim
        self.output_dim = output_dim
        
        # ─── Embedding Layer ───
        # Treat each byte value (0-255) as a token
        self.embedding = nn.Embedding(
            num_embeddings=input_vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=0  # Padding token is 0
        )
        
        # ─── 1D Convolutions ───
        # Extract local patterns at different scales
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
                    dilation=1
                )
            )
            in_channels = out_channels
        
        # ─── Bidirectional LSTM ───
        # Capture long-range sequential patterns
        self.lstm = nn.LSTM(
            input_size=conv_channels[-1],
            hidden_size=lstm_hidden,
            num_layers=2,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if dropout > 0 else 0
        )
        
        # Note: LSTM output size is 2 * lstm_hidden (due to bidirectional)
        lstm_output_size = 2 * lstm_hidden
        
        # ─── Projection to Output Dimension ───
        self.projection = nn.Linear(lstm_output_size, output_dim)
        
        # ─── Regularization ───
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(output_dim)
        
    def forward(self, raw_input: torch.Tensor) -> torch.Tensor:
        """
        Args:
            raw_input: Tensor of shape (batch_size, seq_len)
                      Values in range [0, 256) representing byte values
                      Padding should be 0
        
        Returns:
            encoded: Tensor of shape (batch_size, output_dim)
                    Semantic features extracted from input
        """
        # (batch, seq_len) → (batch, seq_len, embedding_dim)
        x = self.embedding(raw_input)
        x = self.dropout(x)
        
        # (batch, seq_len, embedding_dim) → (batch, embedding_dim, seq_len)
        # Conv1d expects (N, C, L) format
        x = x.transpose(1, 2)
        
        # Apply stacked convolutions
        for i, conv in enumerate(self.conv_layers):
            x = conv(x)
            x = F.relu(x)
            x = self.dropout(x)
        
        # (batch, conv_channels[-1], seq_len) → (batch, seq_len, conv_channels[-1])
        x = x.transpose(1, 2)
        
        # Bidirectional LSTM
        # Returns (output, (h_n, c_n))
        lstm_out, (h_n, c_n) = self.lstm(x)
        
        # lstm_out shape: (batch, seq_len, 2*lstm_hidden)
        # We use max pooling over sequence dimension for aggregation
        # Alternative: use attention, but max-pooling is simpler and effective
        pooled = torch.max(lstm_out, dim=1)[0]  # (batch, 2*lstm_hidden)
        
        # Project to output dimension
        encoded = self.projection(pooled)  # (batch, output_dim)
        encoded = self.layer_norm(encoded)
        
        return encoded


class ActionSequenceEncoder(nn.Module):
    """
    Encodes recent mutation action history into features.
    
    This captures which mutations were applied recently,
    helping the agent understand "we've been doing byte_flip
    for 3 steps, maybe try something else".
    
    Input: (batch_size, seq_len) - action indices (0-3)
    Output: (batch_size, output_dim)
    """
    
    def __init__(self, 
                 num_actions: int = 4,
                 seq_len: int = 8,
                 embedding_dim: int = 8,
                 output_dim: int = 64):
        super().__init__()
        
        self.seq_len = seq_len
        
        # Embed each action index to a vector
        self.action_embedding = nn.Embedding(
            num_embeddings=num_actions,
            embedding_dim=embedding_dim
        )
        
        # LSTM to process action sequence
        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=output_dim // 2,
            num_layers=1,
            bidirectional=True,
            batch_first=True
        )
        
        self.output_dim = output_dim
        
    def forward(self, actions: torch.Tensor) -> torch.Tensor:
        """
        Args:
            actions: (batch_size, seq_len) - action indices
            
        Returns:
            (batch_size, output_dim) - encoded action history
        """
        # Embed actions
        x = self.action_embedding(actions)  # (batch, seq_len, embedding_dim)
        
        # LSTM over action sequence
        lstm_out, (h_n, c_n) = self.lstm(x)  # (batch, seq_len, output_dim)
        
        # Use last hidden state as the encoding
        # (last output of LSTM captures the entire sequence)
        encoded = lstm_out[:, -1, :]  # (batch, output_dim)
        
        return encoded
```

---

### Step 1.2: Create Enhanced Actor-Critic Network (`agent/ppo_agent_lstm.py`)

```python
"""
ppo_agent_lstm.py
LSTM-Enhanced Actor-Critic for Adaptive Fuzzing

Combines:
- Input encoder (learns input structure)
- Action sequence encoder (learns mutation patterns)
- Bidirectional LSTM (tracks temporal dependencies)
- Actor & Critic heads (policy and value function)
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from agent.input_encoder import InputEncoder, ActionSequenceEncoder


class LSTMActorCritic(nn.Module):
    """
    Actor-Critic network with LSTM memory for RL-guided fuzzing.
    
    The network processes:
    1. Coverage observation (67 floats)
    2. Raw input bytes (up to 1024 bytes)
    3. Recent action history (last 8 actions)
    
    And produces:
    1. Action distribution (for actor)
    2. Value estimate (for critic)
    3. Updated LSTM hidden state (for recurrency)
    """
    
    def __init__(self,
                 obs_size: int = 67,
                 max_input_len: int = 1024,
                 n_actions: int = 4,
                 lstm_hidden: int = 256,
                 lstm_layers: int = 2,
                 dropout: float = 0.1):
        
        super().__init__()
        
        self.obs_size = obs_size
        self.max_input_len = max_input_len
        self.n_actions = n_actions
        self.lstm_hidden = lstm_hidden
        self.lstm_layers = lstm_layers
        
        # ─── Input Encoders ───
        
        # 1. Raw input encoder
        self.input_encoder = InputEncoder(
            input_vocab_size=256,
            embedding_dim=32,
            conv_channels=[64, 64, 32],
            lstm_hidden=128,
            output_dim=256,
            dropout=dropout
        )
        
        # 2. Action history encoder
        self.action_encoder = ActionSequenceEncoder(
            num_actions=n_actions,
            seq_len=8,
            embedding_dim=8,
            output_dim=64
        )
        
        # ─── Feature concatenation ───
        # Total features = obs + input_encoded + action_encoded
        # = 67 + 256 + 64 = 387
        total_feature_size = obs_size + 256 + 64
        
        # ─── Main LSTM ───
        self.lstm = nn.LSTM(
            input_size=total_feature_size,
            hidden_size=lstm_hidden,
            num_layers=lstm_layers,
            batch_first=True,
            dropout=dropout if lstm_layers > 1 else 0
        )
        
        # ─── Policy Head (Actor) ───
        self.actor = nn.Sequential(
            nn.Linear(lstm_hidden, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, n_actions)
        )
        
        # ─── Value Head (Critic) ───
        self.critic = nn.Sequential(
            nn.Linear(lstm_hidden, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 1)
        )
        
        # Initialize weights
        for module in [self.actor, self.critic]:
            for layer in module:
                if isinstance(layer, nn.Linear):
                    nn.init.orthogonal_(layer.weight, gain=np.sqrt(2))
                    nn.init.constant_(layer.bias, 0)
    
    def forward(self,
                obs: torch.Tensor,
                raw_input: torch.Tensor,
                action_history: torch.Tensor,
                hidden_state: tuple = None):
        """
        Forward pass producing action logits and value estimate.
        
        Args:
            obs: (batch_size, obs_size) - coverage observation
            raw_input: (batch_size, max_input_len) - raw input bytes
            action_history: (batch_size, 8) - last 8 actions (indices 0-3)
            hidden_state: tuple of (h, c) for LSTM or None
            
        Returns:
            action_logits: (batch_size, n_actions)
            value: (batch_size, 1)
            new_hidden_state: updated LSTM state for next step
        """
        batch_size = obs.shape[0]
        
        # Encode each input component
        encoded_input = self.input_encoder(raw_input)  # (batch, 256)
        encoded_actions = self.action_encoder(action_history)  # (batch, 64)
        
        # Concatenate all features
        combined = torch.cat([obs, encoded_input, encoded_actions], dim=1)
        combined = combined.unsqueeze(1)  # (batch, 1, total_features) for LSTM
        
        # Process through LSTM
        lstm_out, new_hidden_state = self.lstm(combined, hidden_state)
        lstm_features = lstm_out[:, -1, :]  # (batch, lstm_hidden)
        
        # Compute action logits and value
        action_logits = self.actor(lstm_features)  # (batch, n_actions)
        value = self.critic(lstm_features)          # (batch, 1)
        
        return action_logits, value, new_hidden_state


class PPOAgentLSTM:
    """
    PPO Agent with LSTM memory and semantic input encoding.
    
    Maintains LSTM hidden state across episodes for temporal consistency.
    Updates policy every N steps using collected rollout data.
    """
    
    def __init__(self,
                 obs_size: int = 67,
                 max_input_len: int = 1024,
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
                 lstm_layers: int = 2):
        
        self.obs_size = obs_size
        self.max_input_len = max_input_len
        self.n_actions = n_actions
        self.gamma = gamma
        self.clip_epsilon = clip_epsilon
        self.entropy_coef = entropy_coef
        self.value_coef = value_coef
        self.max_grad_norm = max_grad_norm
        self.ppo_epochs = ppo_epochs
        self.batch_size = batch_size
        
        # Device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Network
        self.network = LSTMActorCritic(
            obs_size=obs_size,
            max_input_len=max_input_len,
            n_actions=n_actions,
            lstm_hidden=lstm_hidden,
            lstm_layers=lstm_layers
        ).to(self.device)
        
        self.optimizer = optim.Adam(self.network.parameters(), lr=lr)
        
        # LSTM hidden state (to be reset at episode start)
        self.hidden_state = None
    
    def reset_hidden_state(self):
        """Reset LSTM hidden state at episode start."""
        self.hidden_state = None
    
    def get_action(self, obs: np.ndarray, raw_input: np.ndarray, 
                   action_history: np.ndarray):
        """
        Select an action given current observation.
        
        Args:
            obs: (67,) coverage observation
            raw_input: (max_input_len,) raw input bytes
            action_history: (8,) last 8 actions
            
        Returns:
            action: selected action (0-3)
            log_prob: log probability of selected action
            value: value estimate for this state
        """
        # Convert to tensors
        obs_tensor = torch.FloatTensor(obs).unsqueeze(0).to(self.device)
        input_tensor = torch.LongTensor(raw_input).unsqueeze(0).to(self.device)
        action_tensor = torch.LongTensor(action_history).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            logits, value, self.hidden_state = self.network(
                obs_tensor, input_tensor, action_tensor, self.hidden_state
            )
            
            probs = torch.softmax(logits, dim=-1)
            dist = torch.distributions.Categorical(probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)
        
        return action.item(), log_prob.item(), value.item()
    
    def update(self, rollout_buffer):
        """
        Perform PPO policy update using collected rollout data.
        
        Args:
            rollout_buffer: RolloutBufferLSTM with computed advantages
            
        Returns:
            Dict with training metrics
        """
        total_policy_loss = 0.0
        total_value_loss = 0.0
        total_entropy = 0.0
        n_updates = 0
        
        for epoch in range(self.ppo_epochs):
            for batch in rollout_buffer.get_batches(self.batch_size):
                obs = batch["obs"].float().to(self.device)
                raw_input = batch["raw_input"].long().to(self.device)
                actions = batch["actions"].long().to(self.device)
                action_history = batch["action_history"].long().to(self.device)
                old_log_probs = batch["log_probs"].to(self.device)
                advantages = batch["advantages"].to(self.device)
                returns = batch["returns"].to(self.device)
                
                # Normalize advantages
                if len(advantages) > 1:
                    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
                
                # Forward pass (without hidden state - batch processing)
                logits, values, _ = self.network(obs, raw_input, action_history)
                
                probs = torch.softmax(logits, dim=-1)
                dist = torch.distributions.Categorical(probs)
                new_log_probs = dist.log_prob(actions)
                entropy = dist.entropy().mean()
                
                # PPO clipped objective
                ratio = torch.exp(new_log_probs - old_log_probs)
                surr1 = ratio * advantages
                surr2 = torch.clamp(ratio, 1 - self.clip_epsilon,
                                    1 + self.clip_epsilon) * advantages
                policy_loss = -torch.min(surr1, surr2).mean()
                
                # Value loss (MSE)
                value_loss = 0.5 * (values.squeeze() - returns).pow(2).mean()
                
                # Total loss
                loss = policy_loss + self.value_coef * value_loss - self.entropy_coef * entropy
                
                # Backward
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.network.parameters(), self.max_grad_norm)
                self.optimizer.step()
                
                # Tracking
                total_policy_loss += policy_loss.item()
                total_value_loss += value_loss.item()
                total_entropy += entropy.item()
                n_updates += 1
        
        return {
            "policy_loss": total_policy_loss / max(n_updates, 1),
            "value_loss": total_value_loss / max(n_updates, 1),
            "entropy": total_entropy / max(n_updates, 1),
        }
```

---

### Step 1.3: Create LSTM-Aware Rollout Buffer

```python
"""
replay_buffer_lstm.py
Rollout buffer that tracks raw input + action sequences for LSTM training
"""

class RolloutBufferLSTM:
    """
    Buffer for PPO that stores raw inputs and action history for LSTM
    """
    
    def __init__(self, buffer_size: int, obs_size: int,
                 max_input_len: int = 1024,
                 gamma: float = 0.99, gae_lambda: float = 0.95):
        self.buffer_size = buffer_size
        self.obs_size = obs_size
        self.max_input_len = max_input_len
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        
        # Pre-allocate storage
        self.states = np.zeros((buffer_size, obs_size), dtype=np.float32)
        self.raw_inputs = np.zeros((buffer_size, max_input_len), dtype=np.int64)
        self.action_history = np.zeros((buffer_size, 8), dtype=np.int64)
        self.actions = np.zeros(buffer_size, dtype=np.int64)
        self.rewards = np.zeros(buffer_size, dtype=np.float32)
        self.log_probs = np.zeros(buffer_size, dtype=np.float32)
        self.values = np.zeros(buffer_size, dtype=np.float32)
        self.dones = np.zeros(buffer_size, dtype=np.float32)
        
        self.advantages = np.zeros(buffer_size, dtype=np.float32)
        self.returns = np.zeros(buffer_size, dtype=np.float32)
        
        self.ptr = 0
        self.full = False
    
    def store(self, state, raw_input, action_history, action, reward, log_prob, value, done):
        """Store transition including raw input and action history"""
        self.states[self.ptr] = state
        
        # Pad/truncate raw input to max length
        if len(raw_input) > self.max_input_len:
            self.raw_inputs[self.ptr] = raw_input[:self.max_input_len]
        else:
            self.raw_inputs[self.ptr, -len(raw_input):] = raw_input
        
        self.action_history[self.ptr] = action_history
        self.actions[self.ptr] = action
        self.rewards[self.ptr] = reward
        self.log_probs[self.ptr] = log_prob
        self.values[self.ptr] = value
        self.dones[self.ptr] = float(done)
        
        self.ptr += 1
        if self.ptr >= self.buffer_size:
            self.full = True
    
    def get_batches(self, batch_size):
        """Yield mini-batches as PyTorch tensors"""
        size = self.ptr if not self.full else self.buffer_size
        indices = np.random.permutation(size)
        
        import torch
        for start in range(0, size, batch_size):
            end = min(start + batch_size, size)
            batch_idx = indices[start:end]
            
            yield {
                "obs": torch.FloatTensor(self.states[batch_idx]),
                "raw_input": torch.LongTensor(self.raw_inputs[batch_idx]),
                "action_history": torch.LongTensor(self.action_history[batch_idx]),
                "actions": torch.LongTensor(self.actions[batch_idx]),
                "log_probs": torch.FloatTensor(self.log_probs[batch_idx]),
                "advantages": torch.FloatTensor(self.advantages[batch_idx]),
                "returns": torch.FloatTensor(self.returns[batch_idx]),
            }
```

---

## SECTION 2: ENHANCED TRAINING LOOP

### Step 2.1: Create LSTM-Aware Environment

Modify `environment/fuzz_env_lstm.py` to track action history:

```python
"""
LSTM-aware fuzzing environment that tracks:
1. Last 8 actions
2. Current input bytes
3. Coverage bitmap
"""

class FuzzEnvLSTM(gym.Env):
    def __init__(self, target_path, seed_path, ...):
        # ... existing init ...
        self.action_history = np.zeros(8, dtype=np.int64)
        self.current_input = bytearray()
    
    def reset(self, seed=None, options=None):
        obs, info = super().reset(seed, options)
        self.action_history.fill(0)
        return obs, info
    
    def step(self, action):
        # ... existing step logic ...
        
        # Update action history (shift left, add new action)
        self.action_history = np.roll(self.action_history, -1)
        self.action_history[-1] = action
        
        # Include raw input in info
        info["raw_input"] = np.array(self.current_input, dtype=np.int64)
        info["action_history"] = self.action_history.copy()
        
        return obs, reward, terminated, truncated, info
```

---

## SECTION 3: GUI BACKEND (FASTAPI)

### Step 3.1: Setup FastAPI Server

```bash
pip install fastapi uvicorn websockets sqlalchemy redis
```

### Step 3.2: Create Backend (backend/main.py)

```python
"""
FastAPI backend for Fuzzinator Dashboard

Provides:
- WebSocket streaming of metrics
- REST API for crashes, logs, config
- Coordination with training loop via IPC queue
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
from datetime import datetime
from queue import Queue
import threading

app = FastAPI(title="Fuzzinator Dashboard API")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Global State ───
training_queue = None  # Queue from training loop
metrics_cache = {}
connected_clients = set()

@app.lifespan("startup")
async def startup():
    # Initialize database
    # Start background task to consume training queue
    pass

# ─── WebSocket ───
@app.websocket("/ws/metrics")
async def websocket_metrics(ws: WebSocket):
    """Stream live metrics every 1 second"""
    await ws.accept()
    connected_clients.add(ws)
    
    try:
        while True:
            # Get latest metrics from queue or cache
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "step": metrics_cache.get("step", 0),
                "reward": metrics_cache.get("reward", 0.0),
                "new_edges": metrics_cache.get("new_edges", 0),
                "total_edges": metrics_cache.get("total_edges", 0),
                "crashes": metrics_cache.get("crashes", 0),
                "coverage_buckets": metrics_cache.get("coverage_buckets", [0]*64),
                "current_action": metrics_cache.get("action", 0),
                "fps": metrics_cache.get("fps", 0.0),
            }
            
            await ws.send_json(metrics)
            await asyncio.sleep(1)
    
    except Exception as e:
        connected_clients.discard(ws)

# ─── REST Endpoints ───
@app.get("/api/stats")
def get_stats():
    """Campaign statistics"""
    return {
        "total_steps": metrics_cache.get("step", 0),
        "total_reward": metrics_cache.get("total_reward", 0.0),
        "unique_crashes": metrics_cache.get("crashes", 0),
        "unique_edges": metrics_cache.get("total_edges", 0),
        "uptime_seconds": metrics_cache.get("uptime", 0),
    }

@app.get("/api/crashes")
def get_crashes(limit: int = 50):
    """List recent crashes"""
    # Query database
    return {
        "crashes": [
            {
                "id": "crash_1",
                "timestamp": "2026-03-17T14:23:45Z",
                "signal": "SIGSEGV",
                "size": 247,
            }
        ]
    }

@app.post("/api/config")
def update_config(config: dict):
    """Update runtime parameters"""
    # Send to training loop via queue
    pass

@app.get("/api/status")
def get_status():
    """Current campaign status"""
    return {
        "status": "running",
        "target": "/path/to/target",
        "started_at": "2026-03-17T14:23:00Z",
    }
```

---

## SECTION 4: GUI FRONTEND (REACT)

### Step 4.1: Setup React Project

```bash
npx create-react-app fuzzinator-dashboard --template typescript
cd fuzzinator-dashboard
npm install recharts axios zustand
```

### Step 4.2: Create Main Components

**src/components/CoverageBitmap.tsx:**
```tsx
import React from 'react';

interface CoverageBitmapProps {
  buckets: number[]; // Array of 64 coverage values
  maxValue: number;
  newThisStep: number;
}

export const CoverageBitmap: React.FC<CoverageBitmapProps> = ({
  buckets,
  maxValue,
  newThisStep,
}) => {
  const getColor = (value: number) => {
    const ratio = value / maxValue;
    if (ratio > 0.7) return '#22c55e'; // Green - high coverage
    if (ratio > 0.4) return '#eab308'; // Yellow - medium
    if (ratio > 0.1) return '#f97316'; // Orange - low
    return '#cbd5e1'; // Gray - none
  };

  return (
    <div className="coverage-bitmap">
      <h3>Coverage Heatmap ({newThisStep} new this step)</h3>
      <div className="bitmap-container">
        {buckets.map((value, index) => (
          <div
            key={index}
            className="bitmap-bucket"
            style={{ backgroundColor: getColor(value) }}
            title={`Bucket ${index}: ${value} edges`}
          />
        ))}
      </div>
      <div className="legend">
        <span>█ High</span>
        <span>▓ Medium</span>
        <span>░ Low</span>
        <span>▒ None</span>
      </div>
    </div>
  );
};
```

**src/components/MetricsPanel.tsx:**
```tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

interface MetricsPanelProps {
  data: Array<{ step: number; reward: number; timestamp: string }>;
}

export const MetricsPanel: React.FC<MetricsPanelProps> = ({ data }) => {
  return (
    <div className="metrics-panel">
      <h3>Reward Over Time</h3>
      <LineChart width={600} height={300} data={data}>
        <XAxis dataKey="step" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="reward" stroke="#3b82f6" isAnimationActive={true} />
      </LineChart>
    </div>
  );
};
```

---

## SECTION 5: DATABASE SCHEMA

```sql
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    step INTEGER NOT NULL,
    reward REAL NOT NULL,
    new_edges INTEGER,
    total_edges INTEGER,
    crashes INTEGER,
    fps REAL
);

CREATE TABLE IF NOT EXISTS crashes (
    id TEXT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    signal_name TEXT,
    input_data BLOB,
    input_size INTEGER,
    root_cause TEXT
);

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    level TEXT,
    message TEXT
);

CREATE INDEX idx_metrics_step ON metrics(step);
CREATE INDEX idx_crashes_timestamp ON crashes(timestamp);
```

---

## SECTION 6: QUICK START

### Install Dependencies:
```bash
pip install -r requirements.txt torch torchvision torchaudio
pip install fastapi uvicorn websockets sqlalchemy
cd dashboard && npm install
```

### Start Backend:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### Start Frontend:
```bash
cd dashboard
npm start  # Runs on http://localhost:3000
```

### Start Training (with LSTM):
```bash
python agent/train_lstm.py --target targets/target_buffer_overflow
```

---

## SECTION 7: TESTING CHECKLIST

- [ ] LSTM forward pass produces correct shapes
- [ ] Input encoder handles variable-length inputs
- [ ] Action history tracking works  
- [ ] Hidden state persists across steps
- [ ] WebSocket streams metrics without lag
- [ ] Coverage bitmap updates in real-time
- [ ] Crash vault stores and retrieves crashes
- [ ] Config changes propagate to training loop
- [ ] Dashboard responsive on mobile
- [ ] Training loop integrates with FastAPI

---

**Ready to implement!** Start with input_encoder.py, then ppo_agent_lstm.py, then the training loop modifications.

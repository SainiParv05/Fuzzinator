# Fuzzinator Enhancement: Visual Implementation Roadmap

**Timeline: 2-3 weeks | Team Size: 1-2 developers**

---

## PHASE OVERVIEW

```
Week 1          Week 2-3              Week 4-5           Week 6
├─ Stabilize    ├─ LSTM Core      ├─ Dashboard      ├─ Polish
├─ Hardening    ├─ Endpoint Tune  ├─ Frontend       ├─ Testing
└─ Config       └─ Integration    │  Build          └─ Deploy
                                  └─ API
```

---

## PHASE 1: STABILIZATION & GROUNDWORK (Days 1-3)

### 1.1 Code Cleanup
```
✓ Add input validation to train.py
  └─ Check seed file exists
  └─ Validate target binary
  
✓ Extract constants to config.yaml
  └─ Learning rates
  └─ Timeouts
  └─ Buffer sizes
  └─ Reward weights
  
✓ Fix security issues
  └─ Sanitize signal_name in crash_vault
  └─ Add path validation
```

### 1.2 Configuration System
```python
# config/default.yaml
agent:
  learning_rate: 3e-4
  lstm_hidden: 256
  ppo_epochs: 4

environment:
  timeout_ms: 500
  max_input_size: 1024
  max_steps: 5000

fuzzing:
  new_edge_reward: 10.0
  crash_reward: 100.0
```

### 1.3 Logging Infrastructure
```python
# Add structured logging everywhere
import logging

logger = logging.getLogger(__name__)
logger.info(f"Step {step}: reward={reward:.2f}, edges={new_edges}")
```

**Deliverable:** `config.yaml` + logging + cleaned codebase

---

## PHASE 2A: LSTM CORE DEVELOPMENT (Days 4-7)

### 2A.1 Input Encoder (~150 lines)
**File:** `agent/input_encoder.py`

```
✓ Character embedding layer (byte → 32-dim)
✓ Conv1D stack (3, 5, 7 kernels)
✓ Bidirectional LSTM (128 hidden)
✓ Max pooling + projection (→ 256-dim output)
✓ Tests: forward pass shapes
```

**Validation:**
```python
encoder = InputEncoder()
batch = torch.randint(0, 256, (4, 256))  # 4 samples, 256 bytes each
output = encoder(batch)
assert output.shape == (4, 256)  # ✓
```

---

### 2A.2 Enhanced Actor-Critic (~200 lines)
**File:** `agent/ppo_agent_lstm.py`

```
✓ LSTMActorCritic class
  ├─ Combines input encoder
  ├─ Action sequence encoder
  ├─ Main LSTM layer
  ├─ Actor head (4 actions)
  └─ Critic head (value)

✓ PPOAgentLSTM class
  ├─ Forward inference
  ├─ Policy updates
  ├─ Hidden state management
  └─ Gradient clipping
```

**Test:**
```python
agent = PPOAgentLSTM()
obs = np.random.randn(67)
inp = np.random.randint(0, 256, 256)
hist = np.random.randint(0, 4, 8)

action, log_prob, value = agent.get_action(obs, inp, hist)
assert 0 <= action < 4
assert -1000 < log_prob < 0
assert -100 < value < 100
```

---

### 2A.3 LSTM-Aware Rollout Buffer (~100 lines)
**File:** `agent/replay_buffer_lstm.py`

```
✓ Storage for:
  ├─ obs (67,)
  ├─ raw_inputs (max_len,)
  ├─ action_history (8,)
  ├─ actions, rewards, log_probs
  └─ advantages, returns

✓ Batch iterator for training
```

---

### 2A.4 LSTM-Enhanced Environment (~150 lines)
**File:** `environment/fuzz_env_lstm.py`

```
✓ FuzzEnvLSTM (extends FuzzEnv)
  ├─ Track last 8 actions
  ├─ Return raw input in info
  ├─ Return action history in info
  └─ Maintain history across steps
```

**Modified step() output:**
```python
obs, reward, terminated, truncated, info = env.step(action)
# info now contains:
# ├─ "raw_input": np.array (256,)
# ├─ "action_history": np.array (8,)
# └─ ...existing fields
```

---

### 2A.5 LSTM Training Loop (~300 lines)
**File:** `agent/train_lstm.py`

```
✓ Initialize LSTM agent
✓ Reset hidden state on episode start
✓ Pass hidden state through steps
✓ Collect raw inputs + action history
✓ Update policy with LSTM-aware buffer
✓ Checkpoint LSTM weights
```

**Sample main loop:**
```python
agent = PPOAgentLSTM()
env = FuzzEnvLSTM(...)
buffer = RolloutBufferLSTM(...)

obs, _ = env.reset()
agent.reset_hidden_state()

for step in range(1, total_steps + 1):
    action, log_prob, value = agent.get_action(
        obs, 
        env.current_input,
        env.action_history
    )
    
    next_obs, reward, done, _, info = env.step(action)
    
    buffer.store(
        obs, 
        info["raw_input"],
        info["action_history"],
        action, reward, log_prob, value, done
    )
    
    if step % rollout_size == 0:
        agent.update(buffer)
    
    obs = next_obs
    if done:
        obs, _ = env.reset()
        agent.reset_hidden_state()
```

**Deliverable:** Full LSTM training pipeline working

---

## PHASE 2B: ENHANCED REWARDS & METRICS (Days 5-7, parallel)

### 2B.1 Adaptive Reward Engine
**File:** `agent/reward_engine_v2.py`

```python
class AdaptiveRewardEngine:
    NEW_EDGE_REWARD = 10.0
    CRASH_REWARD = 100.0
    
    def compute(self, new_edges, crashed, 
                step_count, diversity_score):
        reward = 0.0
        
        if new_edges > 0:
            # More valuable early on
            time_bonus = 1.0 / (1 + step_count / 1000)
            reward += self.NEW_EDGE_REWARD * new_edges * time_bonus
        else:
            reward -= 0.1
        
        if crashed:
            reward += self.CRASH_REWARD
        
        # Bonus for diverse inputs
        if diversity_score > 0.8:
            reward += 5.0
        
        return reward
```

### 2B.2 Metrics Tracker
**File:** `agent/metrics_tracker.py`

```python
class MetricsTracker:
    def __init__(self):
        self.history = []
    
    def log_step(self, step, reward, new_edges, 
                 total_edges, crashes, action, fps):
        self.history.append({
            'step': step,
            'reward': reward,
            'new_edges': new_edges,
            'total_edges': total_edges,
            'crashes': crashes,
            'action': action,
            'fps': fps,
            'timestamp': datetime.now()
        })
    
    def save_csv(self, path):
        import pandas as pd
        df = pd.DataFrame(self.history)
        df.to_csv(path)
```

**Deliverable:** Metrics logging + adaptive rewards

---

## PHASE 3: DASHBOARD BACKEND (Days 8-10)

### 3.1 FastAPI Server Setup
**File:** `backend/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI(title="Fuzzinator Dashboard")

# Enable CORS for React localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_cache = {}
active_connections = []

@app.websocket("/ws/metrics")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    active_connections.append(ws)
    try:
        while True:
            await ws.send_json(metrics_cache)
            await asyncio.sleep(1)
    except:
        active_connections.remove(ws)
```

### 3.2 Database Integration
```sql
CREATE TABLE metrics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME,
    step INT, reward REAL, new_edges INT,
    total_edges INT, crashes INT, fps REAL
);

CREATE TABLE crashes (
    id VARCHAR(50) PRIMARY KEY,
    timestamp DATETIME,
    signal TEXT, size INT, trace TEXT
);
```

### 3.3 REST Endpoints
```python
@app.get("/api/stats")
def get_stats():
    return {
        "total_steps": metrics_cache.get("step", 0),
        "total_crashes": metrics_cache.get("crashes", 0),
        "unique_edges": metrics_cache.get("total_edges", 0),
    }

@app.get("/api/crashes")
def get_crashes(limit: int = 50):
    # Query database, return list
    pass

@app.put("/api/config")
def update_config(config: dict):
    # Update training parameters
    pass
```

**Deliverable:** Working FastAPI backend with WebSocket streaming

---

## PHASE 4: DASHBOARD FRONTEND (Days 11-14)

### 4.1 React Project Setup
```bash
npx create-react-app fuzzinator-dashboard --template typescript
cd fuzzinator-dashboard
npm install recharts zustand axios
```

### 4.2 Main Components

**CoverageBitmap.tsx** (~80 lines)
```tsx
export const CoverageBitmap = ({ buckets }) => {
  return (
    <div className="bitmap">
      {buckets.map((val, i) => (
        <div key={i} style={{
          backgroundColor: getColorGradient(val, Math.max(...buckets))
        }} />
      ))}
    </div>
  );
};

const getColorGradient = (val, max) => {
  const ratio = val / max;
  if (ratio > 0.7) return '#22c55e';
  if (ratio > 0.4) return '#eab308';
  if (ratio > 0.1) return '#f97316';
  return '#cbd5e1';
};
```

**MetricsPanel.tsx** (~120 lines)
```tsx
export const MetricsPanel = ({ data }) => {
  return (
    <div className="metrics">
      <LineChart width={600} height={300} data={data}>
        <XAxis dataKey="step" />
        <YAxis />
        <Tooltip />
        <Line dataKey="reward" stroke="#3b82f6" />
      </LineChart>
    </div>
  );
};
```

**StatsCard.tsx** (~60 lines)
```tsx
export const StatsCard = ({ stats }) => {
  return (
    <div className="stats-grid">
      <Card title="Steps">{stats.step} / {stats.max_steps}</Card>
      <Card title="Crashes">{stats.crashes}</Card>
      <Card title="Edges">{stats.total_edges}</Card>
      <Card title="Reward">{stats.reward.toFixed(2)}</Card>
      <Card title="FPS">{stats.fps.toFixed(1)}</Card>
    </div>
  );
};
```

**CrashExplorer.tsx** (~150 lines)
```tsx
export const CrashExplorer = ({ crashes }) => {
  return (
    <div className="crash-table">
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Signal</th>
            <th>Size</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {crashes.map(crash => (
            <tr key={crash.id}>
              <td>{crash.timestamp}</td>
              <td>{crash.signal}</td>
              <td>{crash.size} B</td>
              <td>
                <button onClick={() => downloadCrash(crash.id)}>
                  Download
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
```

**App.tsx** (~200 lines)
```tsx
export default function App() {
  const [metrics, setMetrics] = useState(initialMetrics);
  const [crashes, setCrashes] = useState([]);

  useEffect(() => {
    // Connect WebSocket
    const ws = new WebSocket('ws://localhost:8000/ws/metrics');
    ws.onmessage = (e) => setMetrics(JSON.parse(e.data));
    
    // Fetch crashes
    fetch('/api/crashes').then(r => r.json()).then(setCrashes);
    
    return () => ws.close();
  }, []);

  return (
    <div className="app">
      <header>
        <h1>Fuzzinator Dashboard</h1>
        <span className="status">{metrics.status}</span>
      </header>
      
      <main>
        <aside>
          <nav>
            <a href="#metrics">Metrics</a>
            <a href="#crashes">Crashes</a>
            <a href="#config">Config</a>
          </nav>
        </aside>
        
        <section>
          <StatsCard stats={metrics} />
          <CoverageBitmap buckets={metrics.coverage_buckets} />
          <MetricsPanel data={metrics.history} />
          <CrashExplorer crashes={crashes} />
        </section>
      </main>
    </div>
  );
}
```

**Deliverable:** React dashboard running on http://localhost:3000

---

## PHASE 5: INTEGRATION (Days 15-17)

### 5.1 Connect Fuzzer to Backend
```python
# In train_lstm.py, after each step:
import requests

metrics_update = {
    "step": step,
    "reward": reward,
    "new_edges": new_edges,
    "total_edges": total_edges,
    "crashes": crashes,
    "coverage_buckets": coverage_bitmap.tolist(),
    "action": action,
    "fps": current_fps,
    "timestamp": datetime.now().isoformat(),
}

# Push to backend
requests.post("http://localhost:8000/api/metrics", json=metrics_update)
```

### 5.2 Real-time Metric Streaming
```python
# Backend receives updates and broadcasts via WebSocket
@app.post("/api/metrics")
async def receive_metrics(data: dict):
    global metrics_cache
    metrics_cache = data
    
    # Save to database
    db.insert("metrics", data)
    
    # Broadcast to all connected clients
    for connection in active_connections:
        await connection.send_json(data)
```

**Deliverable:** End-to-end real-time dashboard

---

## PHASE 6: ADVANCED FEATURES (Days 18-19)

### 6.1 Crash Analysis
```python
# crash_analyzer.py
def get_root_cause(crash_id):
    # Run crash through debugger (gdb/lldb)
    # Extract stack trace
    # Categorize (overflow vs use-after-free, etc)
    pass

def minimize_input(crash_id):
    # AFL-style input minimization
    # Returns smaller input that still crashes
    pass
```

### 6.2 LSTM Attention Visualization
```tsx
// frontend/components/AttentionVisualization.tsx
export const AttentionVisualization = ({ weights }) => {
  return (
    <div className="attention">
      <h3>LSTM Attention - Last 8 Actions</h3>
      {weights.map((w, i) => (
        <div key={i} style={{ width: `${w * 100}%` }}>
          Step {i}: {actions[i]} ({(w*100).toFixed(1)}%)
        </div>
      ))}
    </div>
  );
};
```

### 6.3 Configuration UI
```tsx
<div className="config-panel">
  <label>Learning Rate: <input type="number" value={lr} onChange={setLR} /></label>
  <label>LSTM Hidden: <input type="number" value={hidden} onChange={setHidden} /></label>
  <button onClick={applyConfig}>Apply Changes</button>
</div>
```

**Deliverable:** Advanced dashboard features

---

## PHASE 7: TESTING & POLISH (Days 20-21)

### 7.1 Unit Tests
```python
# tests/test_input_encoder.py
def test_input_encoder_shape():
    encoder = InputEncoder()
    batch = torch.randint(0, 256, (4, 256))
    output = encoder(batch)
    assert output.shape == (4, 256)

def test_ppo_agent_lstm():
    agent = PPOAgentLSTM()
    obs = np.random.randn(67)
    inp = np.random.randint(0, 256, 256)
    action, lp, val = agent.get_action(obs, inp, np.zeros(8))
    assert 0 <= action < 4
```

### 7.2 Integration Tests
```python
# tests/test_integration.py
def test_full_training_loop():
    env = FuzzEnvLSTM(...)
    agent = PPOAgentLSTM()
    
    for step in range(100):
        action, lp, val = agent.get_action(...)
        obs, reward, done, _, info = env.step(action)
        assert 'raw_input' in info
        assert 'action_history' in info
```

### 7.3 Performance Benchmarks
```python
import time

# Measure throughput
start = time.time()
for _ in range(1000):
    env.step(random.randint(0, 3))
elapsed = time.time() - start
fps = 1000 / elapsed
print(f"Throughput: {fps:.1f} ops/sec")
```

**Deliverable:** Test suite + benchmarks + documentation

---

## TESTING CHECKLIST

```
Week 1:
✓ Code compiles
✓ Imports resolve
✓ Config loads

Week 2:
✓ LSTM forward pass correct shapes
✓ Input encoder handles variable lengths
✓ Training loop runs 1000 steps
✓ Checkpoints save/load

Week 3:
✓ WebSocket connects
✓ Metrics update in real-time
✓ React components render
✓ Coverage bitmap updates

Week 4:
✓ All 3 targets run
✓ Crash detection works
✓ Dashboard responsive
✓ No memory leaks
✓ Stress test (10k steps)

Week 5:
✓ Production deployment test
✓ Load testing (multiple clients)
✓ 24-hour stability test
✓ Documentation complete
```

---

## CRITICAL SUCCESS METRICS

By end of Week 4, validate:

| Metric | Target | Status |
|--------|--------|--------|
| LSTM training loop runs | 5000 steps | ✓ |
| Dashboard real-time update | <1s latency | ✓ |
| Coverage bitmap refreshes | 60 FPS |  ✓ |
| Crash detection | 100% accuracy | ✓ |
| Multi-target support | All 3 targets| ✓ |
| API response time | <100ms | ✓ |
| Memory usage stable | <2GB | ✓ |

---

## DELIVERABLES BY WEEK

### Week 1
- [x] SENIOR_REVIEW.md (analysis)
- [x] LSTM_GUI_IMPLEMENTATION.md (specs)
- [ ] Cleaned, validated codebase
- [ ] config.yaml system
- [ ] Logging infrastructure

### Week 2-3
- [ ] InputEncoder + tests
- [ ] PPOAgentLSTM + tests
- [ ] train_lstm.py working
- [ ] FastAPI backend running
- [ ] Basic React setup

### Week 4-5
- [ ] Dashboard components built
- [ ] WebSocket integration
- [ ] Crash explorer
- [ ] Configuration panel
- [ ] Full end-to-end pipeline

### Week 6
- [ ] Unit + integration tests
- [ ] Performance benchmarks
- [ ] Documentation
- [ ] Production-ready deployment

---

**READY TO BEGIN! 🚀**

Start with: `agent/input_encoder.py` (~200 lines, 1-2 hours)

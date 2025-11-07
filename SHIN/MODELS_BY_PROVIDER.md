# 🌍 LiteLLM Gateway - Models by Provider

Quick reference guide organized by provider for easy model selection.

---

## 🔵 Anthropic

**Provider:** Anthropic Official API  
**API Key Required:** `ANTHROPIC_API_KEY`  
**Documentation:** https://docs.anthropic.com/

### Available Models

```
claude-3-5-sonnet       - Latest Claude model, best for general use
claude-3-opus           - Claude 3 Opus, previous generation
```

**Example API Call:**
```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{"model": "claude-3-5-sonnet", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## 🟣 NVIDIA NIM

**Provider:** NVIDIA NIM (Inference Microservices)  
**API Key Required:** `NVIDIA_NIM_API_KEY`  
**API Base:** `NVIDIA_NIM_API_BASE`  
**Documentation:** https://docs.api.nvidia.com/nim/

### Llama Models (Meta)

```
nvidia-llama-3-1-8b         - 8B parameters, fast inference
nvidia-llama-3-1-70b        - 70B parameters, high performance
nvidia-llama-3-1-405b       - 405B parameters, maximum capability
nvidia-llama-3-1-nemotron-70b - NVIDIA optimized 70B model
```

### Mistral Models (Mistral AI)

```
nvidia-mistral-nemo-12b     - 12B parameters, balanced performance
nvidia-mistral-large-2      - Large version, advanced reasoning
```

### Multi-Provider Models

```
moonshotai-kimi-k2          - MoonshotAI Kimi K2 model
qwen-coder-480b             - Alibaba Qwen Coder, 480B parameters
minimax-m2                  - MiniMax M2 model
```

**Example API Call:**
```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{"model": "nvidia-llama-3-1-8b", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## 🟠 OpenCode.ai

**Provider:** OpenCode.ai  
**API Key Required:** `OPENCODE_API_KEY`  
**API Base:** `https://opencode.ai/zen/v1/chat/completions`

### Available Models

```
opencode-big-pickle         - Big Pickle model for coding
```

**Example API Call:**
```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{"model": "opencode-big-pickle", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## 🔷 Z.ai

**Provider:** Z.ai  
**API Key Required:** `ZAI_API_KEY`  
**API Base:** `https://api.z.ai/api/anthropic`

### Available Models

```
glm-4.6                     - GLM 4.6 model
```

**Example API Call:**
```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{"model": "glm-4.6", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## 🟢 iFlow

**Provider:** iFlow API  
**API Key Required:** `IFLOW_API_KEY`  
**API Base:** `https://apis.iflow.cn/v1`

### Available Models

```
iflow-qwen3-coder           - Qwen 3 Coder model
iflow-qwen3-coder-plus      - Qwen 3 Coder Plus (enhanced)
iflow-qwen3-max             - Qwen 3 Max (most capable)
iflow-qwen3-235b-thinking   - Qwen 3 with 235B thinking capability
iflow-kimi-k2-0905          - Kimi K2 model
iflow-glm-4.6               - GLM 4.6 model
iflow-deepseek-v3.2         - DeepSeek v3.2 model
```

**Example API Call:**
```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{"model": "iflow-qwen3-max", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## 🔴 Minimax

**Provider:** Minimax  
**API Key Required:** `MINIMAX1_API_KEY`  
**API Base:** `https://api.minimax.io/anthropic`

### Available Models

```
minimax1-claude             - Claude-compatible endpoint via Minimax
```

**Example API Call:**
```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{"model": "minimax1-claude", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## 📊 Provider Comparison

| Provider | Models | Type | Best For |
|----------|--------|------|----------|
| **Anthropic** | 2 | Proprietary | High quality, general purpose |
| **NVIDIA NIM** | 9 | Various | Speed, performance, variety |
| **iFlow** | 7 | Aggregator | Access to multiple models |
| **OpenCode** | 1 | Specialized | Code generation |
| **Z.ai** | 1 | Specialized | GLM models |
| **Minimax** | 1 | Compatible | Claude compatibility |

---

## 🎯 Use Case Recommendations

### Best for General Chat
```
1. claude-3-5-sonnet        (Highest quality)
2. nvidia-llama-3-1-70b     (Good alternative)
3. iflow-qwen3-max          (Capable and fast)
```

### Best for Code
```
1. opencode-big-pickle      (Code-focused)
2. iflow-qwen3-coder-plus   (Code generation)
3. nvidia-llama-3-1-70b     (Good for code)
```

### Best for Speed
```
1. nvidia-llama-3-1-8b      (Fastest)
2. nvidia-mistral-nemo-12b  (Fast)
3. iflow-deepseek-v3.2      (Very fast)
```

### Best for Advanced Reasoning
```
1. claude-3-5-sonnet        (Best reasoning)
2. nvidia-llama-3-1-405b    (Powerful reasoning)
3. iflow-qwen3-235b-thinking (Thinking capability)
```

### Best for Balanced Performance
```
1. claude-3-5-sonnet        (All-rounder)
2. nvidia-llama-3-1-70b     (Balanced)
3. iflow-qwen3-max          (Good balance)
```

---

## 🔄 Model Selection Flowchart

```
START: Which model to use?
│
├─ Need highest quality?
│  └─ YES → claude-3-5-sonnet ✓
│
├─ Need coding capabilities?
│  └─ YES → opencode-big-pickle or iflow-qwen3-coder ✓
│
├─ Need maximum speed?
│  └─ YES → nvidia-llama-3-1-8b ✓
│
├─ Need advanced reasoning?
│  └─ YES → claude-3-5-sonnet or nvidia-llama-3-1-405b ✓
│
├─ Need variety/alternatives?
│  └─ YES → iFlow models (7 options) ✓
│
└─ Need proven performance?
   └─ YES → NVIDIA NIM models ✓
```

---

## 🚀 Quick Start by Provider

### Using Anthropic Claude

```python
import openai

client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="claude-3-5-sonnet",
    messages=[{"role": "user", "content": "Hello Claude!"}]
)
```

### Using NVIDIA Llama

```python
response = client.chat.completions.create(
    model="nvidia-llama-3-1-70b",
    messages=[{"role": "user", "content": "Hello Llama!"}]
)
```

### Using iFlow Models

```python
response = client.chat.completions.create(
    model="iflow-qwen3-max",
    messages=[{"role": "user", "content": "Hello Qwen!"}]
)
```

---

## 📋 All Model IDs Quick List

```
ANTHROPIC:
  - claude-3-5-sonnet
  - claude-3-opus

NVIDIA NIM:
  - nvidia-llama-3-1-nemotron-70b
  - nvidia-llama-3-1-405b
  - nvidia-llama-3-1-70b
  - nvidia-llama-3-1-8b
  - nvidia-mistral-nemo-12b
  - nvidia-mistral-large-2
  - moonshotai-kimi-k2
  - qwen-coder-480b
  - minimax-m2

OPENCODE:
  - opencode-big-pickle

Z.AI:
  - glm-4.6

IFLOW:
  - iflow-qwen3-coder-plus
  - iflow-qwen3-max
  - iflow-qwen3-coder
  - iflow-kimi-k2-0905
  - iflow-glm-4.6
  - iflow-deepseek-v3.2
  - iflow-qwen3-235b-thinking

MINIMAX:
  - minimax1-claude
```

---

## ✅ Environment Variables Needed

**Minimum Setup:**
```bash
LITELLM_MASTER_KEY=your-key
```

**For Anthropic Models:**
```bash
ANTHROPIC_API_KEY=your-key
```

**For NVIDIA Models:**
```bash
NVIDIA_NIM_API_KEY=your-key
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1
```

**For iFlow Models:**
```bash
IFLOW_API_KEY=your-key
```

**For All Providers:**
```bash
LITELLM_MASTER_KEY=your-key
ANTHROPIC_API_KEY=your-anthropic-key
NVIDIA_NIM_API_KEY=your-nvidia-key
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1
OPENCODE_API_KEY=your-opencode-key
ZAI_API_KEY=your-zai-key
IFLOW_API_KEY=your-iflow-key
MINIMAX1_API_KEY=your-minimax-key
```

---

Last Updated: November 7, 2025


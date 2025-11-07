# 🤖 LiteLLM Gateway - Available Models

Complete list of all model IDs available through your LiteLLM Gateway proxy.

**Gateway Base URL:** `http://localhost:4000`  
**API Endpoint:** `http://localhost:4000/chat/completions`

---

## 📋 Table of Contents

- [Anthropic Models](#anthropic-models)
- [NVIDIA NIM Models](#nvidia-nim-models)
- [OpenCode.ai Models](#opencode-models)
- [Z.ai Models](#zai-models)
- [iFlow Models](#iflow-models)
- [Minimax Models](#minimax-models)
- [Quick Start Examples](#quick-start-examples)
- [Environment Setup](#environment-setup)

---

## 🔵 Anthropic Models

Anthropic's Claude models via official API.

### Model List

| Model ID | Display Name | Version | Parameters |
|----------|-------------|---------|------------|
| `claude-3-5-sonnet` | Claude 3.5 Sonnet | 20241022 | Latest |
| `claude-3-opus` | Claude 3 Opus | 20240229 | Latest |

### Configuration

```yaml
Provider: Anthropic
API Base: Official Anthropic API
Requires: ANTHROPIC_API_KEY
Documentation: https://docs.litellm.ai/docs/providers/anthropic
```

### Example Usage

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
print(response.choices[0].message.content)
```

---

## 🟣 NVIDIA NIM Models

NVIDIA NIM (NVIDIA Inference Microservices) models for high-performance inference.

### Llama Models

| Model ID | Full Name | Parameters | Type |
|----------|-----------|------------|------|
| `nvidia-llama-3-1-nemotron-70b` | NVIDIA Llama 3.1 Nemotron | 70B | Instruct |
| `nvidia-llama-3-1-405b` | Meta Llama 3.1 | 405B | Instruct |
| `nvidia-llama-3-1-70b` | Meta Llama 3.1 | 70B | Instruct |
| `nvidia-llama-3-1-8b` | Meta Llama 3.1 | 8B | Instruct |

### Mistral Models

| Model ID | Full Name | Parameters | Type |
|----------|-----------|------------|------|
| `nvidia-mistral-nemo-12b` | Mistral Nemo | 12B | Instruct |
| `nvidia-mistral-large-2` | Mistral Large 2 | - | Instruct |

### Other Models

| Model ID | Full Name | Parameters |
|----------|-----------|------------|
| `moonshotai-kimi-k2` | MoonshotAI Kimi K2 | - |
| `qwen-coder-480b` | Qwen Coder | 480B |
| `minimax-m2` | MiniMax M2 | - |

### Configuration

```yaml
Provider: NVIDIA NIM
API Base: os.environ/NVIDIA_NIM_API_BASE
Requires: NVIDIA_NIM_API_KEY
Documentation: https://docs.api.nvidia.com/nim/reference/llm-apis
```

### Example Usage

```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{
    "model": "nvidia-llama-3-1-8b",
    "messages": [{"role": "user", "content": "Explain quantum computing"}],
    "max_tokens": 500
  }'
```

---

## 🟠 OpenCode.ai Models

OpenCode.ai provider for coding-focused models.

| Model ID | Display Name | API Base |
|----------|-------------|----------|
| `opencode-big-pickle` | Big Pickle | https://opencode.ai/zen/v1/chat/completions |

### Configuration

```yaml
Provider: OpenCode.ai
Requires: OPENCODE_API_KEY
```

---

## 🔷 Z.ai Models

Z.ai provider for GLM models.

| Model ID | Display Name | API Base |
|----------|-------------|----------|
| `glm-4.6` | GLM 4.6 | https://api.z.ai/api/anthropic |

### Configuration

```yaml
Provider: Z.ai
Requires: ZAI_API_KEY
```

---

## 🟢 iFlow Provider Models

iFlow API provides access to multiple state-of-the-art models.

| Model ID | Model Name | API Base |
|----------|-----------|----------|
| `iflow-qwen3-coder-plus` | Qwen 3 Coder Plus | https://apis.iflow.cn/v1 |
| `iflow-qwen3-max` | Qwen 3 Max | https://apis.iflow.cn/v1 |
| `iflow-qwen3-coder` | Qwen 3 Coder | https://apis.iflow.cn/v1 |
| `iflow-kimi-k2-0905` | Kimi K2 0905 | https://apis.iflow.cn/v1 |
| `iflow-glm-4.6` | GLM 4.6 | https://apis.iflow.cn/v1 |
| `iflow-deepseek-v3.2` | DeepSeek v3.2 | https://apis.iflow.cn/v1 |
| `iflow-qwen3-235b-thinking` | Qwen 3 235B Thinking | https://apis.iflow.cn/v1 |

### Configuration

```yaml
Provider: iFlow
API Base: https://apis.iflow.cn/v1
Requires: IFLOW_API_KEY
```

---

## 🔴 Minimax Models

Minimax provider with Claude-compatible endpoint.

| Model ID | Display Name | API Base |
|----------|-------------|----------|
| `minimax1-claude` | Claude | https://api.minimax.io/anthropic |

### Configuration

```yaml
Provider: Minimax
Requires: MINIMAX1_API_KEY
```

---

## 📊 Model Statistics

| Category | Count |
|----------|-------|
| Anthropic Models | 2 |
| NVIDIA NIM Models | 9 |
| OpenCode Models | 1 |
| Z.ai Models | 1 |
| iFlow Models | 7 |
| Minimax Models | 1 |
| **TOTAL** | **21** |

---

## 🚀 Quick Start Examples

### Python - OpenAI SDK

```python
import openai

# Initialize client
client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

# Example 1: Using Claude
response = client.chat.completions.create(
    model="claude-3-5-sonnet",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"}
    ],
    max_tokens=500
)
print("Claude Response:", response.choices[0].message.content)

# Example 2: Using NVIDIA Llama
response = client.chat.completions.create(
    model="nvidia-llama-3-1-8b",
    messages=[
        {"role": "user", "content": "Explain machine learning in 2 sentences."}
    ]
)
print("Llama Response:", response.choices[0].message.content)
```

### cURL - Direct API Call

```bash
# Using Claude
curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{
    "model": "claude-3-5-sonnet",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7,
    "max_tokens": 500
  }'

# Using NVIDIA Llama
curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{
    "model": "nvidia-llama-3-1-70b",
    "messages": [{"role": "user", "content": "What is AI?"}],
    "temperature": 0.8,
    "max_tokens": 1000
  }'
```

### Node.js - JavaScript

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: "your-litellm-master-key",
  baseURL: "http://localhost:4000",
});

async function chat() {
  const response = await openai.chat.completions.create({
    model: "claude-3-5-sonnet",
    messages: [
      {
        role: "user",
        content: "Explain quantum computing",
      },
    ],
  });

  console.log(response.choices[0].message.content);
}

chat();
```

---

## 🔑 Environment Setup

### Required Environment Variables

Create a `.env` file in your project root:

```bash
# Master authentication key for the gateway
LITELLM_MASTER_KEY=sk-your-secret-key-here

# Anthropic API (for Claude models)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# NVIDIA NIM API (for NVIDIA models)
NVIDIA_NIM_API_KEY=nvapi-your-key-here
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1

# OpenCode API (for Big Pickle model)
OPENCODE_API_KEY=your-opencode-key-here

# Z.ai API (for GLM model)
ZAI_API_KEY=your-zai-key-here

# iFlow API (for iFlow models)
IFLOW_API_KEY=your-iflow-key-here

# Minimax API (for Claude model)
MINIMAX1_API_KEY=your-minimax-key-here
```

### Loading Environment Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()

# Access variables
master_key = os.getenv("LITELLM_MASTER_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
```

---

## 🔍 Checking Available Models

### List All Models

```bash
# Health check
curl http://localhost:4000/health

# Get model information
curl -H "Authorization: Bearer your-litellm-master-key" \
  http://localhost:4000/v1/models
```

### List via Python

```python
import openai

client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

# List all available models
models = client.models.list()
for model in models.data:
    print(f"Model ID: {model.id}")
```

---

## 💡 Tips & Best Practices

1. **Model Selection**
   - Use `claude-3-5-sonnet` for best quality
   - Use `nvidia-llama-3-1-8b` for fast responses
   - Use `nvidia-llama-3-1-70b` for complex reasoning

2. **API Keys**
   - Keep API keys secure in `.env` files
   - Never commit `.env` to version control
   - Rotate keys periodically

3. **Error Handling**
   ```python
   try:
       response = client.chat.completions.create(
           model="claude-3-5-sonnet",
           messages=[{"role": "user", "content": "Hello"}]
       )
   except openai.APIError as e:
       print(f"API Error: {e}")
   ```

4. **Rate Limiting**
   - Check your API provider's rate limits
   - Implement exponential backoff for retries
   - Monitor token usage

---

## 📚 References

- **LiteLLM Documentation:** https://docs.litellm.ai/
- **OpenAI API Reference:** https://platform.openai.com/docs/api-reference
- **Anthropic API:** https://docs.anthropic.com/
- **NVIDIA NIM:** https://docs.api.nvidia.com/nim/

---

## ❓ Support

For issues or questions:
1. Check the gateway logs
2. Verify environment variables are set
3. Test with the validation script: `python validate_setup.py`
4. Review configuration in `config.yaml`

Last Updated: November 7, 2025


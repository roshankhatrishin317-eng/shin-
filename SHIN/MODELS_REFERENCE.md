# 📇 Model Reference Card - Quick Lookup

Compact reference for all 21 available models in your LiteLLM Gateway.

**Gateway Base URL:** `http://localhost:4000`  
**API Endpoint:** `POST http://localhost:4000/chat/completions`

---

## 🎯 Model IDs (Copy-Paste Ready)

### Anthropic (2 models)
```
claude-3-5-sonnet
claude-3-opus
```

### NVIDIA NIM (9 models)
```
nvidia-llama-3-1-nemotron-70b
nvidia-llama-3-1-405b
nvidia-llama-3-1-70b
nvidia-llama-3-1-8b
nvidia-mistral-nemo-12b
nvidia-mistral-large-2
moonshotai-kimi-k2
qwen-coder-480b
minimax-m2
```

### OpenCode (1 model)
```
opencode-big-pickle
```

### Z.ai (1 model)
```
glm-4.6
```

### iFlow (7 models)
```
iflow-qwen3-coder-plus
iflow-qwen3-max
iflow-qwen3-coder
iflow-kimi-k2-0905
iflow-glm-4.6
iflow-deepseek-v3.2
iflow-qwen3-235b-thinking
```

### Minimax (1 model)
```
minimax1-claude
```

**TOTAL: 21 Models**

---

## 🔑 Required API Keys

| Model | Provider | API Key |
|-------|----------|---------|
| claude-* | Anthropic | `ANTHROPIC_API_KEY` |
| nvidia-* | NVIDIA | `NVIDIA_NIM_API_KEY` |
| opencode-* | OpenCode | `OPENCODE_API_KEY` |
| glm-4.6 | Z.ai | `ZAI_API_KEY` |
| iflow-* | iFlow | `IFLOW_API_KEY` |
| minimax1-* | Minimax | `MINIMAX1_API_KEY` |

**ALL requests also need:** `LITELLM_MASTER_KEY` (gateway authentication)

---

## 📝 Quick API Examples

### Python

```python
import openai

client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

# Replace "claude-3-5-sonnet" with any model ID from the list above
response = client.chat.completions.create(
    model="claude-3-5-sonnet",
    messages=[{"role": "user", "content": "Your message here"}],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### cURL

```bash
curl -X POST http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{
    "model": "claude-3-5-sonnet",
    "messages": [{"role": "user", "content": "Your message here"}],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

### JavaScript/Node.js

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: "your-litellm-master-key",
  baseURL: "http://localhost:4000",
});

const response = await openai.chat.completions.create({
  model: "claude-3-5-sonnet",
  messages: [{ role: "user", content: "Your message here" }],
  temperature: 0.7,
  max_tokens: 1000,
});

console.log(response.choices[0].message.content);
```

---

## ⚡ Common Parameters

| Parameter | Type | Example | Notes |
|-----------|------|---------|-------|
| `model` | string | `"claude-3-5-sonnet"` | Required - use any ID from above |
| `messages` | array | `[{"role": "user", "content": "..."}]` | Required |
| `temperature` | float | `0.7` | 0.0-1.0, higher = more creative |
| `max_tokens` | int | `1000` | Maximum response length |
| `top_p` | float | `0.9` | Nucleus sampling (0.0-1.0) |
| `frequency_penalty` | float | `0.0` | Reduce repetition (-2.0 to 2.0) |
| `presence_penalty` | float | `0.0` | Encourage new topics (-2.0 to 2.0) |

---

## 🏆 Best Models for Different Tasks

| Task | Best Model | Reason |
|------|-----------|--------|
| **General Chat** | `claude-3-5-sonnet` | Highest quality |
| **Code Generation** | `iflow-qwen3-coder-plus` | Optimized for coding |
| **Speed** | `nvidia-llama-3-1-8b` | Smallest, fastest |
| **Reasoning** | `claude-3-5-sonnet` | Best logical thinking |
| **Translation** | `nvidia-llama-3-1-70b` | Good multilingual |
| **Summarization** | `claude-3-5-sonnet` | Accurate summaries |
| **Long Context** | `nvidia-llama-3-1-405b` | Handles large inputs |
| **Creative Writing** | `claude-3-5-sonnet` | Natural language quality |

---

## 🔄 Model Size vs Speed

| Size | Model | Speed | Quality |
|------|-------|-------|---------|
| **Small** | `nvidia-llama-3-1-8b` | ⚡⚡⚡ Fast | Good |
| **Medium** | `nvidia-mistral-nemo-12b` | ⚡⚡ Medium | Very Good |
| **Large** | `nvidia-llama-3-1-70b` | ⚡ Slower | Excellent |
| **XL** | `nvidia-llama-3-1-405b` | 🐢 Slowest | Best |
| **Top Tier** | `claude-3-5-sonnet` | ⚡ Fast | Best |

---

## 🧪 Test All Models

```python
import openai

client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

models_to_test = [
    "claude-3-5-sonnet",
    "nvidia-llama-3-1-8b",
    "iflow-qwen3-max"
]

test_prompt = "Say 'I work!' and nothing else."

for model in models_to_test:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": test_prompt}],
            max_tokens=100
        )
        print(f"✓ {model}: {response.choices[0].message.content}")
    except Exception as e:
        print(f"✗ {model}: Error - {str(e)}")
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Model not found` | Check model ID spelling from list above |
| `Invalid API key` | Verify `LITELLM_MASTER_KEY` in .env |
| `Authentication failed` | Check `Authorization` header format |
| `Rate limit exceeded` | Wait and retry, or use smaller model |
| `Connection refused` | Ensure gateway is running on port 4000 |
| `Timeout error` | Reduce `max_tokens` or try faster model |

---

## 📊 Gateway Status Check

```bash
# Health check
curl http://localhost:4000/health

# List all models
curl -H "Authorization: Bearer your-litellm-master-key" \
  http://localhost:4000/v1/models

# View usage
curl -H "Authorization: Bearer your-litellm-master-key" \
  http://localhost:4000/admin/users
```

---

## 🎓 Response Format

All responses follow OpenAI's format:

```json
{
  "id": "chatcmpl-8...",
  "object": "chat.completion",
  "created": 1698765432,
  "model": "claude-3-5-sonnet",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Response text here..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

---

## 📚 Additional Resources

- **Full Models Documentation:** See `MODELS.md`
- **Provider Details:** See `MODELS_BY_PROVIDER.md`
- **Gateway Setup:** See `SETUP_COMPLETE.md`
- **Quick Start:** See `QUICK_REFERENCE.md`
- **LiteLLM Docs:** https://docs.litellm.ai/

---

## 🚀 One-Liner Tests

```bash
# Test Claude
curl -s -X POST http://localhost:4000/chat/completions -H "Authorization: Bearer your-key" -d '{"model":"claude-3-5-sonnet","messages":[{"role":"user","content":"test"}]}' | jq '.choices[0].message.content'

# Test Llama
curl -s -X POST http://localhost:4000/chat/completions -H "Authorization: Bearer your-key" -d '{"model":"nvidia-llama-3-1-8b","messages":[{"role":"user","content":"test"}]}' | jq '.choices[0].message.content'

# Test Qwen
curl -s -X POST http://localhost:4000/chat/completions -H "Authorization: Bearer your-key" -d '{"model":"iflow-qwen3-max","messages":[{"role":"user","content":"test"}]}' | jq '.choices[0].message.content'
```

---

## 📋 .env Template

```bash
# Authentication
LITELLM_MASTER_KEY=sk-your-secret-key-here

# Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key

# NVIDIA NIM
NVIDIA_NIM_API_KEY=nvapi-your-key
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1

# Other Providers
OPENCODE_API_KEY=your-key
ZAI_API_KEY=your-key
IFLOW_API_KEY=your-key
MINIMAX1_API_KEY=your-key
```

---

Last Updated: November 7, 2025  
**Total Models Available:** 21  
**Gateway Ready:** ✅


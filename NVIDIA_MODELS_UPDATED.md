# 🟢 NVIDIA NIM Models - Updated Catalog

Your LiteLLM Gateway now has access to **12 powerful models** through NVIDIA NIM API!

## 🚀 Available Models (12 Total)

### 🦙 Llama Models (4 models)

| Model Name | Size | Description | Best For |
|------------|------|-------------|----------|
| `nvidia-llama-3-1-405b` | 405B | **Largest & Most Powerful** | Complex reasoning, research |
| `nvidia-llama-3-1-nemotron-70b` | 70B | NVIDIA-optimized Llama | High-quality responses |
| `nvidia-llama-3-1-70b` | 70B | Meta's Llama 3.1 | General purpose |
| `nvidia-llama-3-1-8b` | 8B | **Fastest** | Quick responses, high volume |

### 🎯 Mistral Models (2 models)

| Model Name | Size | Description | Best For |
|------------|------|-------------|----------|
| `nvidia-mistral-large-2` | Large | **Latest Mistral** | Advanced reasoning |
| `nvidia-mistral-nemo-12b` | 12B | Efficient Mistral | Balanced performance |

### ⭐ Specialized Models (3 NEW!)

| Model Name | Provider | Description | Best For |
|------------|----------|-------------|----------|
| `moonshotai-kimi-k2` | MoonshotAI | **Kimi K2 Instruct** | Chinese & English, long context |
| `qwen-coder-480b` | Qwen/Alibaba | **Qwen3 Coder 480B** | Code generation, debugging |
| `minimax-m2` | MiniMax | **MiniMax M2** | Multilingual, creative tasks |

## 💻 Quick Usage Examples

### 1. Use the Most Powerful Model (405B)

```python
import openai

client = openai.OpenAI(
    api_key="sk-litellm-gateway-2024",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="nvidia-llama-3-1-405b",  # Largest model!
    messages=[
        {"role": "user", "content": "Explain quantum entanglement in detail"}
    ]
)

print(response.choices[0].message.content)
```

### 2. Use Qwen Coder for Programming

```python
response = client.chat.completions.create(
    model="qwen-coder-480b",  # Specialized for code!
    messages=[
        {"role": "user", "content": "Write a Python function to implement binary search"}
    ]
)

print(response.choices[0].message.content)
```

### 3. Use MoonshotAI Kimi K2

```python
response = client.chat.completions.create(
    model="moonshotai-kimi-k2",  # Great for Chinese/English
    messages=[
        {"role": "user", "content": "Tell me about AI in both English and Chinese"}
    ]
)

print(response.choices[0].message.content)
```

### 4. Use MiniMax M2

```python
response = client.chat.completions.create(
    model="minimax-m2",
    messages=[
        {"role": "user", "content": "Write a creative story about space exploration"}
    ]
)

print(response.choices[0].message.content)
```

### 5. Fast Responses with 8B Model

```python
response = client.chat.completions.create(
    model="nvidia-llama-3-1-8b",  # Fastest!
    messages=[
        {"role": "user", "content": "What's 2+2?"}
    ],
    temperature=0
)

print(response.choices[0].message.content)
```

## 📊 Model Comparison

### By Size/Power

```
🏆 Most Powerful:
├── nvidia-llama-3-1-405b (405B) ⭐⭐⭐⭐⭐
├── qwen-coder-480b (480B, specialized)
├── nvidia-llama-3-1-nemotron-70b (70B)
├── nvidia-llama-3-1-70b (70B)
├── nvidia-mistral-large-2
├── nvidia-mistral-nemo-12b (12B)
└── nvidia-llama-3-1-8b (8B) ⚡ Fastest
```

### By Use Case

**🎓 Research & Complex Reasoning:**
- `nvidia-llama-3-1-405b` - Best choice
- `nvidia-llama-3-1-nemotron-70b` - Great alternative

**💻 Code Generation:**
- `qwen-coder-480b` - Specialized for coding
- `nvidia-llama-3-1-405b` - Also excellent

**🌏 Multilingual (Chinese/English):**
- `moonshotai-kimi-k2` - Optimized for Chinese
- `minimax-m2` - Good multilingual support

**⚡ Fast Responses:**
- `nvidia-llama-3-1-8b` - Fastest
- `nvidia-mistral-nemo-12b` - Good balance

**🎨 Creative Writing:**
- `minimax-m2` - Creative tasks
- `nvidia-mistral-large-2` - Also good

## 🔧 cURL Examples

### Test Llama 405B

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-litellm-gateway-2024" \
  -d '{
    "model": "nvidia-llama-3-1-405b",
    "messages": [
      {"role": "user", "content": "Hello from the biggest model!"}
    ]
  }'
```

### Test Qwen Coder

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-litellm-gateway-2024" \
  -d '{
    "model": "qwen-coder-480b",
    "messages": [
      {"role": "user", "content": "Write a quicksort in Python"}
    ]
  }'
```

### Test Kimi K2

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-litellm-gateway-2024" \
  -d '{
    "model": "moonshotai-kimi-k2",
    "messages": [
      {"role": "user", "content": "你好！Tell me about AI."}
    ]
  }'
```

## 🚀 Getting Started

### 1. Start Gateway

```bash
python start_gateway.py
```

### 2. Test All Models

```bash
python test_nvidia.py
```

This will test all 12 models!

### 3. List Available Models

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-litellm-gateway-2024"
```

## 💡 Pro Tips

### 1. **Choose the Right Model for the Task**
- Don't always use the biggest model
- `nvidia-llama-3-1-8b` is great for simple tasks
- `qwen-coder-480b` for all coding tasks
- `nvidia-llama-3-1-405b` for complex reasoning

### 2. **Optimize for Speed**
- Use smaller models during development
- Switch to larger models in production only when needed
- `nvidia-llama-3-1-8b` is 50x faster than 405B

### 3. **Cost Optimization**
- Smaller models = lower costs
- Use 8B for 80% of tasks
- Reserve 405B for complex problems

### 4. **Streaming for Better UX**
```python
stream = client.chat.completions.create(
    model="nvidia-llama-3-1-405b",
    messages=[{"role": "user", "content": "Long response"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### 5. **Temperature Settings**
- `temperature=0` - Deterministic (same answer every time)
- `temperature=0.7` - Balanced (default)
- `temperature=1.5` - Creative (varied responses)

## 📋 Full Model List

Here's the complete configuration in your `config.yaml`:

```yaml
# Llama Models
- nvidia-llama-3-1-405b (meta/llama-3.1-405b-instruct)
- nvidia-llama-3-1-nemotron-70b (nvidia/llama-3.1-nemotron-70b-instruct)
- nvidia-llama-3-1-70b (meta/llama-3.1-70b-instruct)
- nvidia-llama-3-1-8b (meta/llama-3.1-8b-instruct)

# Mistral Models
- nvidia-mistral-large-2 (mistralai/mistral-large-2-instruct)
- nvidia-mistral-nemo-12b (mistralai/mistral-nemo-12b-instruct)

# Specialized Models
- moonshotai-kimi-k2 (moonshotai/kimi-k2-instruct-0905)
- qwen-coder-480b (qwen/qwen3-coder-480b-a35b-instruct)
- minimax-m2 (minimaxai/minimax-m2)
```

## 🔐 Authentication

All models use the same NVIDIA API key from your `.env`:

```bash
NVIDIA_NIM_API_KEY=nvapi-W2jN...T5da
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1
```

## 📚 Resources

- **NVIDIA NIM Catalog:** [https://build.nvidia.com](https://build.nvidia.com)
- **API Documentation:** [https://docs.api.nvidia.com/nim/reference/llm-apis](https://docs.api.nvidia.com/nim/reference/llm-apis)
- **LiteLLM Docs:** [https://docs.litellm.ai/docs/providers/nvidia_nim](https://docs.litellm.ai/docs/providers/nvidia_nim)

## ✅ Summary

You now have access to **12 powerful models**:
- ✅ 4 Llama models (8B to 405B)
- ✅ 2 Mistral models
- ✅ 3 specialized models (Kimi K2, Qwen Coder, MiniMax)
- ✅ Plus 3 OpenAI models (if you add key)
- ✅ Plus 2 Anthropic models (if you add key)

**Total: Up to 17 models in one gateway!** 🎉

Test them all:
```bash
python test_nvidia.py
```


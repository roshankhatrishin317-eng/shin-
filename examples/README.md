# LiteLLM Gateway - Examples

This directory contains practical examples for using the LiteLLM Gateway based on the official documentation at [https://docs.litellm.ai/docs/](https://docs.litellm.ai/docs/).

## Prerequisites

1. **Gateway is running:**
   ```bash
   cd ..
   python start_gateway.py
   ```

2. **Environment variables are set:**
   - `LITELLM_MASTER_KEY` - Your gateway authentication key
   - `OPENAI_API_KEY` - Your OpenAI API key (for OpenAI models)
   - `ANTHROPIC_API_KEY` - Your Anthropic API key (for Claude models)

## Examples

### 1. Python Examples (`basic_usage.py`)

Comprehensive Python examples using the OpenAI SDK:

```bash
python examples/basic_usage.py
```

**Includes:**
- ✅ Basic chat completion
- ✅ Streaming responses
- ✅ Using different models (GPT, Claude)
- ✅ Conversation history
- ✅ Custom parameters (temperature, max_tokens)

### 2. cURL Examples (`curl_examples.sh`)

HTTP API examples using cURL:

```bash
chmod +x examples/curl_examples.sh
./examples/curl_examples.sh
```

**Includes:**
- ✅ Basic requests
- ✅ System messages
- ✅ Streaming
- ✅ Multiple models
- ✅ Health checks
- ✅ Model listing

## Quick Python Example

```python
import openai

# Point to your LiteLLM Gateway
client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

# Use any model configured in config.yaml
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # or gpt-4, claude-3-5-sonnet, etc.
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## Quick cURL Example

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Testing Different Models

The gateway supports multiple providers. Examples:

```python
# OpenAI GPT-4
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# OpenAI GPT-4o (latest)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

# Anthropic Claude
response = client.chat.completions.create(
    model="claude-3-5-sonnet",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Common Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `model` | Model name from config.yaml | `"gpt-3.5-turbo"` |
| `messages` | Array of message objects | `[{"role": "user", "content": "Hi"}]` |
| `temperature` | Randomness (0-2) | `0.7` |
| `max_tokens` | Max response length | `100` |
| `stream` | Enable streaming | `true` |
| `n` | Number of completions | `1` |

## Error Handling

The gateway returns OpenAI-compatible errors:

```python
from openai import OpenAIError

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except OpenAIError as e:
    print(f"Error: {e}")
```

## Monitoring & Debugging

1. **Check gateway logs** - View console output where gateway is running
2. **Health endpoint** - `curl http://localhost:4000/health`
3. **Model list** - `curl http://localhost:4000/v1/models`
4. **Database logs** - Check `litellm.db` for usage history

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/docs/)
- [LiteLLM Proxy Guide](https://docs.litellm.ai/docs/proxy/quick_start)
- [Supported Providers](https://docs.litellm.ai/docs/providers)
- [GitHub Repository](https://github.com/BerriAI/litellm)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Make sure gateway is running on port 4000 |
| Authentication error | Check `LITELLM_MASTER_KEY` matches |
| Model not found | Verify model is in `config.yaml` |
| Provider error | Check provider API key is set and valid |

## Next Steps

1. Try the examples in this directory
2. Modify them for your use case
3. Add more models to `../config.yaml`
4. Explore advanced features like caching, rate limiting, and load balancing


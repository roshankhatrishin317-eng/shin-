# ✅ OpenAI-Compatible API - LiteLLM Gateway

## Yes! Your LiteLLM Gateway is 100% OpenAI-Compatible!

**What does this mean?**
- ✅ Use the OpenAI SDK to access ANY LLM provider
- ✅ Same endpoints as OpenAI (`/v1/chat/completions`, etc.)
- ✅ Same request/response format
- ✅ Works with ANY tool that supports OpenAI API

## 🔄 How It Works

```
┌─────────────────┐
│  Your App with  │
│   OpenAI SDK    │
└────────┬────────┘
         │ OpenAI Format
         ↓
┌─────────────────┐
│ LiteLLM Gateway │ ← You just change base_url here!
│  (Port 4000)    │
└────────┬────────┘
         │ Translates to each provider
         ↓
┌─────────────────────────────────┐
│  OpenAI  │ Anthropic │ Azure... │
└─────────────────────────────────┘
```

## 💻 Quick Start Examples

### 1. Python - OpenAI SDK (Recommended)

```python
import openai

# Instead of this (direct to OpenAI):
# client = openai.OpenAI(
#     api_key="sk-openai-key",
#     base_url="https://api.openai.com/v1"
# )

# Do this (through your gateway):
client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

# Now use ANY model with the same code!
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Works!
    # model="claude-3-5-sonnet",  # Also works!
    # model="gpt-4",  # Also works!
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

### 2. cURL - HTTP API

```bash
# Same format as OpenAI's API
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### 3. Node.js / JavaScript

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'your-litellm-master-key',
  baseURL: 'http://localhost:4000'
});

async function main() {
  const response = await client.chat.completions.create({
    model: 'gpt-3.5-turbo',
    messages: [{ role: 'user', content: 'Hello!' }]
  });
  
  console.log(response.choices[0].message.content);
}

main();
```

### 4. LangChain

```python
from langchain.chat_models import ChatOpenAI

# Point LangChain to your gateway
llm = ChatOpenAI(
    openai_api_base="http://localhost:4000",
    openai_api_key="your-litellm-master-key",
    model_name="gpt-3.5-turbo"
    # or model_name="claude-3-5-sonnet"
)

response = llm.invoke("Tell me a joke!")
print(response.content)
```

### 5. LlamaIndex

```python
from llama_index.llms import OpenAI

llm = OpenAI(
    api_key="your-litellm-master-key",
    api_base="http://localhost:4000",
    model="gpt-3.5-turbo"
)

response = llm.complete("Hello!")
print(response)
```

## 🎯 Available OpenAI-Compatible Endpoints

Your gateway provides these standard OpenAI endpoints:

| Endpoint | Description | Example |
|----------|-------------|---------|
| `/v1/chat/completions` | Chat completions | Main endpoint for conversations |
| `/v1/completions` | Text completions | Legacy text completion |
| `/v1/embeddings` | Generate embeddings | Vector embeddings |
| `/v1/models` | List models | See available models |
| `/health` | Health check | Gateway status |
| `/` or `/docs` | Swagger API docs | Interactive API docs |

## 🔄 Using Multiple Providers

The beauty of OpenAI-compatible API is you can switch providers **without changing your code**:

```python
import openai

client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

# Use OpenAI
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)

# Use Anthropic (same code!)
response = client.chat.completions.create(
    model="claude-3-5-sonnet",
    messages=[{"role": "user", "content": "Hello"}]
)

# Use GPT-4 (same code!)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## 📋 Supported Features

All standard OpenAI features are supported:

### ✅ Chat Completions
- Messages with roles (system, user, assistant)
- Streaming responses
- Temperature, max_tokens, etc.
- Function calling (if provider supports)
- JSON mode (if provider supports)

### ✅ Completions
- Text completion
- Streaming
- Multiple completions (n parameter)

### ✅ Embeddings
- Text to vector embeddings
- Batch processing

### ✅ Models
- List available models
- Model information

## 🔧 Configuration for Different Tools

### Postman / Insomnia

**Base URL:** `http://localhost:4000`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer your-litellm-master-key
```

**Body:**
```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}
```

### Environment Variables

Set these in any tool that uses OpenAI:

```bash
OPENAI_API_BASE=http://localhost:4000
OPENAI_API_KEY=your-litellm-master-key
```

### Docker / Docker Compose

```yaml
environment:
  - OPENAI_API_BASE=http://litellm-gateway:4000
  - OPENAI_API_KEY=your-litellm-master-key
```

## 🚀 Try It Now!

### 1. Start your gateway:
```bash
python start_gateway.py
```

### 2. Run the OpenAI compatibility demo:
```bash
python examples/openai_compatible_demo.py
```

### 3. Or test with cURL:
```bash
./examples/curl_examples.sh
```

## 🎯 Real-World Use Cases

### 1. **Easy Provider Migration**
Switch from OpenAI to Anthropic without code changes:
- Just change `model` parameter
- Same request/response format
- No code refactoring needed

### 2. **Multi-Provider Applications**
Use different providers for different tasks:
- OpenAI for general queries
- Anthropic for analysis
- Local models for privacy-sensitive data

### 3. **Cost Optimization**
Route requests based on cost:
- Cheap models for simple tasks
- Expensive models for complex tasks
- Automatic failover between providers

### 4. **Development & Testing**
- Dev: Use cheap models or local Ollama
- Staging: Use mid-tier models
- Production: Use premium models
- All with the same code!

### 5. **Legacy Application Support**
Point existing OpenAI-based apps to your gateway:
- Add new providers without code changes
- Centralized authentication
- Usage monitoring and logging

## 📊 Response Format (OpenAI-Compatible)

Your gateway returns the exact same format as OpenAI:

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "gpt-3.5-turbo",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

## 🔐 Authentication

Just like OpenAI, use the `Authorization` header:

```bash
Authorization: Bearer your-litellm-master-key
```

Or with the SDK:
```python
client = openai.OpenAI(api_key="your-litellm-master-key", ...)
```

## ❓ FAQ

### Q: Do I need to change my existing OpenAI code?
**A:** Only 2 things:
1. Change `base_url` to your gateway
2. Change `api_key` to your gateway key

### Q: What if a provider doesn't support a feature?
**A:** LiteLLM will do its best to translate or skip unsupported params.

### Q: Can I use streaming?
**A:** Yes! Set `stream=True` just like OpenAI.

### Q: Does it work with all OpenAI SDK versions?
**A:** Yes, it's compatible with OpenAI SDK v1.0.0+

### Q: Can I use it in production?
**A:** Yes! Add proper authentication, rate limiting, and monitoring.

## 📚 More Resources

- **Try the demo:** `python examples/openai_compatible_demo.py`
- **Official docs:** [https://docs.litellm.ai/docs/](https://docs.litellm.ai/docs/)
- **Basic examples:** `python examples/basic_usage.py`
- **cURL examples:** `./examples/curl_examples.sh`

## ✅ Summary

Your LiteLLM Gateway is **100% OpenAI-compatible**, which means:

✅ **Same API format as OpenAI**
✅ **Works with OpenAI SDK**
✅ **Works with any OpenAI-compatible tool**
✅ **But can route to 100+ providers**
✅ **Switch providers without code changes**

**Just change 2 things and you're done:**
1. `base_url`: `http://localhost:4000`
2. `api_key`: Your gateway master key

That's it! 🎉


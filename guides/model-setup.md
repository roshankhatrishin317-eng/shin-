# 🤖 Model Setup Guide

Learn how to add, configure, and manage AI models in your Shin LiteLLM Gateway.

## 📋 Table of Contents

1. [Understanding Model Configuration](#understanding-model-configuration)
2. [Adding New Models](#adding-new-models)
3. [Provider-Specific Setup](#provider-specific-setup)
4. [Model Testing](#model-testing)
5. [Load Balancing](#load-balancing)
6. [Fallback Strategies](#fallback-strategies)
7. [Common Issues](#common-issues)

---

## Understanding Model Configuration

### Model Definition Structure

Every model in `config.yaml` follows this structure:

```yaml
model_list:
  - model_name: YOUR_MODEL_NAME        # Name used in API calls
    litellm_params:
      model: PROVIDER/MODEL_ID         # Provider and model identifier
      api_key: os.environ/API_KEY_VAR  # API key from environment
      api_base: BASE_URL               # API endpoint (optional)
```

### Key Components

1. **model_name**: The name you'll use in API requests
2. **model**: Provider-specific model identifier
3. **api_key**: Reference to environment variable containing the key
4. **api_base**: API endpoint URL (required for some providers)

---

## Adding New Models

### Step 1: Get Provider Credentials

First, obtain API credentials from the provider:

- **NVIDIA NIM**: https://build.nvidia.com/
- **OpenAI**: https://platform.openai.com/
- **Anthropic**: https://console.anthropic.com/
- **Other providers**: See [LiteLLM Providers](https://docs.litellm.ai/docs/providers)

### Step 2: Add to Environment

Edit `.env` and add your key:

```bash
# Example for new provider
MY_PROVIDER_API_KEY=your-api-key-here
MY_PROVIDER_BASE_URL=https://api.provider.com/v1
```

### Step 3: Add to config.yaml

Add model definition to `config.yaml`:

```yaml
model_list:
  - model_name: my-new-model
    litellm_params:
      model: provider/model-name
      api_key: os.environ/MY_PROVIDER_API_KEY
      api_base: os.environ/MY_PROVIDER_BASE_URL  # if needed
```

### Step 4: Restart Gateway

```bash
# Stop current gateway (Ctrl+C)
# Start again
python start_gateway.py
```

### Step 5: Test New Model

```python
import openai

client = openai.OpenAI(
    api_key="your-master-key",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="my-new-model",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

---

## Provider-Specific Setup

### NVIDIA NIM Models

#### Configuration

```yaml
- model_name: shin-llama-405b
  litellm_params:
    model: nvidia_nim/meta/llama-3.1-405b-instruct
    api_key: os.environ/NVIDIA_NIM_API_KEY
    api_base: os.environ/NVIDIA_NIM_API_BASE
```

#### Environment

```bash
NVIDIA_NIM_API_KEY=nvapi-xxxxx
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1
```

#### Available Models

- `nvidia/llama-3.1-nemotron-70b-instruct`
- `meta/llama-3.1-405b-instruct`
- `meta/llama-3.1-70b-instruct`
- `meta/llama-3.1-8b-instruct`
- `mistralai/mistral-nemo-12b-instruct`
- `mistralai/mistral-large-2-instruct`
- `moonshotai/kimi-k2-instruct-0905`
- `qwen/qwen3-coder-480b-a35b-instruct`
- `minimaxai/minimax-m2`

### OpenAI Models

#### Configuration

```yaml
- model_name: gpt-4
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_API_KEY
```

#### Environment

```bash
OPENAI_API_KEY=sk-xxxxx
```

#### Available Models

- `gpt-4`
- `gpt-4-turbo`
- `gpt-3.5-turbo`
- `gpt-4o`

### Anthropic (Claude) Models

#### Configuration

```yaml
- model_name: claude-3-opus
  litellm_params:
    model: claude-3-opus-20240229
    api_key: os.environ/ANTHROPIC_API_KEY
```

#### Environment

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

#### Available Models

- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`

### Azure OpenAI

#### Configuration

```yaml
- model_name: azure-gpt-4
  litellm_params:
    model: azure/your-deployment-name
    api_base: os.environ/AZURE_API_BASE
    api_key: os.environ/AZURE_API_KEY
    api_version: "2023-07-01-preview"
```

#### Environment

```bash
AZURE_API_KEY=xxxxx
AZURE_API_BASE=https://your-resource.openai.azure.com/
```

### Ollama (Local Models)

#### Configuration

```yaml
- model_name: local-llama
  litellm_params:
    model: ollama/llama2
    api_base: http://localhost:11434
```

#### Setup

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama2

# No API key needed for local models
```

### Custom OpenAI-Compatible Endpoints

#### Configuration

```yaml
- model_name: custom-model
  litellm_params:
    model: openai/model-name
    api_key: os.environ/CUSTOM_API_KEY
    api_base: https://api.custom.com/v1
```

This works for any provider with OpenAI-compatible API.

---

## Model Testing

### Test Single Model

```python
import openai

client = openai.OpenAI(
    api_key="your-master-key",
    base_url="http://localhost:4000"
)

# Test the model
try:
    response = client.chat.completions.create(
        model="model-to-test",
        messages=[{"role": "user", "content": "Say 'test successful'"}],
        max_tokens=50
    )
    print(f"✅ Success: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")
```

### Test All Models

```bash
python test_gateway.py
```

This script tests all configured models automatically.

### Verify Model List

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer your-master-key"
```

---

## Load Balancing

### Why Load Balance?

- **Distribute traffic** across multiple API keys
- **Increase rate limits** by using multiple accounts
- **Improve reliability** with redundancy
- **Reduce latency** with geographic distribution

### Simple Load Balancing

Add multiple instances of the same model:

```yaml
model_list:
  # Instance 1
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_KEY_1
  
  # Instance 2
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_KEY_2
  
  # Instance 3
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_KEY_3
```

### Environment

```bash
OPENAI_KEY_1=sk-xxxxx1
OPENAI_KEY_2=sk-xxxxx2
OPENAI_KEY_3=sk-xxxxx3
```

### Configure Strategy

```yaml
router_settings:
  routing_strategy: simple-shuffle  # Random distribution
  enable_loadbalancing: true
```

### Routing Strategies

#### 1. Simple Shuffle (Random)

```yaml
router_settings:
  routing_strategy: simple-shuffle
```

Randomly selects from available instances.

#### 2. Least Busy

```yaml
router_settings:
  routing_strategy: least-busy
```

Routes to the instance with fewest active requests.

#### 3. Latency-Based

```yaml
router_settings:
  routing_strategy: latency-based-routing
```

Routes to the fastest responding instance.

#### 4. Usage-Based

```yaml
router_settings:
  routing_strategy: usage-based-routing
```

Respects rate limits and quotas.

---

## Fallback Strategies

### What are Fallbacks?

Automatic switching to alternative models when primary fails.

### Basic Fallback

```yaml
router_settings:
  fallback_models:
    gpt-4: ["gpt-3.5-turbo"]
    claude-3-opus: ["claude-3-sonnet", "gpt-4"]
```

### How It Works

1. Request sent to primary model (e.g., `gpt-4`)
2. If fails, automatically tries first fallback (`gpt-3.5-turbo`)
3. If that fails, returns error

### Multi-Level Fallback

```yaml
router_settings:
  fallback_models:
    expensive-model: ["medium-model", "cheap-model", "free-model"]
```

### Retry Configuration

```yaml
router_settings:
  num_retries: 3
  retry_after: 2  # seconds
  timeout: 600
```

---

## Advanced Model Configuration

### Custom Default Parameters

```yaml
- model_name: configured-gpt
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_API_KEY
    # Defaults for this model
    temperature: 0.7
    max_tokens: 2000
    top_p: 0.95
```

### Region-Specific Models

```yaml
# US East
- model_name: gpt-4-us-east
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_KEY_US_EAST
    api_base: https://us-east.openai.com/v1

# EU West
- model_name: gpt-4-eu-west
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_KEY_EU_WEST
    api_base: https://eu-west.openai.com/v1
```

### Model Aliases

Create friendly names:

```yaml
- model_name: fast
  litellm_params:
    model: gpt-3.5-turbo
    api_key: os.environ/OPENAI_API_KEY

- model_name: smart
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_API_KEY

- model_name: cheap
  litellm_params:
    model: gpt-3.5-turbo
    api_key: os.environ/OPENAI_API_KEY
```

---

## Common Issues

### Issue 1: Model Not Found

**Error**: `Model not found: model-name`

**Causes**:
- Model not defined in `config.yaml`
- Typo in model name
- Gateway not restarted after config change

**Solution**:
```bash
# Check config
grep "model_name: model-name" config.yaml

# Restart gateway
python start_gateway.py

# List available models
curl http://localhost:4000/v1/models -H "Authorization: Bearer key"
```

### Issue 2: Authentication Failed

**Error**: `Authentication failed for provider`

**Causes**:
- Invalid API key
- API key not set in environment
- Wrong environment variable name

**Solution**:
```bash
# Check environment variable exists
echo $PROVIDER_API_KEY

# Verify key in .env
cat .env | grep PROVIDER_API_KEY

# Test key directly with provider
curl https://api.provider.com/test -H "Authorization: Bearer $PROVIDER_API_KEY"
```

### Issue 3: Timeout Errors

**Error**: `Request timeout after 600 seconds`

**Causes**:
- Model too slow
- Network issues
- Timeout too short

**Solution**:
```yaml
# Increase timeout for specific model
- model_name: slow-model
  litellm_params:
    model: provider/model
    api_key: os.environ/API_KEY
    timeout: 1200  # 20 minutes

# Or globally
litellm_settings:
  request_timeout: 900
```

### Issue 4: Rate Limit Exceeded

**Error**: `Rate limit exceeded`

**Causes**:
- Too many requests
- Single API key overloaded
- Provider limits reached

**Solution**:
```yaml
# Add more keys for load balancing
- model_name: model
  litellm_params:
    model: provider/model
    api_key: os.environ/KEY_1

- model_name: model
  litellm_params:
    model: provider/model
    api_key: os.environ/KEY_2

# Configure rate limiting
litellm_settings:
  rpm: 100  # requests per minute
```

---

## Model Management Best Practices

### 1. Organization

```yaml
model_list:
  # ============================================
  # NVIDIA NIM Models
  # ============================================
  - model_name: shin-llama-405b
    # ... config
  
  # ============================================
  # OpenAI Models
  # ============================================
  - model_name: gpt-4
    # ... config
```

### 2. Naming Conventions

Use clear, consistent names:

```yaml
# Good
- model_name: shin-llama-70b
- model_name: openai-gpt-4
- model_name: anthropic-claude-opus

# Avoid
- model_name: model1
- model_name: m2
- model_name: test
```

### 3. Documentation

Add comments:

```yaml
model_list:
  # Llama 3.1 405B - Best for complex reasoning
  # Context: 128K tokens
  # Cost: $0.002/1K tokens
  - model_name: shin-llama-405b
    litellm_params:
      model: nvidia_nim/meta/llama-3.1-405b-instruct
      api_key: os.environ/NVIDIA_NIM_API_KEY
      api_base: os.environ/NVIDIA_NIM_API_BASE
```

### 4. Testing

Always test new models:

```bash
# Add model to config
# Restart gateway
python start_gateway.py

# Test immediately
python -c "
import openai
client = openai.OpenAI(api_key='key', base_url='http://localhost:4000')
response = client.chat.completions.create(
    model='new-model',
    messages=[{'role': 'user', 'content': 'test'}]
)
print(response.choices[0].message.content)
"
```

---

## Next Steps

- **Secure Your Models**: [Security Guide](security-guide.md)
- **Monitor Usage**: [Monitoring Guide](monitoring-guide.md)
- **API Integration**: [API Integration Guide](api-integration.md)

---

[⬅ Back to Guides](README.md) | [Next: Security Guide ➡](security-guide.md)


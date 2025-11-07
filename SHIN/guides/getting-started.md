# 🚀 Getting Started with Shin LiteLLM Gateway

This guide will walk you through setting up and using the Shin LiteLLM Gateway from scratch.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Starting the Gateway](#starting-the-gateway)
5. [First API Call](#first-api-call)
6. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have:

### System Requirements
- **Python 3.8 or higher**
- **pip** package manager
- **Git** for cloning the repository
- **4GB RAM minimum** (8GB recommended)
- **Linux, macOS, or Windows** (with WSL recommended)

### Required API Keys
At minimum, you need ONE of the following:
- NVIDIA NIM API Key (recommended for beginners)
- OpenCode.ai API Key
- iFlow API Key
- Any other supported provider key

### How to Get API Keys

#### NVIDIA NIM API Key (Free)
1. Visit https://build.nvidia.com/
2. Sign up for a free account
3. Navigate to any model page
4. Click "Get API Key"
5. Copy your API key (starts with `nvapi-`)

#### Other Providers
- **OpenCode.ai**: https://opencode.ai/
- **iFlow**: https://apis.iflow.cn/
- **Z.ai**: https://z.ai/

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/roshankhatrishin317-eng/shin-.git
cd shin-
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `litellm[proxy]` - The LiteLLM proxy server
- `python-dotenv` - Environment variable management
- `pyyaml` - YAML configuration parser

### Step 3: Verify Installation

```bash
python validate_setup.py
```

You should see:
```
✅ All required files are present
✅ LiteLLM is installed (version X.X.X)
✅ Configuration file is valid
```

---

## Configuration

### Step 1: Create Environment File

```bash
# Copy the template
cp env.template .env
```

### Step 2: Edit Your Environment Variables

Open `.env` in your favorite editor:

```bash
nano .env
# or
vim .env
# or
code .env
```

### Step 3: Add Your API Keys

**Minimum Configuration:**

```bash
# Gateway Master Key (create your own secure key)
LITELLM_MASTER_KEY=sk-1234567890abcdef

# NVIDIA NIM Configuration
NVIDIA_NIM_API_KEY=nvapi-YOUR_KEY_HERE
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1

# Server Configuration (optional)
LITELLM_PORT=4000
LITELLM_HOST=0.0.0.0
```

**Full Configuration (all providers):**

```bash
# Gateway Configuration
LITELLM_MASTER_KEY=sk-1234567890abcdef
LITELLM_PORT=4000
LITELLM_HOST=0.0.0.0

# NVIDIA NIM
NVIDIA_NIM_API_KEY=nvapi-xxxxx
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1

# OpenCode.ai
OPENCODE_API_KEY=your-opencode-key

# Z.ai
ZAI_API_KEY=your-zai-key

# iFlow
IFLOW_API_KEY=your-iflow-key

# Minimax
MINIMAX1_API_KEY=your-minimax-key

# KAT
KAT_API_KEY=your-kat-key
```

### Important Notes About Keys

1. **LITELLM_MASTER_KEY**: This is YOUR gateway password. Make it strong!
   - Use at least 20 characters
   - Include letters, numbers, and special characters
   - Example: `sk-$(openssl rand -hex 16)`

2. **Provider Keys**: Only add keys for providers you want to use
   - Gateway will skip models with missing keys
   - You can add more keys later

---

## Starting the Gateway

### Method 1: Using the Start Script (Recommended)

```bash
python start_gateway.py
```

This script:
- Loads your environment variables
- Validates configuration
- Starts the gateway with proper settings
- Shows you the access URL

### Method 2: Using LiteLLM CLI Directly

```bash
litellm --config config.yaml --host 0.0.0.0 --port 4000
```

### Method 3: Using Quick Start Script

```bash
./quick-start.sh
```

### Expected Output

```
LiteLLM Proxy Server Starting...
📡 Server running at http://localhost:4000
🔑 Master Key: sk-*****************
📊 Admin UI: http://localhost:4000/ui
📝 API Docs: http://localhost:4000/

Available Models:
  - shin-llama-3-1-70b
  - shin-mistral-large-2
  - otsu-qwen3-max
  ... (more models)

Press Ctrl+C to stop
```

---

## First API Call

### Option 1: Using Test Script

In a **new terminal** (keep the gateway running):

```bash
python test_gateway.py
```

This will test all configured models and show results.

### Option 2: Using Python

Create a file `test.py`:

```python
import openai

# Configure client
client = openai.OpenAI(
    api_key="sk-1234567890abcdef",  # Your LITELLM_MASTER_KEY
    base_url="http://localhost:4000"
)

# Make a request
response = client.chat.completions.create(
    model="shin-llama-3-1-70b",
    messages=[
        {"role": "user", "content": "Hello! Can you hear me?"}
    ]
)

print(response.choices[0].message.content)
```

Run it:
```bash
python test.py
```

### Option 3: Using cURL

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234567890abcdef" \
  -d '{
    "model": "shin-llama-3-1-70b",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### Expected Response

```json
{
  "id": "chatcmpl-xxxxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "shin-llama-3-1-70b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! Yes, I can hear you. How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  }
}
```

---

## Exploring Available Models

### List All Models

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-1234567890abcdef"
```

### Try Different Models

```python
# Llama 3.1 70B
response = client.chat.completions.create(
    model="shin-llama-3-1-70b",
    messages=[{"role": "user", "content": "Write a haiku"}]
)

# Mistral Large 2
response = client.chat.completions.create(
    model="shin-mistral-large-2",
    messages=[{"role": "user", "content": "Explain AI"}]
)

# Qwen Coder
response = client.chat.completions.create(
    model="otsu-qwen3-coder",
    messages=[{"role": "user", "content": "Write a Python function"}]
)
```

---

## Understanding the Web UI

### Access the Dashboard

Open in your browser:
```
http://localhost:4000/ui
```

### Features

1. **Model Management** - View and test all models
2. **Usage Analytics** - See request counts and costs
3. **API Keys** - Create virtual keys for different users
4. **Logs** - View request history
5. **Settings** - Configure gateway behavior

### API Documentation

Browse interactive API docs:
```
http://localhost:4000/
```

This shows Swagger/OpenAPI documentation with all endpoints.

---

## Common First-Time Issues

### Issue 1: Port Already in Use

**Error:** `Address already in use: 4000`

**Solution:**
```bash
# Find what's using the port
lsof -i :4000

# Kill the process
kill -9 <PID>

# Or use a different port
export LITELLM_PORT=4001
python start_gateway.py
```

### Issue 2: Authentication Failed

**Error:** `Authentication error: Invalid API key`

**Solution:**
- Ensure `LITELLM_MASTER_KEY` in `.env` matches your client code
- Check for typos or extra spaces
- Verify the key starts with `Bearer` in Authorization header

### Issue 3: Model Not Found

**Error:** `Model shin-llama-3-1-70b not found`

**Solution:**
- Check `config.yaml` has the model defined
- Verify API key for that provider is set in `.env`
- Restart the gateway after config changes

### Issue 4: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'litellm'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep litellm
```

---

## Next Steps

Congratulations! You now have a working LiteLLM Gateway. Here's what to do next:

### 1. Explore More Models
- Try different models for different tasks
- Compare responses between models
- Test streaming responses

### 2. Integrate with Your Application
- Read the [API Integration Guide](api-integration.md)
- Try the examples in `/examples` folder
- Build your first AI-powered feature

### 3. Learn Configuration
- Read [Configuration Guide](configuration-guide.md)
- Customize routing strategies
- Set up load balancing

### 4. Secure Your Gateway
- Read [Security Guide](security-guide.md)
- Implement rate limiting
- Set up authentication

### 5. Monitor Usage
- Read [Monitoring Guide](monitoring-guide.md)
- Track costs across providers
- Analyze usage patterns

### 6. Deploy to Production
- Read [Production Deployment Guide](production-deployment.md)
- Set up HTTPS
- Configure backups

---

## Quick Reference Commands

```bash
# Start gateway
python start_gateway.py

# Test gateway
python test_gateway.py

# Validate setup
python validate_setup.py

# View logs
tail -f gateway.log

# Stop gateway
# Press Ctrl+C in the terminal running the gateway

# List models
curl http://localhost:4000/v1/models -H "Authorization: Bearer YOUR_KEY"

# Health check
curl http://localhost:4000/health
```

---

## Getting Help

### Documentation
- **Configuration**: [Configuration Guide](configuration-guide.md)
- **Models**: [Model Setup Guide](model-setup.md)
- **API Usage**: [API Integration Guide](api-integration.md)
- **Troubleshooting**: [Troubleshooting Guide](troubleshooting.md)

### Resources
- **Main README**: [../README.md](../README.md)
- **Examples**: [../examples/](../examples/)
- **LiteLLM Docs**: https://docs.litellm.ai/

### Support
- **GitHub Issues**: https://github.com/roshankhatrishin317-eng/shin-/issues
- **Email**: roshanshiloh31@gmail.com

---

## Summary

You've learned how to:
- ✅ Install the gateway and dependencies
- ✅ Configure environment variables
- ✅ Start the gateway server
- ✅ Make your first API call
- ✅ Explore available models
- ✅ Use the web dashboard

**You're ready to build amazing AI-powered applications!** 🎉

---

[⬅ Back to Guides](README.md) | [Next: Configuration Guide ➡](configuration-guide.md)


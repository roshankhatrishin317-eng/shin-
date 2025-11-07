# 🚀 Shin LiteLLM Gateway

<div align="center">

[![LiteLLM](https://img.shields.io/badge/LiteLLM-v1.44.0+-blue)](https://docs.litellm.ai/)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-shin--gateway-black)](https://github.com/roshankhatrishin317-eng/shin-.git)

**A unified, production-ready LLM gateway providing access to 20+ AI models through a single OpenAI-compatible API**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Configuration](#-configuration) • [Support](#-support)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Supported Models](#-supported-models)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [API Documentation](#-api-documentation)
- [Monitoring & Logging](#-monitoring--logging)
- [Production Deployment](#-production-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**Shin LiteLLM Gateway** is a powerful, production-ready proxy server built on [LiteLLM](https://docs.litellm.ai/) that provides unified access to multiple Large Language Model providers through a single, OpenAI-compatible API endpoint.

### Why Use This Gateway?

- 🔄 **Switch between 20+ models** without changing your code
- 🔌 **Drop-in OpenAI replacement** - works with existing OpenAI SDK code
- 🛡️ **Production-ready** with authentication, rate limiting, and monitoring
- 💰 **Cost optimization** through load balancing and fallback strategies
- 📊 **Built-in monitoring** with usage tracking and analytics
- 🚀 **Easy deployment** with Docker support and cloud-ready configuration

---

## ✨ Features

### Core Capabilities

- ✅ **100+ LLM Provider Support** - OpenAI, Anthropic, NVIDIA NIM, Azure, and more
- ✅ **OpenAI-Compatible API** - Drop-in replacement for OpenAI SDK
- ✅ **Load Balancing** - Distribute requests across multiple API keys and endpoints
- ✅ **Authentication & Security** - Master key authentication with API key management
- ✅ **Request Retry Logic** - Automatic retries with exponential backoff
- ✅ **Fallback Strategies** - Automatic failover to backup models
- ✅ **Response Caching** - Optional Redis caching to reduce costs
- ✅ **Cost Tracking** - Monitor spending across all providers
- ✅ **Usage Analytics** - Detailed logging and metrics
- ✅ **Rate Limiting** - Protect your API keys from overuse
- ✅ **Streaming Support** - Server-sent events for real-time responses

### Advanced Features

- 🔐 **Virtual Keys** - Generate separate API keys for different users/applications
- 📈 **Admin Dashboard** - Web UI for monitoring and management
- 🌐 **CORS Support** - Ready for web applications
- 🐳 **Docker Ready** - Easy containerized deployment
- 📝 **Comprehensive Logging** - SQLite database with detailed request logs
- 🔄 **Hot Reload** - Update configuration without downtime

---

## 🤖 Supported Models

This gateway provides access to **20+ AI models** from multiple providers:

### NVIDIA NIM Models (via NVIDIA API)
| Model Name | Provider | Description | Context |
|------------|----------|-------------|---------|
| `shin-llama-3-1-nemotron-70b` | NVIDIA | Llama 3.1 Nemotron 70B | 128K |
| `shin-llama-3-1-405b` | Meta | Llama 3.1 405B Instruct | 128K |
| `shin-llama-3-1-70b` | Meta | Llama 3.1 70B Instruct | 128K |
| `shin-llama-3-1-8b` | Meta | Llama 3.1 8B Instruct | 128K |
| `shin-mistral-nemo-12b` | Mistral | Mistral Nemo 12B | 128K |
| `shin-mistral-large-2` | Mistral | Mistral Large 2 | 128K |
| `shin-moonshotai-kimi-k2` | MoonshotAI | Kimi K2 Instruct | 128K |
| `shin-qwen-coder-480b` | Qwen | Qwen3 Coder 480B | 32K |
| `shin-minimax-m2` | MiniMax | MiniMax M2 | 128K |

### OpenCode.ai Provider
| Model Name | Provider | Description |
|------------|----------|-------------|
| `shin-4.6` | OpenCode.ai | Big Pickle Model |

### Z.ai Provider
| Model Name | Provider | Description |
|------------|----------|-------------|
| `glm-4.6` | Z.ai | GLM 4.6 |

### iFlow Provider (Otsu Models)
| Model Name | Provider | Description |
|------------|----------|-------------|
| `otsu-qwen3-coder-plus` | iFlow | Qwen3 Coder Plus |
| `otsu-qwen3-max` | iFlow | Qwen3 Max |
| `otsu-qwen3-coder` | iFlow | Qwen3 Coder |
| `otsu-kimi-k2-0905` | iFlow | Kimi K2 0905 |
| `otsu-glm-4.6` | iFlow | GLM 4.6 |
| `otsu-deepseek-v3.2` | iFlow | DeepSeek V3.2 |
| `otsu-qwen3-235b-thinking` | iFlow | Qwen3 235B Thinking |

### Minimax Provider
| Model Name | Provider | Description |
|------------|----------|-------------|
| `minimax1-claude` | Minimax | Claude Compatible |

### KAT Custom Endpoints
| Model Name | Provider | Description |
|------------|----------|-------------|
| `shin-otsu-pro` | KAT | Otsu Pro |
| `shin-otsu-plus` | KAT | Otsu Plus |

> **Note:** All models are accessible through the same OpenAI-compatible API interface.

---

## 🚀 Quick Start

Get up and running in 3 minutes!

### Prerequisites

- Python 3.8 or higher
- pip package manager
- API keys for the providers you want to use

### 1. Clone the Repository

```bash
git clone https://github.com/roshankhatrishin317-eng/shin-.git
cd shin-
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the environment template
cp env.template .env

# Edit .env and add your API keys
nano .env
```

**Minimum required variables:**
```bash
LITELLM_MASTER_KEY=sk-your-secret-master-key-here
NVIDIA_NIM_API_KEY=nvapi-your-nvidia-key
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1
```

### 4. Validate Setup

```bash
python validate_setup.py
```

### 5. Start the Gateway

```bash
python start_gateway.py
```

The gateway will start at: **http://localhost:4000**

### 6. Test It!

```bash
# In a new terminal
python test_gateway.py
```

🎉 **You're ready to go!**

---

## 📦 Installation

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/roshankhatrishin317-eng/shin-.git
cd shin-

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp env.template .env

# Edit configuration
nano .env
nano config.yaml  # Optional: customize model configurations
```

### Docker Installation (Coming Soon)

```bash
# Build the Docker image
docker build -t shin-gateway .

# Run the container
docker run -d -p 4000:4000 --env-file .env shin-gateway
```

### Production Installation

For production deployments, see the [Production Deployment Guide](guides/production-deployment.md).

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with your API keys:

```bash
# Gateway Configuration
LITELLM_MASTER_KEY=sk-1234567890abcdef  # Your gateway authentication key
LITELLM_PORT=4000                        # Port to run the gateway
LITELLM_HOST=0.0.0.0                     # Host to bind to

# Provider API Keys
NVIDIA_NIM_API_KEY=nvapi-xxxxx          # NVIDIA NIM API key
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1

OPENCODE_API_KEY=your-opencode-key      # OpenCode.ai API key
ZAI_API_KEY=your-zai-key                # Z.ai API key
IFLOW_API_KEY=your-iflow-key            # iFlow API key
MINIMAX1_API_KEY=your-minimax-key       # Minimax API key
KAT_API_KEY=your-kat-key                # KAT API key
```

### Gateway Settings (`config.yaml`)

The gateway behavior is controlled by `config.yaml`:

```yaml
# Model definitions
model_list:
  - model_name: shin-llama-3-1-70b
    litellm_params:
      model: nvidia_nim/meta/llama-3.1-70b-instruct
      api_key: os.environ/NVIDIA_NIM_API_KEY
      api_base: os.environ/NVIDIA_NIM_API_BASE

# Gateway settings
litellm_settings:
  drop_params: true
  set_verbose: true
  request_timeout: 600

# Security and authentication
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY

# Routing and load balancing
router_settings:
  routing_strategy: simple-shuffle
  num_retries: 3
  retry_after: 2
  timeout: 600
```

**📚 For detailed configuration options, see:**
- [Configuration Guide](guides/configuration-guide.md)
- [Model Setup Guide](guides/model-setup.md)
- [Security Guide](guides/security-guide.md)

---

## 💻 Usage Examples

### Python (OpenAI SDK)

```python
import openai

# Initialize client with your gateway
client = openai.OpenAI(
    api_key="sk-your-litellm-master-key",
    base_url="http://localhost:4000"
)

# Use any configured model
response = client.chat.completions.create(
    model="shin-llama-3-1-70b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ]
)

print(response.choices[0].message.content)
```

### cURL

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-your-litellm-master-key" \
  -d '{
    "model": "shin-llama-3-1-70b",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Streaming Responses

```python
response = client.chat.completions.create(
    model="shin-llama-3-1-70b",
    messages=[{"role": "user", "content": "Write a story"}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### JavaScript/Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'sk-your-litellm-master-key',
  baseURL: 'http://localhost:4000'
});

const response = await client.chat.completions.create({
  model: 'shin-llama-3-1-70b',
  messages: [{ role: 'user', content: 'Hello!' }]
});

console.log(response.choices[0].message.content);
```

**📚 More examples:**
- [examples/basic_usage.py](examples/basic_usage.py)
- [examples/curl_examples.sh](examples/curl_examples.sh)
- [examples/openai_compatible_demo.py](examples/openai_compatible_demo.py)

---

## 📚 API Documentation

### Endpoints

#### Chat Completions
```
POST /v1/chat/completions
```
OpenAI-compatible chat completions endpoint.

#### Models List
```
GET /v1/models
```
List all available models.

#### Health Check
```
GET /health
```
Check gateway health status.

#### Admin UI
```
GET /ui
```
Access the web-based admin dashboard.

### API Reference

For complete API documentation, visit:
- **Swagger UI**: http://localhost:4000/ (when gateway is running)
- **Admin Dashboard**: http://localhost:4000/ui
- **LiteLLM Docs**: https://docs.litellm.ai/docs/proxy/quick_start

---

## 📊 Monitoring & Logging

### Built-in Features

- **SQLite Database**: Stores all request logs, usage stats, and costs
- **Admin Dashboard**: Web UI at `http://localhost:4000/ui`
- **Health Endpoint**: `http://localhost:4000/health`
- **Verbose Logging**: Configurable log levels in `config.yaml`

### Log Files

- `gateway.log` - Gateway application logs
- `litellm.log` - LiteLLM proxy logs
- `tunnel.log` - Cloudflare tunnel logs (if using public access)

### Monitoring Metrics

The gateway tracks:
- ✅ Request count per model
- ✅ Token usage (input/output)
- ✅ Response times
- ✅ Error rates
- ✅ Cost per request
- ✅ API key usage

**📚 See:** [Monitoring Guide](guides/monitoring-guide.md)

---

## 🌐 Production Deployment

### Security Checklist

- ✅ Use strong, unique `LITELLM_MASTER_KEY`
- ✅ Never commit `.env` file to version control
- ✅ Use HTTPS in production (reverse proxy recommended)
- ✅ Implement rate limiting
- ✅ Restrict network access (firewall rules)
- ✅ Regularly rotate API keys
- ✅ Monitor logs for suspicious activity

### Deployment Options

1. **VPS/Cloud Server** - Deploy on AWS, DigitalOcean, etc.
2. **Docker Container** - Containerized deployment
3. **Kubernetes** - Scalable orchestration
4. **Cloudflare Tunnel** - Secure public access (included)

### Public Access with Cloudflare

This gateway includes Cloudflare Tunnel support for secure public access:

```bash
# Start gateway with public tunnel
./manage_tunnel.sh start
```

**📚 See:**
- [Production Deployment Guide](guides/production-deployment.md)
- [Security Best Practices](guides/security-guide.md)
- [Public Access Setup](PUBLIC_URL.md)

---

## 🛠️ Troubleshooting

### Common Issues

#### Gateway Won't Start

```bash
# Check if port is in use
lsof -i :4000

# Validate configuration
python validate_setup.py

# Check logs
tail -f gateway.log
```

#### Authentication Errors

- Verify `LITELLM_MASTER_KEY` matches in `.env` and client
- Check that provider API keys are correct
- Ensure API keys have proper permissions

#### Model Not Found

- Confirm model is defined in `config.yaml`
- Verify provider API key is set
- Check model name spelling

#### Timeout Errors

- Increase `request_timeout` in `config.yaml`
- Check provider API status
- Verify network connectivity

**📚 See:** [Troubleshooting Guide](guides/troubleshooting.md)

---

## 📖 Documentation

### Guides

- 📘 [Getting Started Guide](guides/getting-started.md)
- ⚙️ [Configuration Guide](guides/configuration-guide.md)
- 🤖 [Model Setup Guide](guides/model-setup.md)
- 🔐 [Security Guide](guides/security-guide.md)
- 📊 [Monitoring Guide](guides/monitoring-guide.md)
- 🚀 [Production Deployment](guides/production-deployment.md)
- 🐛 [Troubleshooting Guide](guides/troubleshooting.md)
- 🔌 [API Integration Guide](guides/api-integration.md)

### Reference Documentation

- [All Models List](MODELS.md)
- [Models by Provider](MODELS_BY_PROVIDER.md)
- [Quick Reference](QUICK_REFERENCE.md)
- [Master Key Info](MASTER_KEY_INFO.md)
- [External Access](EXTERNAL_ACCESS.md)

### Official LiteLLM Documentation

- **Main Docs**: https://docs.litellm.ai/docs/
- **Proxy Guide**: https://docs.litellm.ai/docs/proxy/quick_start
- **Providers**: https://docs.litellm.ai/docs/providers
- **GitHub**: https://github.com/BerriAI/litellm

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs** - Open an issue with details
2. **Suggest Features** - Share your ideas
3. **Submit PRs** - Improve code or documentation
4. **Share Examples** - Add usage examples
5. **Improve Docs** - Help others get started

### Development Setup

```bash
# Fork and clone the repo
git clone https://github.com/YOUR_USERNAME/shin-.git
cd shin-

# Create a branch
git checkout -b feature/your-feature

# Make changes and test
python test_gateway.py

# Submit PR
git push origin feature/your-feature
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LiteLLM** - Amazing proxy framework ([GitHub](https://github.com/BerriAI/litellm))
- **NVIDIA** - NIM API access
- All the AI model providers making this possible

---

## 📞 Support

### Need Help?

- 📖 **Documentation**: Check the [guides](guides/) folder
- 🐛 **Bug Reports**: Open an [issue](https://github.com/roshankhatrishin317-eng/shin-/issues)
- 💬 **Discussions**: Join our [discussions](https://github.com/roshankhatrishin317-eng/shin-/discussions)
- 📧 **Email**: roshanshiloh31@gmail.com

### Useful Links

- 🌐 **GitHub**: https://github.com/roshankhatrishin317-eng/shin-.git
- 📚 **LiteLLM Docs**: https://docs.litellm.ai/
- 🚀 **NVIDIA NIM**: https://docs.api.nvidia.com/nim/

---

<div align="center">

**Made with ❤️ by Roshan Khatri**

⭐ Star this repo if you find it helpful!

[⬆ Back to Top](#-shin-litellm-gateway)

</div>

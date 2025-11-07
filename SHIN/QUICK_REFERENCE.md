# LiteLLM Gateway - Quick Reference

## 📁 Files Created

- `requirements.txt` - Python dependencies
- `config.yaml` - LiteLLM configuration (models, providers, settings)
- `env.template` - Environment variables template
- `start_gateway.py` - Main script to start the gateway
- `test_gateway.py` - Test script to verify the gateway
- `quick-start.sh` - Automated setup and start script
- `README.md` - Complete documentation
- `.gitignore` - Git ignore rules

## 🚀 Quick Start (3 Steps)

### 1️⃣ Set up your environment
```bash
cp env.template .env
nano .env  # Add your API keys
```

### 2️⃣ Start the gateway
```bash
python start_gateway.py
```

Or use the quick start script:
```bash
./quick-start.sh
```

### 3️⃣ Test it (in another terminal)
```bash
python test_gateway.py
```

## 🔑 Required Environment Variables

At minimum, you need:
- `LITELLM_MASTER_KEY` - Authentication key for your gateway
- One or more provider API keys:
  - `OPENAI_API_KEY` - For GPT models
  - `ANTHROPIC_API_KEY` - For Claude models

## 📡 Using the Gateway

### Python Example
```python
import openai

client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

### cURL Example
```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## 🎯 Available Models (by default)

Configure in `config.yaml`:
- `gpt-4` - OpenAI GPT-4
- `gpt-3.5-turbo` - OpenAI GPT-3.5 Turbo
- `claude-3-5-sonnet` - Anthropic Claude 3.5 Sonnet
- `claude-3-opus` - Anthropic Claude 3 Opus

## 🛠️ Common Commands

| Command | Description |
|---------|-------------|
| `python start_gateway.py` | Start the gateway server |
| `python test_gateway.py` | Test the gateway |
| `./quick-start.sh` | Automated setup and start |
| `litellm --help` | View all CLI options |

## 🌐 Default Settings

- **Port:** 4000
- **Host:** 0.0.0.0 (all interfaces)
- **Database:** SQLite (`litellm.db`)
- **Config:** `config.yaml`

## 🔧 Customization

### Change Port
Set in `.env`:
```bash
LITELLM_PORT=8000
```

### Add New Model
Edit `config.yaml`:
```yaml
- model_name: my-model
  litellm_params:
    model: provider/model-name
    api_key: os.environ/PROVIDER_API_KEY
```

### Enable Caching
Uncomment in `config.yaml`:
```yaml
litellm_settings:
  cache: true
```

## 📊 Monitoring

- Admin UI: `http://localhost:4000/ui`
- Health Check: `http://localhost:4000/health`
- Database: `litellm.db` (view with SQLite tools)

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change `LITELLM_PORT` in `.env` |
| Authentication error | Check `LITELLM_MASTER_KEY` matches |
| Model not found | Add model to `config.yaml` |
| Provider error | Verify API key is correct and active |

## 📚 Resources

- [Full Documentation](README.md)
- [LiteLLM Docs](https://docs.litellm.ai/)
- [Supported Providers](https://docs.litellm.ai/docs/providers)
- [GitHub](https://github.com/BerriAI/litellm)


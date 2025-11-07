# LiteLLM Gateway Setup

This is a complete LiteLLM Gateway setup based on the official documentation at [https://docs.litellm.ai/docs/](https://docs.litellm.ai/docs/).

**LiteLLM Gateway** provides a unified interface for 100+ LLM providers (OpenAI, Anthropic, Azure OpenAI, and more) with a single OpenAI-compatible API.

## 🌟 Features

- **Unified API**: Use OpenAI-compatible API for all LLM providers
- **Load Balancing**: Distribute requests across multiple models/instances
- **Authentication**: Secure your gateway with master keys
- **Logging & Monitoring**: Track usage, costs, and performance
- **Retries & Fallbacks**: Automatic retry logic and fallback models
- **Caching**: Optional response caching to reduce costs

## ✅ Validate Your Setup

Before starting, run the validation script to ensure everything is configured correctly:

```bash
python validate_setup.py
```

This will check:
- ✅ All required files are present
- ✅ Dependencies are installed (LiteLLM v1.79.1)
- ✅ Configuration is valid
- ✅ Environment variables are set

## 📦 Installation

### Step 1: Install dependencies (Already Done! ✅)

```bash
pip install -r requirements.txt
```

### Step 2: Configure environment variables

```bash
cp env.template .env
nano .env  # Edit and add your API keys
```

**Required variables:**
- `LITELLM_MASTER_KEY` - Your gateway authentication key (create your own)
- `OPENAI_API_KEY` - Your OpenAI API key (for GPT models)
- `ANTHROPIC_API_KEY` - Your Anthropic API key (for Claude models)

### Step 3: Update configuration (optional)

Edit `config.yaml` to add/remove models or adjust settings. The default configuration includes:
- OpenAI: GPT-4o, GPT-4, GPT-3.5-turbo
- Anthropic: Claude 3.5 Sonnet, Claude 3 Opus

## 🚀 Quick Start

### Start the Gateway

```bash
python start_gateway.py
```

Or use the LiteLLM CLI directly:
```bash
litellm --config config.yaml --host 0.0.0.0 --port 4000
```

The gateway will be available at: `http://localhost:4000`

### Test the Gateway

In a separate terminal:
```bash
python test_gateway.py
```

## 🔧 Configuration

### Environment Variables (.env)

- `LITELLM_MASTER_KEY`: Master key for authenticating with the proxy
- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `LITELLM_PORT`: Port to run the gateway (default: 4000)
- `LITELLM_HOST`: Host to bind to (default: 0.0.0.0)

### Config File (config.yaml)

The `config.yaml` file defines:
- **model_list**: Available models and their configurations
- **litellm_settings**: Request handling, caching, timeouts
- **general_settings**: Database, logging, authentication
- **router_settings**: Load balancing and routing strategies

## 📡 Using the Gateway

### Python (OpenAI SDK)

```python
import openai

client = openai.OpenAI(
    api_key="your-litellm-master-key",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # or any model in your config
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

### cURL

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-litellm-master-key" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Using Different Models

The gateway supports 100+ providers. Pre-configured models include:

| Model Name | Provider | Description |
|------------|----------|-------------|
| `gpt-4o` | OpenAI | Latest GPT-4 Optimized |
| `gpt-4` | OpenAI | GPT-4 |
| `gpt-3.5-turbo` | OpenAI | GPT-3.5 Turbo |
| `claude-3-5-sonnet` | Anthropic | Claude 3.5 Sonnet |
| `claude-3-opus` | Anthropic | Claude 3 Opus |

Just change the `model` parameter in your requests!

For more providers, see: [https://docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers)

## 🔐 Security

1. **Always use a strong master key** in production
2. **Never commit .env file** to version control
3. **Use HTTPS** in production (consider a reverse proxy like Nginx)
4. **Restrict network access** if not needed publicly

## 📊 Monitoring

LiteLLM creates a SQLite database (`litellm.db`) to store:
- Request logs
- Token usage
- Error tracking
- Performance metrics

Access the admin UI at: `http://localhost:4000/ui` (if enabled)

## 🛠️ Advanced Configuration

### Adding More Models

Edit `config.yaml` and add to `model_list`:

```yaml
- model_name: my-custom-model
  litellm_params:
    model: provider/model-name
    api_key: os.environ/PROVIDER_API_KEY
```

### Enable Caching

Uncomment cache settings in `config.yaml`:

```yaml
litellm_settings:
  cache: true
  cache_params:
    type: "redis"
    host: "localhost"
    port: 6379
```

### Load Balancing

Add multiple instances of the same model with different API keys:

```yaml
- model_name: gpt-4
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_API_KEY_1

- model_name: gpt-4
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_API_KEY_2
```

## 📚 Official Resources

- **Documentation:** [https://docs.litellm.ai/docs/](https://docs.litellm.ai/docs/)
- **Proxy Quick Start:** [https://docs.litellm.ai/docs/proxy/quick_start](https://docs.litellm.ai/docs/proxy/quick_start)
- **Supported Providers:** [https://docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers)
- **GitHub Repository:** [https://github.com/BerriAI/litellm](https://github.com/BerriAI/litellm)
- **Swagger API Docs:** Available at `http://localhost:4000/` when running

## 🐛 Troubleshooting

### Gateway won't start
- Check if port 4000 is already in use
- Verify `config.yaml` syntax
- Ensure all required environment variables are set

### Authentication errors
- Verify `LITELLM_MASTER_KEY` matches between server and client
- Check that provider API keys (OpenAI, Anthropic) are correct

### Model not found
- Ensure the model is defined in `config.yaml`
- Check that the model name matches exactly
- Verify provider API key is set for that model

## 🤝 Contributing

Feel free to customize this setup for your needs! Add more models, adjust settings, or integrate with your existing infrastructure.

## 📝 License

This setup is provided as-is for your use. LiteLLM itself is licensed under the MIT License.


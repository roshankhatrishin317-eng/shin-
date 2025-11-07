# ⚙️ Configuration Guide

This guide covers all configuration options for the Shin LiteLLM Gateway.

## 📋 Table of Contents

1. [Configuration Files Overview](#configuration-files-overview)
2. [Environment Variables](#environment-variables)
3. [config.yaml Structure](#configyaml-structure)
4. [Model Configuration](#model-configuration)
5. [Gateway Settings](#gateway-settings)
6. [Router Settings](#router-settings)
7. [Advanced Configuration](#advanced-configuration)
8. [Configuration Best Practices](#configuration-best-practices)

---

## Configuration Files Overview

The gateway uses two main configuration files:

| File | Purpose | Format |
|------|---------|--------|
| `.env` | API keys and secrets | Key-value pairs |
| `config.yaml` | Gateway behavior and models | YAML |

### File Locations

```
shin-/
├── .env                 # Environment variables (create from env.template)
├── env.template         # Template for .env
└── config.yaml          # Main configuration file
```

---

## Environment Variables

### Creating the .env File

```bash
cp env.template .env
nano .env
```

### Required Variables

```bash
# Gateway Master Key (REQUIRED)
LITELLM_MASTER_KEY=sk-your-secret-key-here
```

### Server Configuration

```bash
# Server settings
LITELLM_PORT=4000                    # Port to run on (default: 4000)
LITELLM_HOST=0.0.0.0                 # Host to bind to (default: 0.0.0.0)
```

### Provider API Keys

```bash
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

### Optional Variables

```bash
# Logging
LOG_LEVEL=INFO                       # DEBUG, INFO, WARNING, ERROR

# Database
DATABASE_URL=sqlite:///litellm.db   # Database connection string

# Caching
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
```

### Security Note

⚠️ **Never commit `.env` to version control!**

The `.gitignore` file should include:
```
.env
*.env
.env.*
```

---

## config.yaml Structure

The `config.yaml` file has four main sections:

```yaml
model_list:           # Define available models
litellm_settings:     # Request handling settings
general_settings:     # Authentication and database
router_settings:      # Load balancing and routing
```

---

## Model Configuration

### Basic Model Definition

```yaml
model_list:
  - model_name: my-model-name       # Name to use in API requests
    litellm_params:
      model: provider/actual-model  # Provider and model identifier
      api_key: os.environ/API_KEY   # Reference to environment variable
      api_base: os.environ/API_BASE # API endpoint
```

### NVIDIA NIM Models

```yaml
- model_name: shin-llama-3-1-70b
  litellm_params:
    model: nvidia_nim/meta/llama-3.1-70b-instruct
    api_key: os.environ/NVIDIA_NIM_API_KEY
    api_base: os.environ/NVIDIA_NIM_API_BASE
```

### OpenAI-Compatible Endpoints

```yaml
- model_name: custom-model
  litellm_params:
    model: openai/model-name
    api_key: os.environ/CUSTOM_API_KEY
    api_base: https://api.example.com/v1
```

### Model with Custom Parameters

```yaml
- model_name: custom-gpt
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_API_KEY
    temperature: 0.7
    max_tokens: 2000
    top_p: 0.9
```

### Multiple Instances (Load Balancing)

```yaml
# First instance
- model_name: gpt-4
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_KEY_1

# Second instance
- model_name: gpt-4
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_KEY_2
```

---

## Gateway Settings

### litellm_settings Section

```yaml
litellm_settings:
  # Drop unknown parameters (recommended)
  drop_params: true
  
  # Enable verbose logging
  set_verbose: true
  
  # Request timeout (seconds)
  request_timeout: 600
  
  # Max parallel requests
  max_parallel_requests: 1000
  
  # Enable telemetry (anonymous usage stats)
  telemetry: false
```

### Request Handling

```yaml
litellm_settings:
  # Timeouts
  request_timeout: 600              # Total request timeout
  stream_timeout: 300               # Streaming timeout
  
  # Retry configuration
  num_retries: 3                    # Number of retries
  retry_after: 2                    # Seconds between retries
  
  # Rate limiting
  rpm: 1000                         # Requests per minute
  tpm: 100000                       # Tokens per minute
```

### Caching Configuration

#### Redis Cache

```yaml
litellm_settings:
  cache: true
  cache_params:
    type: "redis"
    host: os.environ/REDIS_HOST
    port: os.environ/REDIS_PORT
    password: os.environ/REDIS_PASSWORD
    ttl: 3600                       # Cache TTL in seconds
```

#### In-Memory Cache

```yaml
litellm_settings:
  cache: true
  cache_params:
    type: "local"
    ttl: 600
```

### Success Callbacks

```yaml
litellm_settings:
  success_callback: ["langfuse", "slack"]
  failure_callback: ["slack"]
```

---

## General Settings

### Authentication

```yaml
general_settings:
  # Master key (required)
  master_key: os.environ/LITELLM_MASTER_KEY
  
  # Additional security
  allowed_ips: ["127.0.0.1", "192.168.1.0/24"]
  
  # CORS
  cors_origin: "*"                  # or specific domains
```

### Database Configuration

```yaml
general_settings:
  # SQLite (default)
  database_url: "sqlite:///litellm.db"
  
  # PostgreSQL
  # database_url: "postgresql://user:pass@localhost/litellm"
```

### Logging

```yaml
general_settings:
  # Log level
  log_level: "INFO"                 # DEBUG, INFO, WARNING, ERROR
  
  # Log file
  log_file: "gateway.log"
  
  # JSON logging
  json_logs: true
```

### UI Settings

```yaml
general_settings:
  # Admin UI
  ui_username: "admin"
  ui_password: os.environ/UI_PASSWORD
  
  # Disable UI
  # ui_enabled: false
```

---

## Router Settings

### Routing Strategy

```yaml
router_settings:
  # Options: simple-shuffle, least-busy, usage-based-routing, latency-based-routing
  routing_strategy: simple-shuffle
```

#### Routing Strategies Explained

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `simple-shuffle` | Random selection | Default, simple load balancing |
| `least-busy` | Route to least busy endpoint | Even distribution |
| `usage-based-routing` | Based on usage limits | Quota management |
| `latency-based-routing` | Fastest endpoint | Performance optimization |

### Retry Configuration

```yaml
router_settings:
  # Retry settings
  num_retries: 3                    # Number of retry attempts
  retry_after: 2                    # Seconds to wait before retry
  timeout: 600                      # Request timeout in seconds
  
  # Exponential backoff
  retry_policy: "exponential"       # or "constant"
```

### Fallback Configuration

```yaml
router_settings:
  # Fallback models
  fallback_models:
    gpt-4: ["gpt-3.5-turbo"]
    claude-3-opus: ["claude-3-sonnet"]
```

### Load Balancing

```yaml
router_settings:
  # Enable load balancing
  enable_loadbalancing: true
  
  # Load balancing strategy
  loadbalancing_strategy: "round-robin"  # or "weighted"
```

---

## Advanced Configuration

### Custom Model Aliases

```yaml
model_list:
  # Create an alias
  - model_name: my-gpt               # Custom name
    litellm_params:
      model: gpt-4                   # Actual model
      api_key: os.environ/OPENAI_API_KEY
```

### Model-Specific Timeouts

```yaml
model_list:
  - model_name: slow-model
    litellm_params:
      model: provider/model
      api_key: os.environ/API_KEY
      timeout: 900                   # 15 minutes
```

### Default Model Parameters

```yaml
model_list:
  - model_name: configured-gpt
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY
      # Default parameters
      temperature: 0.7
      max_tokens: 2000
      top_p: 0.9
      frequency_penalty: 0.0
      presence_penalty: 0.0
```

### Region-Specific Configuration

```yaml
model_list:
  # US Region
  - model_name: gpt-4-us
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_KEY_US
      api_base: https://api.openai.com/v1
  
  # EU Region
  - model_name: gpt-4-eu
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_KEY_EU
      api_base: https://api.openai.eu/v1
```

### Budget Limits

```yaml
litellm_settings:
  # Global budget
  max_budget: 100.00                # USD per month
  
  # Budget window
  budget_duration: "30d"            # 1d, 7d, 30d, etc.
```

### Model-Specific Budget

```yaml
model_list:
  - model_name: expensive-model
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY
      max_budget: 50.00
```

---

## Configuration Best Practices

### 1. Security

✅ **DO:**
- Use environment variables for all secrets
- Use strong master keys (20+ characters)
- Restrict CORS origins in production
- Enable rate limiting
- Use HTTPS in production

❌ **DON'T:**
- Hard-code API keys in config.yaml
- Use simple/predictable master keys
- Allow CORS from `*` in production
- Commit `.env` to version control

### 2. Performance

✅ **DO:**
- Enable caching for repeated queries
- Use load balancing for high traffic
- Set appropriate timeouts
- Configure retry logic
- Monitor usage patterns

❌ **DON'T:**
- Set timeout too low (<60s)
- Disable retries completely
- Use single API key for high traffic

### 3. Reliability

✅ **DO:**
- Configure fallback models
- Use multiple API keys for load balancing
- Enable error callbacks
- Set up health checks
- Monitor logs regularly

❌ **DON'T:**
- Rely on single provider
- Ignore error logs
- Skip health monitoring

### 4. Cost Optimization

✅ **DO:**
- Set budget limits
- Use caching
- Choose appropriate models for tasks
- Monitor token usage
- Implement rate limiting

❌ **DON'T:**
- Use expensive models for simple tasks
- Disable caching
- Ignore cost analytics

### 5. Development Workflow

✅ **DO:**
- Use separate configs for dev/prod
- Version control config.yaml
- Document custom configurations
- Test changes in development
- Use environment-specific .env files

❌ **DON'T:**
- Test in production
- Skip validation
- Use production keys in development

---

## Configuration Examples

### Example 1: Simple Setup

```yaml
model_list:
  - model_name: default-llm
    litellm_params:
      model: nvidia_nim/meta/llama-3.1-70b-instruct
      api_key: os.environ/NVIDIA_NIM_API_KEY
      api_base: os.environ/NVIDIA_NIM_API_BASE

litellm_settings:
  drop_params: true
  request_timeout: 300

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

### Example 2: High Availability

```yaml
model_list:
  # Primary
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_KEY_1
  
  # Backup
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_KEY_2

router_settings:
  routing_strategy: least-busy
  num_retries: 5
  fallback_models:
    gpt-4: ["gpt-3.5-turbo"]
```

### Example 3: Cost-Optimized

```yaml
model_list:
  - model_name: cheap-model
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY
      max_tokens: 500

litellm_settings:
  cache: true
  cache_params:
    type: "redis"
    host: "localhost"
    port: 6379
    ttl: 3600

router_settings:
  enable_loadbalancing: true
```

---

## Validation

### Validate Configuration

```bash
# Check syntax
python validate_setup.py

# Test configuration
litellm --config config.yaml --test
```

### Common Validation Errors

1. **Invalid YAML syntax**
   - Check indentation (use spaces, not tabs)
   - Verify quotes and colons

2. **Missing environment variables**
   - Ensure all referenced vars exist in `.env`
   - Check spelling

3. **Invalid model names**
   - Verify provider format
   - Check LiteLLM documentation for correct names

---

## Hot Reloading

Some changes don't require restart:

```bash
# Reload configuration
kill -HUP $(cat gateway.pid)
```

**Note:** Model list changes require full restart.

---

## Configuration Templates

### Development

```yaml
general_settings:
  master_key: "sk-dev-key-123"
  log_level: "DEBUG"
  
litellm_settings:
  set_verbose: true
```

### Production

```yaml
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  log_level: "INFO"
  json_logs: true
  allowed_ips: ["10.0.0.0/8"]
  
litellm_settings:
  cache: true
  telemetry: false
  
router_settings:
  enable_loadbalancing: true
  num_retries: 5
```

---

## Next Steps

- **Add Models**: See [Model Setup Guide](model-setup.md)
- **Secure Gateway**: See [Security Guide](security-guide.md)
- **Monitor Usage**: See [Monitoring Guide](monitoring-guide.md)

---

[⬅ Back to Guides](README.md) | [Next: Model Setup ➡](model-setup.md)


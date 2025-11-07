# 🐛 Troubleshooting Guide

Solutions to common issues and problems with Shin LiteLLM Gateway.

## 📋 Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Gateway Won't Start](#gateway-wont-start)
3. [Authentication Issues](#authentication-issues)
4. [Model Errors](#model-errors)
5. [Performance Issues](#performance-issues)
6. [Network Problems](#network-problems)
7. [Database Issues](#database-issues)
8. [Provider-Specific Issues](#provider-specific-issues)

---

## Quick Diagnostics

### Health Check

```bash
# Check if gateway is running
curl http://localhost:4000/health

# Expected response
{"status": "healthy", "uptime": 123456}
```

### Validation Script

```bash
python validate_setup.py
```

### Check Logs

```bash
# Gateway logs
tail -f gateway.log

# LiteLLM logs
tail -f litellm.log

# System logs (if using systemd)
sudo journalctl -u litellm -f
```

### List Models

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer YOUR_MASTER_KEY"
```

---

## Gateway Won't Start

### Issue 1: Port Already in Use

**Error:**
```
Address already in use: 4000
```

**Solution:**

```bash
# Find what's using the port
lsof -i :4000
# or
netstat -tuln | grep 4000

# Kill the process
kill -9 <PID>

# Or use a different port
export LITELLM_PORT=4001
python start_gateway.py
```

### Issue 2: Import Error

**Error:**
```
ModuleNotFoundError: No module named 'litellm'
```

**Solution:**

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep litellm

# If still failing, use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 3: Configuration Syntax Error

**Error:**
```
yaml.parser.ParserError: while parsing a block mapping
```

**Solution:**

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Common issues:
# 1. Incorrect indentation (use spaces, not tabs)
# 2. Missing colons
# 3. Mismatched quotes

# Check specific line
grep -n "^" config.yaml | head -20
```

### Issue 4: Environment Variables Not Loaded

**Error:**
```
KeyError: 'LITELLM_MASTER_KEY'
```

**Solution:**

```bash
# Check .env file exists
ls -la .env

# Load manually
source .env  # Won't work
export $(cat .env | xargs)  # Works

# Or use python-dotenv
pip install python-dotenv

# Verify variables
echo $LITELLM_MASTER_KEY
```

### Issue 5: Permission Denied

**Error:**
```
Permission denied: './start_gateway.py'
```

**Solution:**

```bash
# Make executable
chmod +x start_gateway.py

# Or run with python
python start_gateway.py
```

---

## Authentication Issues

### Issue 1: Invalid Master Key

**Error:**
```
Authentication failed: Invalid API key
```

**Solutions:**

```bash
# 1. Check key in .env
cat .env | grep LITELLM_MASTER_KEY

# 2. Verify key in request
# Should be: Authorization: Bearer YOUR_KEY

# 3. Check for typos/spaces
# Bad:  "Bearer  key" (double space)
# Good: "Bearer key"

# 4. Verify config references it correctly
grep master_key config.yaml
```

### Issue 2: Provider API Key Invalid

**Error:**
```
AuthenticationError: Invalid API key for provider
```

**Solutions:**

```bash
# 1. Check provider key exists
echo $NVIDIA_NIM_API_KEY

# 2. Test key directly with provider
curl https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer $NVIDIA_NIM_API_KEY"

# 3. Regenerate key from provider dashboard

# 4. Check key format
# NVIDIA: nvapi-xxxxx
# OpenAI: sk-xxxxx
# Anthropic: sk-ant-xxxxx
```

### Issue 3: Token Expired

**Error:**
```
Token has expired
```

**Solution:**

```bash
# Virtual keys can expire
# Check key info
curl http://localhost:4000/key/info \
  -H "Authorization: Bearer YOUR_MASTER_KEY"

# Regenerate expired key
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{"user_id": "user123", "duration": "30d"}'
```

---

## Model Errors

### Issue 1: Model Not Found

**Error:**
```
Model not found: shin-llama-70b
```

**Solutions:**

```bash
# 1. List available models
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer YOUR_KEY"

# 2. Check model exists in config.yaml
grep "model_name: shin-llama-70b" config.yaml

# 3. Verify exact spelling
# Wrong: shin-llama-70B (capital B)
# Right: shin-llama-70b

# 4. Restart gateway after config changes
python start_gateway.py
```

### Issue 2: Model Timeout

**Error:**
```
Request timeout after 600 seconds
```

**Solutions:**

```yaml
# Increase timeout for specific model
- model_name: slow-model
  litellm_params:
    model: provider/model
    api_key: os.environ/API_KEY
    timeout: 1200  # 20 minutes

# Or increase globally
litellm_settings:
  request_timeout: 900

router_settings:
  timeout: 900
```

### Issue 3: Rate Limit Exceeded

**Error:**
```
RateLimitError: Rate limit exceeded
```

**Solutions:**

1. **Add more API keys for load balancing:**

```yaml
- model_name: gpt-4
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_KEY_1

- model_name: gpt-4
  litellm_params:
    model: gpt-4
    api_key: os.environ/OPENAI_KEY_2
```

2. **Implement rate limiting:**

```yaml
litellm_settings:
  rpm: 100  # Limit requests
```

3. **Use cheaper models:**

```yaml
router_settings:
  fallback_models:
    gpt-4: ["gpt-3.5-turbo"]
```

### Issue 4: Invalid Parameters

**Error:**
```
Invalid parameter: temperature must be between 0 and 2
```

**Solution:**

```yaml
# Enable parameter dropping
litellm_settings:
  drop_params: true  # Drops unknown/invalid params

# Or fix the parameter
temperature: 0.7  # Valid range: 0-2
```

---

## Performance Issues

### Issue 1: Slow Response Times

**Symptoms:**
- Requests taking > 30 seconds
- Timeouts
- High latency

**Solutions:**

```bash
# 1. Check server resources
htop
free -h
df -h

# 2. Monitor gateway logs
tail -f gateway.log | grep "latency"

# 3. Test network to provider
curl -w "@curl-format.txt" https://integrate.api.nvidia.com/v1/models

# 4. Enable caching
```

```yaml
litellm_settings:
  cache: true
  cache_params:
    type: "redis"
    host: "localhost"
    port: 6379
```

### Issue 2: High Memory Usage

**Symptoms:**
- Memory > 90%
- OOM errors
- Gateway crashes

**Solutions:**

```bash
# 1. Check memory usage
free -m
ps aux | grep python | awk '{print $6/1024 " MB\t" $11}'

# 2. Limit concurrent requests
```

```yaml
litellm_settings:
  max_parallel_requests: 100  # Adjust as needed
```

```bash
# 3. Restart gateway regularly
# Add to crontab
0 3 * * * systemctl restart litellm
```

### Issue 3: Gateway Crashes

**Symptoms:**
- Gateway stops responding
- Process dies
- No response

**Solutions:**

```bash
# 1. Check logs for errors
tail -100 gateway.log
sudo journalctl -u litellm -n 100

# 2. Enable auto-restart
```

```ini
# In systemd service file
[Service]
Restart=always
RestartSec=10
```

```bash
# 3. Monitor with process manager
pm2 start start_gateway.py --name litellm --interpreter python3
```

---

## Network Problems

### Issue 1: Cannot Connect to Gateway

**Error:**
```
Connection refused
```

**Solutions:**

```bash
# 1. Check gateway is running
curl http://localhost:4000/health

# 2. Check port binding
netstat -tuln | grep 4000

# 3. Check firewall
sudo ufw status
sudo iptables -L

# 4. Verify host setting
# In .env
LITELLM_HOST=0.0.0.0  # Listen on all interfaces
```

### Issue 2: CORS Errors

**Error:**
```
Access to fetch at 'http://localhost:4000' has been blocked by CORS policy
```

**Solution:**

```yaml
# In config.yaml
general_settings:
  cors_origin: "*"  # Development

  # Production (specific domains)
  cors_origin:
    - "https://yourdomain.com"
    - "https://app.yourdomain.com"
```

### Issue 3: SSL/TLS Errors

**Error:**
```
SSL certificate verify failed
```

**Solutions:**

```bash
# 1. Check certificate
curl -v https://api.yourdomain.com

# 2. Renew certificate
sudo certbot renew

# 3. Check nginx config
sudo nginx -t

# 4. Verify certificate chain
openssl s_client -connect api.yourdomain.com:443
```

---

## Database Issues

### Issue 1: Database Locked

**Error:**
```
database is locked
```

**Solutions:**

```bash
# 1. Close other connections
lsof litellm.db

# 2. Use PostgreSQL instead of SQLite
```

```yaml
general_settings:
  database_url: "postgresql://user:pass@localhost/litellm"
```

```bash
# 3. Restart gateway
systemctl restart litellm
```

### Issue 2: Database Corruption

**Error:**
```
database disk image is malformed
```

**Solutions:**

```bash
# 1. Restore from backup
cp backups/litellm_latest.db litellm.db

# 2. Try to recover
sqlite3 litellm.db ".recover" | sqlite3 litellm_recovered.db

# 3. Start fresh (loses history)
rm litellm.db
python start_gateway.py
```

---

## Provider-Specific Issues

### NVIDIA NIM Issues

**Error:**
```
NVIDIA API error: Model not available
```

**Solutions:**

```bash
# 1. Verify API key
curl https://integrate.api.nvidia.com/v1/models \
  -H "Authorization: Bearer $NVIDIA_NIM_API_KEY"

# 2. Check model name
# See: https://docs.api.nvidia.com/nim/

# 3. Some models require specific format
```

```yaml
- model_name: shin-llama-405b
  litellm_params:
    model: nvidia_nim/meta/llama-3.1-405b-instruct  # Correct format
    api_key: os.environ/NVIDIA_NIM_API_KEY
    api_base: https://integrate.api.nvidia.com/v1
```

### OpenAI Issues

**Error:**
```
OpenAI API error: Insufficient quota
```

**Solutions:**

```bash
# 1. Check billing
# https://platform.openai.com/account/billing

# 2. Use fallback model
```

```yaml
router_settings:
  fallback_models:
    gpt-4: ["gpt-3.5-turbo"]
```

### Anthropic Issues

**Error:**
```
Anthropic API error: overloaded_error
```

**Solutions:**

```yaml
# Enable retries
router_settings:
  num_retries: 5
  retry_after: 5

# Add fallback
fallback_models:
  claude-3-opus: ["claude-3-sonnet", "gpt-4"]
```

---

## Debugging Tips

### Enable Debug Logging

```yaml
# In config.yaml
general_settings:
  log_level: "DEBUG"

litellm_settings:
  set_verbose: true
```

### Test Individual Components

```python
# Test LiteLLM directly
import litellm
litellm.set_verbose = True

response = litellm.completion(
    model="nvidia_nim/meta/llama-3.1-70b-instruct",
    messages=[{"role": "user", "content": "test"}],
    api_key="nvapi-xxx",
    api_base="https://integrate.api.nvidia.com/v1"
)
print(response)
```

### Isolate the Problem

```bash
# 1. Test provider directly
curl https://api.provider.com/v1/models \
  -H "Authorization: Bearer $API_KEY"

# 2. Test LiteLLM proxy
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $MASTER_KEY" \
  -d '{"model": "test-model", "messages": [{"role": "user", "content": "test"}]}'

# 3. Test from client application
python test_gateway.py
```

---

## Getting Help

### Before Asking for Help

1. ✅ Check logs (`gateway.log`, `litellm.log`)
2. ✅ Run validation script
3. ✅ Search existing issues
4. ✅ Try solutions in this guide
5. ✅ Enable debug logging

### When Asking for Help

Include:

```bash
# System info
uname -a
python --version
pip list | grep litellm

# Configuration (sanitized)
# Remove API keys before sharing!
cat config.yaml

# Error logs
tail -50 gateway.log

# Steps to reproduce
```

### Resources

- **GitHub Issues**: https://github.com/roshankhatrishin317-eng/shin-/issues
- **LiteLLM Docs**: https://docs.litellm.ai/docs/troubleshooting
- **LiteLLM Discord**: https://discord.gg/wuPM9dRgDw
- **Email Support**: roshanshiloh31@gmail.com

---

## Preventive Measures

### Regular Maintenance

```bash
# Weekly tasks
- Review error logs
- Check disk space
- Verify backups
- Update dependencies

# Monthly tasks
- Rotate API keys
- Review usage patterns
- Update documentation
- Test disaster recovery
```

### Monitoring

Set up alerts for:
- Gateway downtime
- High error rates
- Unusual costs
- Performance degradation

See [Monitoring Guide](monitoring-guide.md)

---

[⬅ Back to Guides](README.md) | [Next: API Integration ➡](api-integration.md)


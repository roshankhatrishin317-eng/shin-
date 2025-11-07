# 🔐 Security Guide

Complete security guide for hardening and protecting your Shin LiteLLM Gateway.

## 📋 Table of Contents

1. [Security Overview](#security-overview)
2. [Authentication](#authentication)
3. [API Key Management](#api-key-management)
4. [Network Security](#network-security)
5. [HTTPS Setup](#https-setup)
6. [Rate Limiting](#rate-limiting)
7. [Access Control](#access-control)
8. [Security Best Practices](#security-best-practices)

---

## Security Overview

### Security Layers

Your gateway has multiple security layers:

```
┌─────────────────────────────────────┐
│   1. Network (Firewall, HTTPS)     │
├─────────────────────────────────────┤
│   2. Authentication (Master Key)    │
├─────────────────────────────────────┤
│   3. Authorization (Virtual Keys)   │
├─────────────────────────────────────┤
│   4. Rate Limiting                  │
├─────────────────────────────────────┤
│   5. Monitoring & Logging           │
└─────────────────────────────────────┘
```

### Security Checklist

- [ ] Strong master key (20+ characters)
- [ ] HTTPS enabled (production)
- [ ] Firewall configured
- [ ] Rate limiting enabled
- [ ] Access logs monitored
- [ ] Regular key rotation
- [ ] IP allowlist (if applicable)
- [ ] Environment variables secured
- [ ] Database encrypted
- [ ] Regular security updates

---

## Authentication

### Master Key

The master key is your gateway's main authentication mechanism.

#### Creating a Strong Master Key

```bash
# Generate secure random key
openssl rand -hex 32

# Or use Python
python -c "import secrets; print('sk-' + secrets.token_hex(32))"
```

Example strong key:
```
sk-a1b2c3d4e5f67890abcdef1234567890a1b2c3d4e5f67890abcdef12345678
```

#### Setting Master Key

In `.env`:
```bash
LITELLM_MASTER_KEY=sk-your-secure-key-here
```

In `config.yaml`:
```yaml
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

#### ⚠️ Master Key Security

**DO:**
- ✅ Use 20+ characters
- ✅ Include letters, numbers, special chars
- ✅ Store in `.env` file
- ✅ Never commit to git
- ✅ Rotate regularly (every 90 days)
- ✅ Use different keys for dev/prod

**DON'T:**
- ❌ Use simple passwords (`password123`)
- ❌ Hard-code in config files
- ❌ Share via email/chat
- ❌ Reuse across services
- ❌ Store in plain text

---

## API Key Management

### Virtual Keys

Create separate API keys for different users/applications.

#### Creating Virtual Keys

```bash
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "key_name": "mobile-app",
    "duration": "30d",
    "models": ["gpt-3.5-turbo", "shin-llama-70b"],
    "max_budget": 100.0
  }'
```

#### Response

```json
{
  "key": "sk-generated-key-abc123",
  "user_id": "user-123",
  "key_name": "mobile-app",
  "expires": "2025-12-07T00:00:00Z"
}
```

#### Using Virtual Keys

```python
import openai

# Use virtual key instead of master key
client = openai.OpenAI(
    api_key="sk-generated-key-abc123",
    base_url="http://localhost:4000"
)
```

#### Key Permissions

```bash
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{
    "models": ["gpt-3.5-turbo"],      # Only these models
    "max_budget": 50.0,                # Max $50
    "max_parallel_requests": 10,       # Max concurrent
    "tpm": 10000,                      # Tokens per minute
    "rpm": 100                         # Requests per minute
  }'
```

### List All Keys

```bash
curl http://localhost:4000/key/info \
  -H "Authorization: Bearer YOUR_MASTER_KEY"
```

### Revoke Key

```bash
curl -X DELETE http://localhost:4000/key/delete \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{"key": "sk-key-to-revoke"}'
```

---

## Network Security

### Firewall Configuration

#### UFW (Ubuntu/Debian)

```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow gateway (internal only)
sudo ufw allow from 10.0.0.0/8 to any port 4000

# Enable firewall
sudo ufw enable
```

#### iptables

```bash
# Allow localhost
iptables -A INPUT -i lo -j ACCEPT

# Allow gateway from internal network
iptables -A INPUT -p tcp -s 10.0.0.0/8 --dport 4000 -j ACCEPT

# Drop all other gateway connections
iptables -A INPUT -p tcp --dport 4000 -j DROP
```

### IP Allowlist

In `config.yaml`:

```yaml
general_settings:
  allowed_ips:
    - "127.0.0.1"           # Localhost
    - "10.0.0.0/8"          # Internal network
    - "192.168.1.100"       # Specific IP
```

### CORS Configuration

#### Development

```yaml
general_settings:
  cors_origin: "*"  # Allow all
```

#### Production

```yaml
general_settings:
  cors_origin:
    - "https://yourdomain.com"
    - "https://app.yourdomain.com"
```

---

## HTTPS Setup

### Why HTTPS?

- Encrypts all traffic
- Prevents man-in-the-middle attacks
- Required for production
- Protects API keys in transit

### Option 1: Nginx Reverse Proxy

#### Install Nginx

```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx
```

#### Configure Nginx

Create `/etc/nginx/sites-available/litellm`:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/litellm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Get SSL Certificate

```bash
sudo certbot --nginx -d api.yourdomain.com
```

Now your gateway is accessible at: `https://api.yourdomain.com`

### Option 2: Cloudflare Tunnel

Included in the repository:

```bash
./manage_tunnel.sh start
```

Provides:
- Free HTTPS
- DDoS protection
- No port forwarding needed
- Automatic SSL certificates

See [PUBLIC_URL.md](../PUBLIC_URL.md) for details.

---

## Rate Limiting

### Why Rate Limit?

- Prevent abuse
- Control costs
- Protect upstream APIs
- Fair usage across users

### Global Rate Limits

```yaml
litellm_settings:
  rpm: 1000              # Requests per minute
  tpm: 100000            # Tokens per minute
```

### Per-Model Rate Limits

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY
      rpm: 100           # This model: 100 req/min
      tpm: 50000         # This model: 50K tok/min
```

### Per-User Rate Limits

When creating virtual keys:

```bash
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{
    "user_id": "free-tier-user",
    "rpm": 10,
    "tpm": 1000,
    "max_budget": 5.0
  }'
```

### Rate Limit Response

When exceeded:

```json
{
  "error": {
    "message": "Rate limit exceeded",
    "type": "rate_limit_error",
    "code": 429
  }
}
```

---

## Access Control

### Role-Based Access

Create keys with different permissions:

#### Admin Key

```bash
# Full access to all models
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{
    "key_name": "admin",
    "models": ["*"]
  }'
```

#### Developer Key

```bash
# Access to development models only
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{
    "key_name": "developer",
    "models": ["gpt-3.5-turbo", "shin-llama-8b"],
    "max_budget": 10.0
  }'
```

#### Production Key

```bash
# Production models with high limits
curl http://localhost:4000/key/generate \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{
    "key_name": "production",
    "models": ["gpt-4", "shin-llama-405b"],
    "max_budget": 1000.0,
    "rpm": 500
  }'
```

### Model-Level Access

```yaml
# In config.yaml - coming soon
model_list:
  - model_name: internal-only-model
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY
      allowed_keys: ["admin-key-1", "internal-key-2"]
```

---

## Security Best Practices

### 1. Secrets Management

#### Use Environment Variables

✅ **Good:**
```yaml
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

❌ **Bad:**
```yaml
general_settings:
  master_key: "sk-hardcoded-key-123"
```

#### Secure .env File

```bash
# Set restrictive permissions
chmod 600 .env

# Never commit
echo ".env" >> .gitignore

# Use template for sharing
cp .env .env.template
# Remove actual values from template
```

### 2. Regular Updates

```bash
# Update LiteLLM
pip install --upgrade litellm[proxy]

# Update system packages
sudo apt update && sudo apt upgrade

# Monitor security advisories
# https://github.com/BerriAI/litellm/security/advisories
```

### 3. Logging and Monitoring

Enable comprehensive logging:

```yaml
general_settings:
  log_level: "INFO"
  json_logs: true
  
litellm_settings:
  set_verbose: true
```

Monitor for suspicious activity:

```bash
# Watch for failed authentication
tail -f gateway.log | grep "Authentication failed"

# Monitor rate limit hits
tail -f gateway.log | grep "rate_limit_exceeded"

# Track unusual models
tail -f gateway.log | grep "model not found"
```

### 4. Database Security

```yaml
# Encrypt database (if using PostgreSQL)
general_settings:
  database_url: "postgresql://user:pass@localhost/litellm?sslmode=require"
```

### 5. Input Validation

Gateway automatically validates:
- Model names
- Message format
- Parameter types
- Token limits

Additional validation in `config.yaml`:

```yaml
litellm_settings:
  drop_params: true      # Drop unknown parameters
  max_tokens: 4000       # Global max
```

### 6. Audit Trail

Enable request logging:

```yaml
general_settings:
  database_url: "sqlite:///litellm.db"
```

Query audit log:

```python
import sqlite3

conn = sqlite3.connect('litellm.db')
cursor = conn.cursor()

# Recent requests
cursor.execute("""
    SELECT timestamp, user, model, tokens
    FROM request_log
    ORDER BY timestamp DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(row)
```

---

## Security Incident Response

### If Master Key Is Compromised

1. **Immediately generate new key**
   ```bash
   openssl rand -hex 32
   ```

2. **Update .env**
   ```bash
   nano .env
   # Replace LITELLM_MASTER_KEY
   ```

3. **Restart gateway**
   ```bash
   python start_gateway.py
   ```

4. **Revoke all virtual keys**
   ```bash
   # Revoke through admin UI or API
   ```

5. **Audit logs**
   ```bash
   grep "suspicious-activity" gateway.log
   ```

### If Virtual Key Is Compromised

```bash
# Revoke specific key
curl -X DELETE http://localhost:4000/key/delete \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{"key": "compromised-key"}'
```

---

## Compliance

### GDPR Compliance

- Store minimal user data
- Enable request anonymization
- Provide data export
- Implement data deletion

```yaml
general_settings:
  anonymize_logs: true
  data_retention_days: 30
```

### SOC 2 Compliance

- Enable audit logging
- Implement access controls
- Regular security reviews
- Encrypted communications

---

## Security Checklist for Production

```
Pre-Deployment:
[ ] Strong master key generated
[ ] All secrets in environment variables
[ ] .env file not committed to git
[ ] HTTPS configured (Nginx/Cloudflare)
[ ] Firewall rules configured
[ ] IP allowlist configured (if needed)
[ ] Rate limiting enabled
[ ] Virtual keys created for users
[ ] Logging enabled
[ ] Monitoring set up

Post-Deployment:
[ ] Test authentication
[ ] Verify HTTPS works
[ ] Test rate limits
[ ] Monitor logs for errors
[ ] Set up alerts
[ ] Document key rotation schedule
[ ] Create incident response plan
```

---

## Next Steps

- **Monitor Gateway**: [Monitoring Guide](monitoring-guide.md)
- **Deploy to Production**: [Production Deployment](production-deployment.md)
- **Troubleshoot Issues**: [Troubleshooting Guide](troubleshooting.md)

---

[⬅ Back to Guides](README.md) | [Next: Monitoring ➡](monitoring-guide.md)


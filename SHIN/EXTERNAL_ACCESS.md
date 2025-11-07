# 🌐 External Access Guide for LiteLLM Gateway

Your LiteLLM Gateway is now accessible from other computers!

## 📍 Access URLs

### Internal Network Access (Same Network)
```
http://10.192.12.52:4000
```
Use this URL when accessing from computers on the same local network.

### External Access (Internet)
```
http://98.83.113.118:4000
```
Use this URL when accessing from anywhere on the internet.

### Localhost (This Computer Only)
```
http://localhost:4000
```
Use this URL only from this computer.

---

## 🔑 Authentication

All requests require your Master Key in the Authorization header:

```bash
Authorization: Bearer YOUR_MASTER_KEY
```

Find your master key in `.env` file:
```bash
grep LITELLM_MASTER_KEY .env
```

---

## 🚀 Usage Examples from Other Computers

### 1. Using cURL

```bash
# Test connection
curl http://98.83.113.118:4000/health

# List available models
curl http://98.83.113.118:4000/v1/models \
  -H "Authorization: Bearer YOUR_MASTER_KEY"

# Make a completion request
curl http://98.83.113.118:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_MASTER_KEY" \
  -d '{
    "model": "nvidia-llama-3-1-405b",
    "messages": [
      {"role": "user", "content": "Hello from another computer!"}
    ]
  }'
```

### 2. Using Python (OpenAI SDK)

```python
from openai import OpenAI

# Initialize client with your gateway URL
client = OpenAI(
    api_key="YOUR_MASTER_KEY",  # Your LiteLLM master key
    base_url="http://98.83.113.118:4000/v1"  # Your gateway URL
)

# Use any configured model
response = client.chat.completions.create(
    model="nvidia-llama-3-1-405b",
    messages=[
        {"role": "user", "content": "Hello from Python!"}
    ]
)

print(response.choices[0].message.content)
```

### 3. Using Node.js (OpenAI SDK)

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'YOUR_MASTER_KEY',  // Your LiteLLM master key
  baseURL: 'http://98.83.113.118:4000/v1',  // Your gateway URL
});

async function main() {
  const completion = await client.chat.completions.create({
    model: 'nvidia-llama-3-1-405b',
    messages: [
      { role: 'user', content: 'Hello from Node.js!' }
    ],
  });

  console.log(completion.choices[0].message.content);
}

main();
```

### 4. Configure in AI Applications

Many AI applications support custom OpenAI-compatible endpoints:

- **Base URL:** `http://98.83.113.118:4000/v1`
- **API Key:** Your LiteLLM Master Key
- **Model:** Any of your 21 configured models

Examples:
- **Continue.dev:** Set custom endpoint in config
- **Open WebUI:** Add as OpenAI endpoint
- **LibreChat:** Configure custom endpoint
- **Cursor/Copilot alternatives:** Use custom base URL

---

## 🔒 Security Recommendations

### ⚠️ IMPORTANT Security Notes

1. **Keep Your Master Key Secret**
   - Never commit it to git
   - Don't share it publicly
   - Rotate it periodically

2. **Firewall Configuration** (Recommended)
   ```bash
   # Allow only specific IPs (recommended for production)
   sudo ufw allow from TRUSTED_IP to any port 4000
   
   # Or allow from specific subnet
   sudo ufw allow from 192.168.1.0/24 to any port 4000
   ```

3. **HTTPS/TLS** (Recommended for production)
   - Use a reverse proxy (nginx/caddy) with SSL
   - Get free SSL certificate from Let's Encrypt
   - See "Production Setup" section below

4. **Rate Limiting**
   - Consider adding rate limiting in production
   - Monitor usage and costs

---

## 🛡️ Production Setup with HTTPS (Recommended)

For production use, set up a reverse proxy with SSL:

### Option 1: Using Caddy (Easiest)

1. Install Caddy:
```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

2. Create Caddyfile:
```bash
cat > Caddyfile << 'EOF'
your-domain.com {
    reverse_proxy localhost:4000
}
EOF
```

3. Run Caddy:
```bash
sudo caddy run --config Caddyfile
```

Now access via: `https://your-domain.com`

### Option 2: Using Nginx

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:4000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 Monitoring Access

### View Gateway Logs
```bash
# Real-time logs
tail -f gateway.log

# View specific request logs
grep "POST /v1/chat/completions" gateway.log

# Check for errors
grep "ERROR" gateway.log
```

### Check Active Connections
```bash
# See who's connected
netstat -an | grep :4000

# Or using ss
ss -tn | grep :4000
```

---

## 🔧 Troubleshooting

### Can't Connect from Other Computer?

1. **Check if gateway is running:**
```bash
curl http://localhost:4000/health
```

2. **Check if port 4000 is accessible:**
```bash
# On the gateway server
sudo netstat -tlnp | grep 4000
```

3. **Check firewall:**
```bash
# Check if port is blocked
sudo ufw status
sudo iptables -L -n | grep 4000
```

4. **Open port if needed:**
```bash
# Open port 4000
sudo ufw allow 4000/tcp
```

5. **Test from another computer:**
```bash
# Replace with your IP
curl http://98.83.113.118:4000/health
```

### Connection Timeout?

- Ensure your cloud provider's security group allows port 4000
- Check if your ISP blocks the port
- Verify the IP address is correct

### 401 Unauthorized Error?

- Check your master key is correct
- Ensure Authorization header is properly formatted
- Verify the key hasn't been changed

---

## 📱 Quick Connection Test

Run this from another computer to test connectivity:

```bash
# Replace YOUR_MASTER_KEY with your actual key
export LITELLM_KEY="YOUR_MASTER_KEY"

# Test health endpoint (no auth needed)
curl http://98.83.113.118:4000/health

# Test with authentication
curl http://98.83.113.118:4000/v1/models \
  -H "Authorization: Bearer $LITELLM_KEY"
```

If you see the model list, you're all set! 🎉

---

## 🌟 Next Steps

1. ✅ Save your access URLs and master key securely
2. ✅ Test connection from another computer
3. ✅ Configure your AI applications to use the gateway
4. ✅ Set up monitoring and logging
5. ✅ Consider HTTPS for production use
6. ✅ Configure firewall rules as needed

---

## 📞 Support

For more information:
- LiteLLM Docs: https://docs.litellm.ai/
- Gateway Config: `config.yaml`
- Environment Variables: `.env`
- Master Key Info: `MASTER_KEY_INFO.md`


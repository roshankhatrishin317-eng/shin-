# 🌐 Public Access URL - LiteLLM Gateway

Your LiteLLM Gateway is now accessible from anywhere in the world!

## ✅ Working Public URL

```
https://stands-birth-featured-investigate.trycloudflare.com
```

This URL works from **ANY computer, anywhere** - no network restrictions!

---

## 🚀 Quick Usage

### Base URL for OpenAI-Compatible Apps:
```
https://stands-birth-featured-investigate.trycloudflare.com/v1
```

### Master Key:
```
sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN
```

---

## 🧪 Test from Any Computer

### 1. Test Health (No Auth):
```bash
curl https://stands-birth-featured-investigate.trycloudflare.com/health
```

### 2. List Models:
```bash
curl https://stands-birth-featured-investigate.trycloudflare.com/v1/models \
  -H "Authorization: Bearer sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN"
```

### 3. Make a Request:
```bash
curl https://stands-birth-featured-investigate.trycloudflare.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN" \
  -d '{
    "model": "claude-3-5-sonnet",
    "messages": [{"role": "user", "content": "Hello from the internet!"}]
  }'
```

---

## 💻 Use in Your Applications

### Python (OpenAI SDK):
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN",
    base_url="https://stands-birth-featured-investigate.trycloudflare.com/v1"
)

response = client.chat.completions.create(
    model="nvidia-llama-3-1-405b",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

### Node.js:
```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN',
  baseURL: 'https://stands-birth-featured-investigate.trycloudflare.com/v1',
});

const response = await client.chat.completions.create({
  model: 'nvidia-llama-3-1-405b',
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(response.choices[0].message.content);
```

### cURL:
```bash
curl https://stands-birth-featured-investigate.trycloudflare.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN" \
  -d '{
    "model": "nvidia-llama-3-1-405b",
    "messages": [{"role": "user", "content": "Write a hello world program"}],
    "temperature": 0.7
  }'
```

---

## 📋 Available Models (21 Total)

### Anthropic (2):
- `claude-3-5-sonnet`
- `claude-3-opus`

### NVIDIA NIM (9):
- `nvidia-llama-3-1-405b` (largest)
- `nvidia-llama-3-1-70b`
- `nvidia-llama-3-1-8b` (fastest)
- `nvidia-llama-3-1-nemotron-70b`
- `nvidia-mistral-large-2`
- `nvidia-mistral-nemo-12b`
- `moonshotai-kimi-k2`
- `qwen-coder-480b` (best for coding)
- `minimax-m2`

### Custom Providers (10):
- `opencode-big-pickle`
- `glm-4.6`
- `iflow-qwen3-coder-plus`
- `iflow-qwen3-max`
- `iflow-qwen3-coder`
- `iflow-kimi-k2-0905`
- `iflow-glm-4.6`
- `iflow-deepseek-v3.2`
- `iflow-qwen3-235b-thinking`
- `minimax1-claude`

---

## 🔧 Configure in Popular Apps

### Continue.dev (VS Code):
```json
{
  "models": [{
    "title": "LiteLLM Gateway",
    "provider": "openai",
    "model": "nvidia-llama-3-1-405b",
    "apiKey": "sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN",
    "apiBase": "https://stands-birth-featured-investigate.trycloudflare.com/v1"
  }]
}
```

### Open WebUI:
- **Type:** OpenAI API
- **Base URL:** `https://stands-birth-featured-investigate.trycloudflare.com/v1`
- **API Key:** `sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN`

### LibreChat:
Add to `.env`:
```bash
OPENAI_API_KEY=sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN
OPENAI_REVERSE_PROXY=https://stands-birth-featured-investigate.trycloudflare.com/v1
```

---

## 🛠️ How This Works

This uses **Cloudflare Tunnel** to securely expose your local LiteLLM Gateway to the internet:

```
Your Computer → LiteLLM Gateway (localhost:4000)
        ↓
Cloudflare Tunnel (cloudflared)
        ↓
Public HTTPS URL (stands-birth-featured-investigate.trycloudflare.com)
        ↓
Anyone on the Internet ✅
```

**Benefits:**
- ✅ No firewall configuration needed
- ✅ Free HTTPS included
- ✅ Works from anywhere
- ✅ No port forwarding required
- ✅ Secure by default

---

## 📊 Monitor & Manage

### Check Gateway Status:
```bash
# View gateway logs
tail -f gateway.log

# View tunnel logs
tail -f tunnel.log

# Check if tunnel is running
ps aux | grep cloudflared
```

### Restart Services:
```bash
# Restart gateway
kill $(cat gateway.pid)
python start_gateway.py > gateway.log 2>&1 &

# Restart tunnel
kill $(cat tunnel.pid)
./cloudflared tunnel --url http://localhost:4000 > tunnel.log 2>&1 &
```

### Stop Services:
```bash
# Stop gateway
kill $(cat gateway.pid)

# Stop tunnel
kill $(cat tunnel.pid)
```

---

## ⚠️ Important Notes

1. **Cloudflare Free Tunnel URL Changes:** 
   - The free tunnel URL changes each time you restart it
   - For a permanent URL, use Cloudflare Tunnel with an account (optional)

2. **Keep Services Running:**
   - Both gateway and tunnel must be running for external access
   - Gateway PID: `gateway.pid`
   - Tunnel PID: `tunnel.pid`

3. **Security:**
   - Your master key authenticates all requests
   - HTTPS is automatic via Cloudflare
   - Keep your master key secret

4. **Rate Limits:**
   - Cloudflare free tunnel has generous limits
   - Your actual limits depend on your API providers

---

## 🔄 Getting a New URL

If you need a new public URL:

```bash
# Stop old tunnel
kill $(cat tunnel.pid)

# Start new tunnel (will get new URL)
./cloudflared tunnel --url http://localhost:4000 > tunnel.log 2>&1 &
echo $! > tunnel.pid

# Wait a few seconds, then get the new URL
sleep 5
grep -oP "https://[a-zA-Z0-9-]+\.trycloudflare\.com" tunnel.log | head -1
```

---

## 🎉 You're All Set!

Your LiteLLM Gateway is now accessible from anywhere in the world!

**Share this with your team:**
- Public URL: `https://stands-birth-featured-investigate.trycloudflare.com/v1`
- Master Key: `sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN`
- 21 AI models ready to use!

Test it now from any device: https://stands-birth-featured-investigate.trycloudflare.com/health


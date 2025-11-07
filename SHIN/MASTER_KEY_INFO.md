# 🔐 Master Key Information

## Your Gateway Master Key

Your LiteLLM Gateway is now secured with a cryptographically secure random master key.

### 🔑 Master Key

```
sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN
```

**⚠️ IMPORTANT: Keep this key secure!**

## 🚀 How to Use

### With Python (OpenAI SDK)

```python
import openai

client = openai.OpenAI(
    api_key="sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="nvidia-llama-3-1-405b",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### With cURL

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN" \
  -d '{
    "model": "nvidia-llama-3-1-405b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### With Environment Variable

```bash
export LITELLM_MASTER_KEY="sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN"
```

## 📋 Key Features

- ✅ **48 random characters** - Highly secure
- ✅ **Cryptographically secure** - Generated using `secrets` module
- ✅ **OpenAI-compatible format** - Starts with `sk-`
- ✅ **Production ready** - Suitable for production environments

## 🔒 Security Best Practices

1. **Never commit this key to version control**
   - It's already in `.env` which is in `.gitignore`

2. **Store securely**
   - Use environment variables in production
   - Use secret management services (AWS Secrets Manager, etc.)

3. **Rotate regularly**
   - Change the key periodically
   - Generate new key: `python3 -c "import secrets; print('sk-' + ''.join(secrets.token_urlsafe(36)))"`

4. **Restrict access**
   - Only share with authorized users/services
   - Use different keys for different environments (dev/staging/prod)

5. **Monitor usage**
   - Check `litellm.db` for unusual activity
   - Enable logging in production

## 🔄 Generate New Key Anytime

To generate a new random master key:

```bash
python3 << 'EOF'
import secrets
import string
alphabet = string.ascii_letters + string.digits
random_key = ''.join(secrets.choice(alphabet) for _ in range(48))
print(f"sk-{random_key}")
EOF
```

Then update in `.env`:
```bash
LITELLM_MASTER_KEY=sk-YOUR-NEW-KEY-HERE
```

## 📍 Where It's Used

Your master key is configured in:
- ✅ `.env` file (active)
- ✅ `config.yaml` (reads from environment)
- ✅ All test scripts use it automatically

## 🧪 Test Your Key

```bash
# Start gateway
python start_gateway.py

# In another terminal, test with your key
python test_all_providers.py
```

## ⚡ Quick Reference

**Your Gateway URL:** `http://localhost:4000`
**Your Master Key:** `sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN`

**Use in requests:**
```
Authorization: Bearer sk-wkSsJJHrYWxg0dIEyid7jL5gFfejusBlVESnILg4BFD8HqDN
```

---

**🔐 Keep this key secure and never share it publicly!**


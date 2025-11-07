# 🔌 API Integration Guide

Complete guide for integrating Shin LiteLLM Gateway into your applications.

## 📋 Table of Contents

1. [OpenAI SDK Integration](#openai-sdk-integration)
2. [cURL Examples](#curl-examples)
3. [Python Integration](#python-integration)
4. [JavaScript/Node.js](#javascriptnodejs)
5. [Framework Integration](#framework-integration)
6. [Streaming Responses](#streaming-responses)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)

---

## OpenAI SDK Integration

The gateway is **100% OpenAI-compatible**, meaning you can use it as a drop-in replacement for OpenAI's API.

### Python (OpenAI SDK)

```python
import openai

# Configure client to use your gateway
client = openai.OpenAI(
    api_key="your-litellm-master-key",  # Your gateway master key
    base_url="http://localhost:4000"     # Your gateway URL
)

# Use exactly like OpenAI
response = client.chat.completions.create(
    model="shin-llama-3-1-70b",  # Any model in your config
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message.content)
```

### JavaScript/TypeScript (OpenAI SDK)

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'your-litellm-master-key',
  baseURL: 'http://localhost:4000'
});

const response = await client.chat.completions.create({
  model: 'shin-llama-3-1-70b',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'What is the capital of France?' }
  ]
});

console.log(response.choices[0].message.content);
```

---

## cURL Examples

### Basic Chat Completion

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-master-key" \
  -d '{
    "model": "shin-llama-3-1-70b",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### With System Message

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-master-key" \
  -d '{
    "model": "shin-llama-3-1-70b",
    "messages": [
      {"role": "system", "content": "You are a helpful coding assistant."},
      {"role": "user", "content": "Write a Python hello world"}
    ]
  }'
```

### With Parameters

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-master-key" \
  -d '{
    "model": "shin-llama-3-1-70b",
    "messages": [{"role": "user", "content": "Tell me a joke"}],
    "temperature": 0.7,
    "max_tokens": 150,
    "top_p": 0.9
  }'
```

### Streaming Response

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-master-key" \
  -d '{
    "model": "shin-llama-3-1-70b",
    "messages": [{"role": "user", "content": "Count to 10"}],
    "stream": true
  }'
```

---

## Python Integration

### Basic Usage

```python
import openai
import os

# Initialize client
client = openai.OpenAI(
    api_key=os.getenv("LITELLM_MASTER_KEY"),
    base_url=os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
)

def chat(message, model="shin-llama-3-1-70b"):
    """Send a chat message and get response"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content

# Use it
result = chat("What is Python?")
print(result)
```

### Multi-Turn Conversation

```python
class ChatSession:
    def __init__(self, model="shin-llama-3-1-70b"):
        self.client = openai.OpenAI(
            api_key="your-master-key",
            base_url="http://localhost:4000"
        )
        self.model = model
        self.messages = []
    
    def send(self, message):
        # Add user message
        self.messages.append({"role": "user", "content": message})
        
        # Get response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        
        # Add assistant response
        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message

# Use it
chat = ChatSession()
print(chat.send("Hi, I'm learning Python"))
print(chat.send("Can you explain functions?"))
print(chat.send("Give me an example"))
```

### Async Usage

```python
import openai
import asyncio

client = openai.AsyncOpenAI(
    api_key="your-master-key",
    base_url="http://localhost:4000"
)

async def chat_async(message):
    response = await client.chat.completions.create(
        model="shin-llama-3-1-70b",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content

# Use it
async def main():
    tasks = [
        chat_async("What is AI?"),
        chat_async("What is ML?"),
        chat_async("What is DL?")
    ]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

asyncio.run(main())
```

### With Error Handling

```python
import openai
from openai import OpenAIError

def safe_chat(message, model="shin-llama-3-1-70b", max_retries=3):
    client = openai.OpenAI(
        api_key="your-master-key",
        base_url="http://localhost:4000"
    )
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        
        except openai.RateLimitError:
            print(f"Rate limit hit, retrying... ({attempt + 1}/{max_retries})")
            time.sleep(2 ** attempt)  # Exponential backoff
        
        except openai.APIError as e:
            print(f"API error: {e}")
            if attempt == max_retries - 1:
                raise
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    raise Exception("Max retries exceeded")

# Use it
result = safe_chat("Tell me about AI")
print(result)
```

---

## JavaScript/Node.js

### Basic Usage

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.LITELLM_MASTER_KEY,
  baseURL: process.env.LITELLM_BASE_URL || 'http://localhost:4000'
});

async function chat(message, model = 'shin-llama-3-1-70b') {
  const response = await client.chat.completions.create({
    model: model,
    messages: [{ role: 'user', content: message }]
  });
  
  return response.choices[0].message.content;
}

// Use it
const result = await chat('What is JavaScript?');
console.log(result);
```

### Multi-Turn Conversation

```javascript
class ChatSession {
  constructor(model = 'shin-llama-3-1-70b') {
    this.client = new OpenAI({
      apiKey: process.env.LITELLM_MASTER_KEY,
      baseURL: 'http://localhost:4000'
    });
    this.model = model;
    this.messages = [];
  }
  
  async send(message) {
    // Add user message
    this.messages.push({ role: 'user', content: message });
    
    // Get response
    const response = await this.client.chat.completions.create({
      model: this.model,
      messages: this.messages
    });
    
    // Add assistant response
    const assistantMessage = response.choices[0].message.content;
    this.messages.push({ role: 'assistant', content: assistantMessage });
    
    return assistantMessage;
  }
}

// Use it
const chat = new ChatSession();
console.log(await chat.send('Hi!'));
console.log(await chat.send('Tell me about Node.js'));
```

### Express.js Integration

```javascript
import express from 'express';
import OpenAI from 'openai';

const app = express();
app.use(express.json());

const client = new OpenAI({
  apiKey: process.env.LITELLM_MASTER_KEY,
  baseURL: 'http://localhost:4000'
});

app.post('/api/chat', async (req, res) => {
  try {
    const { message, model = 'shin-llama-3-1-70b' } = req.body;
    
    const response = await client.chat.completions.create({
      model: model,
      messages: [{ role: 'user', content: message }]
    });
    
    res.json({
      success: true,
      response: response.choices[0].message.content
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
```

---

## Framework Integration

### LangChain (Python)

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Initialize with your gateway
llm = ChatOpenAI(
    model_name="shin-llama-3-1-70b",
    openai_api_key="your-master-key",
    openai_api_base="http://localhost:4000/v1"
)

# Use it
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is LangChain?")
]

response = llm.invoke(messages)
print(response.content)
```

### LlamaIndex (Python)

```python
from llama_index.llms.openai_like import OpenAILike

# Initialize with your gateway
llm = OpenAILike(
    model="shin-llama-3-1-70b",
    api_key="your-master-key",
    api_base="http://localhost:4000/v1"
)

# Use it
response = llm.complete("What is LlamaIndex?")
print(response.text)
```

### Vercel AI SDK (JavaScript)

```javascript
import { Configuration, OpenAIApi } from 'openai-edge';
import { OpenAIStream, StreamingTextResponse } from 'ai';

const config = new Configuration({
  apiKey: process.env.LITELLM_MASTER_KEY,
  basePath: 'http://localhost:4000/v1'
});

const openai = new OpenAIApi(config);

export async function POST(req) {
  const { messages } = await req.json();
  
  const response = await openai.createChatCompletion({
    model: 'shin-llama-3-1-70b',
    stream: true,
    messages
  });
  
  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}
```

---

## Streaming Responses

### Python Streaming

```python
import openai

client = openai.OpenAI(
    api_key="your-master-key",
    base_url="http://localhost:4000"
)

def stream_chat(message):
    stream = client.chat.completions.create(
        model="shin-llama-3-1-70b",
        messages=[{"role": "user", "content": message}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()  # New line at end

# Use it
stream_chat("Tell me a long story")
```

### JavaScript Streaming

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'your-master-key',
  baseURL: 'http://localhost:4000'
});

async function streamChat(message) {
  const stream = await client.chat.completions.create({
    model: 'shin-llama-3-1-70b',
    messages: [{ role: 'user', content: message }],
    stream: true
  });
  
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    process.stdout.write(content);
  }
  console.log(); // New line at end
}

// Use it
await streamChat('Tell me a long story');
```

### React Streaming Component

```jsx
import { useState } from 'react';
import OpenAI from 'openai';

function ChatComponent() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  
  const client = new OpenAI({
    apiKey: 'your-master-key',
    baseURL: 'http://localhost:4000',
    dangerouslyAllowBrowser: true // Only for demo
  });
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse('');
    
    const stream = await client.chat.completions.create({
      model: 'shin-llama-3-1-70b',
      messages: [{ role: 'user', content: message }],
      stream: true
    });
    
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      setResponse(prev => prev + content);
    }
    
    setLoading(false);
  };
  
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
      <div>{response}</div>
    </div>
  );
}
```

---

## Error Handling

### Comprehensive Error Handling (Python)

```python
import openai
from openai import (
    APIError,
    RateLimitError,
    AuthenticationError,
    APIConnectionError
)
import time

def robust_chat(message, model="shin-llama-3-1-70b"):
    client = openai.OpenAI(
        api_key="your-master-key",
        base_url="http://localhost:4000"
    )
    
    max_retries = 3
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}],
                timeout=60.0
            )
            return response.choices[0].message.content
        
        except AuthenticationError as e:
            print(f"Authentication failed: {e}")
            return None  # Don't retry auth errors
        
        except RateLimitError as e:
            delay = base_delay * (2 ** attempt)
            print(f"Rate limit hit. Waiting {delay}s...")
            time.sleep(delay)
        
        except APIConnectionError as e:
            print(f"Connection error: {e}")
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2 ** attempt))
        
        except APIError as e:
            print(f"API error: {e}")
            if e.status_code >= 500:  # Server error, retry
                if attempt < max_retries - 1:
                    time.sleep(base_delay * (2 ** attempt))
            else:  # Client error, don't retry
                return None
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    print("Max retries exceeded")
    return None
```

### Error Handling (JavaScript)

```javascript
async function robustChat(message, model = 'shin-llama-3-1-70b') {
  const client = new OpenAI({
    apiKey: 'your-master-key',
    baseURL: 'http://localhost:4000'
  });
  
  const maxRetries = 3;
  let baseDelay = 1000; // ms
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await client.chat.completions.create({
        model: model,
        messages: [{ role: 'user', content: message }],
        timeout: 60000
      });
      
      return response.choices[0].message.content;
    } catch (error) {
      if (error.status === 401) {
        console.error('Authentication failed');
        return null;
      }
      
      if (error.status === 429) {
        const delay = baseDelay * Math.pow(2, attempt);
        console.log(`Rate limit hit. Waiting ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      
      if (error.status >= 500) {
        if (attempt < maxRetries - 1) {
          const delay = baseDelay * Math.pow(2, attempt);
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }
      }
      
      console.error('Error:', error.message);
      return null;
    }
  }
  
  console.error('Max retries exceeded');
  return null;
}
```

---

## Best Practices

### 1. API Key Management

```python
# Good: Use environment variables
import os
api_key = os.getenv("LITELLM_MASTER_KEY")

# Bad: Hardcode keys
api_key = "sk-1234567890"  # Never do this!
```

### 2. Timeout Configuration

```python
# Set appropriate timeouts
response = client.chat.completions.create(
    model="shin-llama-3-1-70b",
    messages=[{"role": "user", "content": message}],
    timeout=60.0  # 60 seconds
)
```

### 3. Model Selection

```python
# Choose appropriate model for task
def get_model_for_task(task_type):
    if task_type == "simple":
        return "shin-llama-3-1-8b"  # Fast, cheap
    elif task_type == "complex":
        return "shin-llama-3-1-405b"  # Powerful
    elif task_type == "code":
        return "otsu-qwen3-coder-plus"  # Specialized
    else:
        return "shin-llama-3-1-70b"  # Balanced
```

### 4. Request Batching

```python
import asyncio

async def batch_requests(messages):
    client = openai.AsyncOpenAI(
        api_key="your-master-key",
        base_url="http://localhost:4000"
    )
    
    tasks = [
        client.chat.completions.create(
            model="shin-llama-3-1-70b",
            messages=[{"role": "user", "content": msg}]
        )
        for msg in messages
    ]
    
    responses = await asyncio.gather(*tasks)
    return [r.choices[0].message.content for r in responses]

# Use it
messages = ["What is AI?", "What is ML?", "What is DL?"]
results = asyncio.run(batch_requests(messages))
```

### 5. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chat_with_logging(message):
    logger.info(f"Sending message: {message[:50]}...")
    
    try:
        response = client.chat.completions.create(
            model="shin-llama-3-1-70b",
            messages=[{"role": "user", "content": message}]
        )
        result = response.choices[0].message.content
        logger.info(f"Received response: {len(result)} characters")
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

---

## Next Steps

- **Explore Examples**: Check [/examples](../examples/) folder
- **Monitor Usage**: [Monitoring Guide](monitoring-guide.md)
- **Handle Errors**: [Troubleshooting Guide](troubleshooting.md)
- **Deploy**: [Production Deployment](production-deployment.md)

---

[⬅ Back to Guides](README.md) | [Main README](../README.md)


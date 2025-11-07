#!/usr/bin/env python3
"""
OpenAI-Compatible API Demo for LiteLLM Gateway

This demonstrates how to use your LiteLLM Gateway with OpenAI-compatible clients.
ANY tool that works with OpenAI's API will work with LiteLLM Gateway!
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 70)
print("🔄 OpenAI-Compatible API Demo - LiteLLM Gateway")
print("=" * 70)
print()

# Gateway configuration
GATEWAY_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
GATEWAY_KEY = os.getenv("LITELLM_MASTER_KEY", "your-master-key")

print(f"Gateway URL: {GATEWAY_URL}")
print(f"Gateway Key: {'*' * 10}{GATEWAY_KEY[-4:] if len(GATEWAY_KEY) > 4 else '****'}")
print()

# Example 1: Using OpenAI SDK (Python)
print("=" * 70)
print("Example 1: OpenAI Python SDK (Recommended)")
print("=" * 70)
print()

try:
    import openai
    
    # This is the ONLY thing you need to change to use LiteLLM Gateway
    # instead of OpenAI directly!
    client = openai.OpenAI(
        api_key=GATEWAY_KEY,      # Use your gateway key instead of OpenAI key
        base_url=GATEWAY_URL       # Point to your gateway instead of OpenAI
    )
    
    print("✅ OpenAI SDK configured to use LiteLLM Gateway")
    print()
    
    # Now you can use ANY model configured in your gateway!
    print("Testing different models through OpenAI-compatible interface:")
    print()
    
    # Test 1: OpenAI Model
    print("1️⃣ Testing OpenAI Model (gpt-3.5-turbo)...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'OpenAI via Gateway works!'"}],
            max_tokens=20
        )
        print(f"   ✅ Response: {response.choices[0].message.content}")
        print(f"   📊 Tokens: {response.usage.total_tokens}")
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
    print()
    
    # Test 2: Anthropic Model (through OpenAI-compatible interface!)
    print("2️⃣ Testing Anthropic Model (claude-3-5-sonnet) via OpenAI SDK...")
    try:
        response = client.chat.completions.create(
            model="claude-3-5-sonnet",  # Anthropic model!
            messages=[{"role": "user", "content": "Say 'Claude via OpenAI SDK works!'"}],
            max_tokens=20
        )
        print(f"   ✅ Response: {response.choices[0].message.content}")
        print(f"   📊 Model: {response.model}")
    except Exception as e:
        print(f"   ⚠️ Error: {e} (Make sure ANTHROPIC_API_KEY is set)")
    print()
    
    # Test 3: Streaming
    print("3️⃣ Testing Streaming (OpenAI-compatible)...")
    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Count from 1 to 3"}],
            stream=True,
            max_tokens=30
        )
        print("   Streaming response: ", end="", flush=True)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print(" ✅")
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
    print()

except ImportError:
    print("❌ OpenAI SDK not installed. Install with: pip install openai")
    print()

# Example 2: Show HTTP Request Format
print("=" * 70)
print("Example 2: Raw HTTP Request (OpenAI-Compatible)")
print("=" * 70)
print()
print("You can use standard HTTP requests just like OpenAI's API:")
print()
print(f"""
curl {GATEWAY_URL}/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer {GATEWAY_KEY}" \\
  -d '{{
    "model": "gpt-3.5-turbo",
    "messages": [
      {{"role": "user", "content": "Hello!"}}
    ]
  }}'
""")

# Example 3: Show how to use with other tools
print("=" * 70)
print("Example 3: Using with LangChain")
print("=" * 70)
print()
print("LangChain example (install with: pip install langchain):")
print()
print(f"""
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    openai_api_base="{GATEWAY_URL}",
    openai_api_key="{GATEWAY_KEY}",
    model_name="gpt-3.5-turbo"
)

response = llm.invoke("Hello!")
print(response.content)
""")
print()

# Example 4: List models
print("=" * 70)
print("Example 4: List Available Models (OpenAI-Compatible)")
print("=" * 70)
print()

try:
    import openai
    client = openai.OpenAI(api_key=GATEWAY_KEY, base_url=GATEWAY_URL)
    
    models = client.models.list()
    print("Available models through OpenAI-compatible interface:")
    for model in models.data:
        print(f"  • {model.id}")
except Exception as e:
    print(f"⚠️ Could not list models: {e}")
print()

# Summary
print("=" * 70)
print("📋 Summary: OpenAI-Compatible Features")
print("=" * 70)
print()
print("✅ Your LiteLLM Gateway provides:")
print("   • Same API endpoints as OpenAI (/v1/chat/completions, etc.)")
print("   • Same request/response format")
print("   • Works with OpenAI SDK (Python, Node.js, etc.)")
print("   • Works with any OpenAI-compatible tool")
print("   • But can route to ANY provider (OpenAI, Anthropic, Azure, etc.)")
print()
print("🎯 Benefits:")
print("   • Write code once, use any LLM provider")
print("   • Easy migration between providers")
print("   • Load balancing across providers")
print("   • Single authentication point")
print("   • Cost tracking across all providers")
print()
print("📚 More info:")
print("   • Official Docs: https://docs.litellm.ai/docs/")
print("   • Run examples: python examples/basic_usage.py")
print()


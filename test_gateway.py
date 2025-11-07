#!/usr/bin/env python3
"""
Test script for LiteLLM Gateway
Tests the proxy server by making a simple API call
"""

import os
import sys
from dotenv import load_dotenv

try:
    import openai
except ImportError:
    print("Installing openai package...")
    os.system("pip install openai")
    import openai

def test_gateway():
    """Test the LiteLLM gateway with a simple completion request"""
    
    load_dotenv()
    
    # Configuration
    base_url = os.getenv('LITELLM_BASE_URL', 'http://localhost:4000')
    api_key = os.getenv('LITELLM_MASTER_KEY', 'sk-1234')
    
    print("🧪 Testing LiteLLM Gateway")
    print(f"📍 Base URL: {base_url}")
    print(f"🔑 API Key: {'*' * 10}{api_key[-4:] if len(api_key) > 4 else '****'}")
    print()
    
    # Initialize OpenAI client pointing to LiteLLM
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    try:
        print("📤 Sending test request...")
        print("   Model: gpt-3.5-turbo")
        print("   Message: 'Hello! Test LiteLLM Gateway'")
        print()
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'LiteLLM Gateway is working!' in a creative way. Keep it brief."}
            ],
            max_tokens=50
        )
        
        print("✅ Success! Gateway is working correctly.")
        print()
        print("📥 Response:")
        print("-" * 50)
        print(response.choices[0].message.content)
        print("-" * 50)
        print()
        print(f"📊 Model used: {response.model}")
        print(f"🎫 Tokens used: {response.usage.total_tokens}")
        
        return True
        
    except openai.APIConnectionError as e:
        print(f"❌ Connection Error: Could not connect to {base_url}")
        print(f"   Make sure the gateway is running!")
        print(f"   Error: {e}")
        return False
        
    except openai.AuthenticationError as e:
        print(f"❌ Authentication Error: Invalid API key")
        print(f"   Check your LITELLM_MASTER_KEY in .env")
        print(f"   Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}")
        print(f"   {e}")
        return False

if __name__ == '__main__':
    success = test_gateway()
    sys.exit(0 if success else 1)


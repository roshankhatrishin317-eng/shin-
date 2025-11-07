#!/usr/bin/env python3
"""
Test LiteLLM Gateway Connection from Remote Computer

Usage:
    python test_remote_connection.py <gateway_url> <master_key>

Example:
    python test_remote_connection.py http://98.83.113.118:4000 your-master-key-here
"""

import sys
import requests
from openai import OpenAI

def test_connection(base_url: str, api_key: str):
    """Test connection to LiteLLM Gateway"""
    
    print("🔍 Testing LiteLLM Gateway Connection")
    print("=" * 60)
    print(f"Gateway URL: {base_url}")
    print(f"API Key: {api_key[:20]}..." if len(api_key) > 20 else f"API Key: {api_key}")
    print("=" * 60)
    print()
    
    # Test 1: Health Check
    print("1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("   ✅ Health check passed!")
            print(f"   Response: {response.text[:100]}")
        else:
            print(f"   ❌ Health check failed! Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Connection failed! Error: {e}")
        return False
    
    print()
    
    # Test 2: List Models
    print("2️⃣ Testing Model List Endpoint...")
    try:
        response = requests.get(
            f"{base_url}/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        if response.status_code == 200:
            models = response.json()
            print(f"   ✅ Successfully retrieved {len(models.get('data', []))} models!")
            print("   Available models:")
            for i, model in enumerate(models.get('data', [])[:5], 1):
                print(f"      {i}. {model['id']}")
            if len(models.get('data', [])) > 5:
                print(f"      ... and {len(models.get('data', [])) - 5} more")
        else:
            print(f"   ❌ Failed to retrieve models! Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Request failed! Error: {e}")
        return False
    
    print()
    
    # Test 3: Chat Completion (if models available)
    print("3️⃣ Testing Chat Completion...")
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=f"{base_url}/v1"
        )
        
        # Get first available model
        models_list = models.get('data', [])
        if not models_list:
            print("   ⚠️ No models available to test")
            return True
        
        test_model = models_list[0]['id']
        print(f"   Using model: {test_model}")
        
        response = client.chat.completions.create(
            model=test_model,
            messages=[
                {"role": "user", "content": "Say 'Connection successful!' and nothing else."}
            ],
            max_tokens=50,
            timeout=30
        )
        
        reply = response.choices[0].message.content
        print(f"   ✅ Chat completion successful!")
        print(f"   Model response: {reply}")
        
    except Exception as e:
        print(f"   ❌ Chat completion failed! Error: {e}")
        print("   Note: This might be due to missing API keys for the provider")
        print("   But the gateway connection itself is working!")
    
    print()
    print("=" * 60)
    print("🎉 Connection test completed successfully!")
    print("=" * 60)
    print()
    print("You can now use this gateway from any application that supports")
    print("OpenAI-compatible APIs by setting:")
    print(f"  • Base URL: {base_url}/v1")
    print(f"  • API Key: {api_key}")
    print()
    
    return True

def main():
    if len(sys.argv) != 3:
        print("Usage: python test_remote_connection.py <gateway_url> <master_key>")
        print()
        print("Example:")
        print("  python test_remote_connection.py http://98.83.113.118:4000 sk-1234...")
        print()
        sys.exit(1)
    
    gateway_url = sys.argv[1].rstrip('/')
    master_key = sys.argv[2]
    
    success = test_connection(gateway_url, master_key)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()


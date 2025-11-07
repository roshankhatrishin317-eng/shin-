#!/usr/bin/env python3
"""
Test Script for NVIDIA NIM Integration
Tests the NVIDIA models through the LiteLLM Gateway
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

def test_nvidia_models():
    """Test NVIDIA NIM models through the gateway"""
    
    load_dotenv()
    
    # Configuration
    base_url = os.getenv('LITELLM_BASE_URL', 'http://localhost:4000')
    api_key = os.getenv('LITELLM_MASTER_KEY', 'sk-litellm-gateway-2024')
    
    print("=" * 70)
    print("🚀 Testing NVIDIA NIM Integration")
    print("=" * 70)
    print(f"📍 Base URL: {base_url}")
    print(f"🔑 API Key: {'*' * 10}{api_key[-4:] if len(api_key) > 4 else '****'}")
    print()
    
    # Initialize OpenAI client pointing to LiteLLM
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    # Test different NVIDIA models
    nvidia_models = [
        ("nvidia-llama-3-1-nemotron-70b", "NVIDIA Llama 3.1 Nemotron 70B"),
        ("nvidia-llama-3-1-405b", "NVIDIA Llama 3.1 405B (Largest!)"),
        ("nvidia-llama-3-1-70b", "NVIDIA Llama 3.1 70B"),
        ("nvidia-llama-3-1-8b", "NVIDIA Llama 3.1 8B (Fast)"),
        ("nvidia-mistral-nemo-12b", "NVIDIA Mistral Nemo 12B"),
        ("nvidia-mistral-large-2", "NVIDIA Mistral Large 2"),
        ("moonshotai-kimi-k2", "MoonshotAI Kimi K2"),
        ("qwen-coder-480b", "Qwen3 Coder 480B"),
        ("minimax-m2", "MiniMax M2"),
    ]
    
    for model_name, description in nvidia_models:
        print(f"Testing {description}...")
        print(f"Model: {model_name}")
        print("-" * 70)
        
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": "Say 'NVIDIA NIM is working!' and tell me what model you are in one sentence."}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            print("✅ Success!")
            print(f"Response: {response.choices[0].message.content}")
            print(f"Model Used: {response.model}")
            print(f"Tokens: {response.usage.total_tokens}")
            print()
            
        except openai.APIConnectionError as e:
            print(f"❌ Connection Error: Could not connect to {base_url}")
            print(f"   Make sure the gateway is running!")
            print(f"   Error: {e}")
            print()
            return False
            
        except openai.AuthenticationError as e:
            print(f"❌ Authentication Error: Invalid API key")
            print(f"   Check your LITELLM_MASTER_KEY or NVIDIA_NIM_API_KEY in .env")
            print(f"   Error: {e}")
            print()
            return False
            
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}")
            print(f"   {e}")
            print()
            # Continue testing other models
    
    # Test streaming
    print("=" * 70)
    print("Testing Streaming with NVIDIA Model...")
    print("-" * 70)
    
    try:
        stream = client.chat.completions.create(
            model="nvidia-llama-3-1-8b",
            messages=[
                {"role": "user", "content": "Count from 1 to 5"}
            ],
            stream=True,
            max_tokens=50
        )
        
        print("Streaming response: ", end="", flush=True)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n✅ Streaming works!")
        print()
        
    except Exception as e:
        print(f"❌ Streaming error: {e}")
        print()
    
    print("=" * 70)
    print("✅ NVIDIA NIM Integration Test Complete!")
    print("=" * 70)
    print()
    print("📚 Available Models via NVIDIA NIM:")
    print()
    print("🔹 Llama Models:")
    print("   • nvidia-llama-3-1-405b - Largest (405B)")
    print("   • nvidia-llama-3-1-nemotron-70b - Powerful (70B)")
    print("   • nvidia-llama-3-1-70b - Balanced (70B)")
    print("   • nvidia-llama-3-1-8b - Fast (8B)")
    print()
    print("🔹 Mistral Models:")
    print("   • nvidia-mistral-large-2 - Latest Mistral")
    print("   • nvidia-mistral-nemo-12b - Efficient (12B)")
    print()
    print("🔹 Specialized Models:")
    print("   • moonshotai-kimi-k2 - MoonshotAI Kimi K2")
    print("   • qwen-coder-480b - Qwen3 Coder (480B)")
    print("   • minimax-m2 - MiniMax M2")
    print()
    print("💡 Usage:")
    print("   model='nvidia-llama-3-1-405b'  # Largest")
    print("   model='qwen-coder-480b'        # For coding")
    print("   model='moonshotai-kimi-k2'     # Kimi K2")
    print()
    
    return True

if __name__ == '__main__':
    success = test_nvidia_models()
    sys.exit(0 if success else 1)


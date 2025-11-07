#!/usr/bin/env python3
"""
Quick test for the newly added models:
- nvidia-llama-3-1-405b (Largest Llama model)
- moonshotai-kimi-k2 (MoonshotAI Kimi K2)
- qwen-coder-480b (Qwen3 Coder - for programming)
- minimax-m2 (MiniMax M2)
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("LITELLM_MASTER_KEY", "sk-litellm-gateway-2024"),
    base_url=os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
)

print("=" * 70)
print("🆕 Testing Newly Added Models")
print("=" * 70)
print()

# Test 1: Llama 3.1 405B (Largest!)
print("1️⃣ NVIDIA Llama 3.1 405B - The Largest Model")
print("-" * 70)
try:
    response = client.chat.completions.create(
        model="nvidia-llama-3-1-405b",
        messages=[
            {"role": "user", "content": "In one sentence, what makes you special as a 405B model?"}
        ],
        max_tokens=100
    )
    print(f"✅ Model: {response.model}")
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"❌ Error: {e}")
print()

# Test 2: MoonshotAI Kimi K2
print("2️⃣ MoonshotAI Kimi K2 - Multilingual Model")
print("-" * 70)
try:
    response = client.chat.completions.create(
        model="moonshotai-kimi-k2",
        messages=[
            {"role": "user", "content": "Say hello in both English and Chinese."}
        ],
        max_tokens=100
    )
    print(f"✅ Model: {response.model}")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")
print()

# Test 3: Qwen3 Coder 480B
print("3️⃣ Qwen3 Coder 480B - Specialized for Code")
print("-" * 70)
try:
    response = client.chat.completions.create(
        model="qwen-coder-480b",
        messages=[
            {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
        ],
        max_tokens=200
    )
    print(f"✅ Model: {response.model}")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")
print()

# Test 4: MiniMax M2
print("4️⃣ MiniMax M2 - Creative & Multilingual")
print("-" * 70)
try:
    response = client.chat.completions.create(
        model="minimax-m2",
        messages=[
            {"role": "user", "content": "Write a short creative tagline for an AI assistant."}
        ],
        max_tokens=100
    )
    print(f"✅ Model: {response.model}")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")
print()

print("=" * 70)
print("✅ New Models Test Complete!")
print("=" * 70)
print()
print("🎯 Model Recommendations:")
print("   • nvidia-llama-3-1-405b → Use for most complex reasoning")
print("   • qwen-coder-480b       → Use for all coding tasks")
print("   • moonshotai-kimi-k2    → Use for Chinese/English content")
print("   • minimax-m2            → Use for creative writing")
print()


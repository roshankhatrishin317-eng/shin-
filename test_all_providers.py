#!/usr/bin/env python3
"""
Test All Providers - Quick connectivity test
Tests one model from each active provider
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
print("🌐 Testing All Providers")
print("=" * 70)
print()

providers_to_test = [
    ("NVIDIA NIM", "nvidia-llama-3-1-8b", "Fast NVIDIA model"),
    ("iFlow", "iflow-qwen3-coder", "iFlow Qwen Coder"),
    ("OpenCode.ai", "opencode-big-pickle", "Big Pickle model"),
    ("Z.ai", "glm-4.6", "GLM 4.6 via Z.ai"),
    ("Minimax1", "minimax1-claude", "Claude via Minimax"),
]

results = []

for provider, model, description in providers_to_test:
    print(f"Testing {provider}: {description}")
    print(f"Model: {model}")
    print("-" * 70)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": f"Say 'Hello from {provider}!' in one sentence."}
            ],
            max_tokens=50,
            timeout=30
        )
        
        print(f"✅ {provider} - SUCCESS")
        print(f"   Response: {response.choices[0].message.content[:80]}...")
        results.append((provider, "✅ Working"))
        
    except Exception as e:
        error_msg = str(e)[:100]
        print(f"❌ {provider} - ERROR: {error_msg}")
        results.append((provider, f"❌ Error"))
    
    print()

print("=" * 70)
print("📊 Provider Status Summary")
print("=" * 70)
print()

for provider, status in results:
    print(f"{status:15} {provider}")

print()
print("=" * 70)

working_count = sum(1 for _, status in results if "✅" in status)
total_count = len(results)

print(f"\n✅ Working Providers: {working_count}/{total_count}")
print()

if working_count == total_count:
    print("🎉 All providers are working correctly!")
else:
    print("⚠️  Some providers may need attention. Check API keys and endpoints.")

print()
print("📚 For detailed documentation, see:")
print("   • ALL_PROVIDERS_SUMMARY.md - Complete guide")
print("   • NVIDIA_MODELS_UPDATED.md - NVIDIA models")
print("   • OPENAI_COMPATIBLE.md - API usage")
print()


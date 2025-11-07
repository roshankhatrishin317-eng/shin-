#!/usr/bin/env python3
"""
Basic Usage Examples for LiteLLM Gateway
Based on: https://docs.litellm.ai/docs/

This script demonstrates how to use the LiteLLM Gateway with the OpenAI SDK.
"""

import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure client to use LiteLLM Gateway
client = openai.OpenAI(
    api_key=os.getenv("LITELLM_MASTER_KEY", "your-master-key"),
    base_url=os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
)

def example_basic_chat():
    """Basic chat completion example"""
    print("=" * 60)
    print("Example 1: Basic Chat Completion")
    print("=" * 60)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello, how are you?"}
        ]
    )
    
    print(f"Model: {response.model}")
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens used: {response.usage.total_tokens}")
    print()


def example_streaming():
    """Streaming response example"""
    print("=" * 60)
    print("Example 2: Streaming Response")
    print("=" * 60)
    
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Write a short poem about AI"}
        ],
        stream=True
    )
    
    print("Streaming response: ", end="", flush=True)
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")


def example_anthropic():
    """Example using Anthropic Claude through the gateway"""
    print("=" * 60)
    print("Example 3: Using Claude via Gateway")
    print("=" * 60)
    
    try:
        response = client.chat.completions.create(
            model="claude-3-5-sonnet",  # Model name from config.yaml
            messages=[
                {"role": "user", "content": "Explain quantum computing in one sentence."}
            ]
        )
        
        print(f"Model: {response.model}")
        print(f"Response: {response.choices[0].message.content}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure ANTHROPIC_API_KEY is set in your .env file")
        print()


def example_multiple_messages():
    """Example with conversation history"""
    print("=" * 60)
    print("Example 4: Conversation with History")
    print("=" * 60)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that speaks like a pirate."},
        {"role": "user", "content": "What's the weather like?"},
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    print(f"Response: {response.choices[0].message.content}")
    print()


def example_with_parameters():
    """Example with various parameters"""
    print("=" * 60)
    print("Example 5: Using Different Parameters")
    print("=" * 60)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Generate 3 creative product names for a smart water bottle"}
        ],
        temperature=0.9,  # Higher creativity
        max_tokens=100,
        n=1,  # Number of completions
    )
    
    print(f"Response: {response.choices[0].message.content}")
    print(f"Finish reason: {response.choices[0].finish_reason}")
    print()


if __name__ == "__main__":
    print("\n🚀 LiteLLM Gateway - Usage Examples\n")
    print(f"Gateway URL: {os.getenv('LITELLM_BASE_URL', 'http://localhost:4000')}")
    print(f"Master Key: {'Set ✓' if os.getenv('LITELLM_MASTER_KEY') else 'Not Set ⚠️'}")
    print()
    
    try:
        # Run examples
        example_basic_chat()
        example_streaming()
        example_multiple_messages()
        example_with_parameters()
        
        # Only run Anthropic example if key is available
        if os.getenv("ANTHROPIC_API_KEY"):
            example_anthropic()
        else:
            print("⏭️  Skipping Anthropic example (ANTHROPIC_API_KEY not set)\n")
        
        print("✅ All examples completed successfully!")
        
    except openai.APIConnectionError as e:
        print(f"❌ Connection Error: Could not connect to gateway")
        print(f"   Make sure the gateway is running on port 4000")
        print(f"   Error: {e}")
    
    except openai.AuthenticationError as e:
        print(f"❌ Authentication Error: Invalid API key")
        print(f"   Check your LITELLM_MASTER_KEY in .env")
        print(f"   Error: {e}")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


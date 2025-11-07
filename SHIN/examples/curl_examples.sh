#!/bin/bash
# cURL Examples for LiteLLM Gateway
# Based on: https://docs.litellm.ai/docs/
#
# Make sure to:
# 1. Start the gateway: python start_gateway.py
# 2. Set your LITELLM_MASTER_KEY in .env

# Load environment variables (if using bash)
if [ -f ../.env ]; then
    export $(cat ../.env | grep -v '^#' | xargs)
fi

GATEWAY_URL="${LITELLM_BASE_URL:-http://localhost:4000}"
API_KEY="${LITELLM_MASTER_KEY:-your-master-key}"

echo "🚀 LiteLLM Gateway - cURL Examples"
echo "===================================="
echo "Gateway URL: $GATEWAY_URL"
echo ""

# Example 1: Basic Chat Completion
echo "Example 1: Basic Chat Completion"
echo "--------------------------------"
curl "$GATEWAY_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "Hello! Say hi back."
      }
    ]
  }'
echo -e "\n\n"

# Example 2: With System Message
echo "Example 2: With System Message"
echo "-------------------------------"
curl "$GATEWAY_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant that speaks like Shakespeare."
      },
      {
        "role": "user",
        "content": "Tell me about the weather."
      }
    ],
    "max_tokens": 100
  }'
echo -e "\n\n"

# Example 3: Streaming Response
echo "Example 3: Streaming Response"
echo "-----------------------------"
curl "$GATEWAY_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "Count from 1 to 5."
      }
    ],
    "stream": true
  }'
echo -e "\n\n"

# Example 4: Using Claude (if configured)
echo "Example 4: Using Claude Model"
echo "------------------------------"
curl "$GATEWAY_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "claude-3-5-sonnet",
    "messages": [
      {
        "role": "user",
        "content": "What is 2+2?"
      }
    ]
  }'
echo -e "\n\n"

# Example 5: Health Check
echo "Example 5: Health Check"
echo "-----------------------"
curl "$GATEWAY_URL/health"
echo -e "\n\n"

# Example 6: Model List
echo "Example 6: List Available Models"
echo "---------------------------------"
curl "$GATEWAY_URL/v1/models" \
  -H "Authorization: Bearer $API_KEY"
echo -e "\n\n"

echo "✅ All examples completed!"


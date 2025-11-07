#!/bin/bash

# Quick Start Script for LiteLLM Gateway
# This script helps you set up and start the gateway

echo "🚀 LiteLLM Gateway - Quick Start"
echo "================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.template .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys:"
    echo "   - LITELLM_MASTER_KEY (for gateway authentication)"
    echo "   - OPENAI_API_KEY (if using OpenAI models)"
    echo "   - ANTHROPIC_API_KEY (if using Anthropic models)"
    echo ""
    read -p "Press Enter to open .env in nano (or Ctrl+C to exit and edit manually)..."
    nano .env
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🔍 Checking Python dependencies..."
if ! python3 -c "import litellm" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🎯 Starting LiteLLM Gateway..."
echo ""
python3 start_gateway.py


#!/bin/bash
# Setup script to create .env file with NVIDIA configuration

echo "🟢 Setting up NVIDIA NIM configuration..."
echo ""

# Create .env file
cat > .env << 'EOF'
# LiteLLM Gateway Configuration
# Generated with NVIDIA NIM integration

# Master key for authenticating with the LiteLLM proxy
LITELLM_MASTER_KEY=sk-litellm-gateway-2024

# NVIDIA NIM API (NVIDIA Inference Microservices)
NVIDIA_NIM_API_KEY=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
NVIDIA_NIM_API_BASE=https://integrate.api.nvidia.com/v1

# Additional NVIDIA API Key (for load balancing - see config_nvidia_loadbalance.yaml)
# NVIDIA_NIM_API_KEY_2=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

# OpenAI API Key (optional - uncomment if you want to use OpenAI models)
# OPENAI_API_KEY=sk-your-openai-key-here

# Anthropic API Key (optional - uncomment if you want to use Claude models)
# ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Azure OpenAI (optional)
# AZURE_API_KEY=your-azure-key-here
# AZURE_API_BASE=https://your-resource.openai.azure.com/

# Gateway settings
LITELLM_PORT=4000
LITELLM_HOST=0.0.0.0
LITELLM_BASE_URL=http://localhost:4000
EOF

echo "✅ Created .env file with NVIDIA configuration"
echo ""
echo "📋 Configuration Summary:"
echo "   • NVIDIA API Key 1: nvapi-W2jN...T5da (Active)"
echo "   • NVIDIA API Key 2: nvapi-tCzM...2E5S (Available for load balancing)"
echo "   • Gateway Master Key: sk-litellm-gateway-2024"
echo "   • Gateway Port: 4000"
echo ""
echo "🚀 Next steps:"
echo "   1. Start gateway: python start_gateway.py"
echo "   2. Test NVIDIA:   python test_nvidia.py"
echo ""


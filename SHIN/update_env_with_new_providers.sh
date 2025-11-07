#!/bin/bash
# Script to update .env file with new provider API keys

echo "🔧 Updating .env with new provider configurations..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp env.template .env
fi

# Add new provider keys to .env if not already present
if ! grep -q "OPENCODE_API_KEY" .env; then
    cat >> .env << 'EOF'

# OpenCode.ai Provider
OPENCODE_API_KEY=sk-Nl9LXlUnTLqto9OtzhSnC4miavUT53ub3XLpOptEX1E9tMqWgBezpsweF6Xhaldu

# Z.ai Provider (GLM)
ZAI_API_KEY=3ac47a4dd15e40418607e1c7dddde823.QghF1VETCzdSVFtq

# iFlow Provider
IFLOW_API_KEY=sk-54dadfcb9878fd37d68ee227379c4665

# Minimax1 Provider
MINIMAX1_API_KEY=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJEZWx0YSIsIlVzZXJOYW1lIjoiRGVsdGEiLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTk4Mjc1ODkwNjUzNDgzMDg0OSIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5ODI3NTg5MDY1MzA2MzI0NDkiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJkZWx0YWFwb2MzMTdAZ21haWwuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMTAtMzAgMTk6Mjk6MDAiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.bSMFu2hjbMKqkJsRsYuhpYQjBO_qYhWVrdNbU-h-t7Bj3CqdwwWHW8jiU5Si87DZBNlmE0VNgZObn2BoPjzjyGlJ8hqRYdGlqg2Qt8nUQhJNLMlg63FWlJS57ho29aXNqzBX0Bf8rFhD4BZdS2w905HicROGi8C3ZJ2jMk27oDeSbDJAneMhr_vGw78NwPwf32xpMYTGUjjVWZtbLzGXj6KcV4GGncUP5_F2FebZSEnmDl967H6W8eamEo6QcOgCGlsg8fdUu-7b3JFnxnRi_zWrfTiIc7bBB5hixcCSAXHrucawpA6r59pPLes4lQn3Qxxt6qRuWwmww_KvTMxyqA
EOF
    echo "✅ Added new provider keys to .env"
else
    echo "✅ Provider keys already exist in .env"
fi

echo ""
echo "📋 Summary of new providers added:"
echo "   • OpenCode.ai - big-pickle model"
echo "   • Z.ai - GLM 4.6 model"
echo "   • iFlow - 7 models (Qwen, Kimi, GLM, DeepSeek)"
echo "   • Minimax1 - Claude endpoint"
echo ""
echo "✅ Configuration complete!"
echo ""
echo "🚀 Next step: python start_gateway.py"


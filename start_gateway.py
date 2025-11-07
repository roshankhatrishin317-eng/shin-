#!/usr/bin/env python3
"""
LiteLLM Gateway Starter Script
This script starts the LiteLLM proxy server with the specified configuration.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("⚠️  Warning: .env file not found!")
        print("📝 Please copy env.template to .env and configure your API keys")
        print("   cp env.template .env")
        print()
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Check if config.yaml exists
    if not Path('config.yaml').exists():
        print("❌ Error: config.yaml not found!")
        sys.exit(1)
    
    # Set default port
    port = os.getenv('LITELLM_PORT', '4000')
    host = os.getenv('LITELLM_HOST', '0.0.0.0')
    
    print("🚀 Starting LiteLLM Gateway...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"📄 Config: config.yaml")
    print(f"🔑 Master Key: {'Set ✓' if os.getenv('LITELLM_MASTER_KEY') else 'Not Set ⚠️'}")
    print()
    
    # Start the LiteLLM proxy
    cmd = [
        'litellm',
        '--config', 'config.yaml',
        '--host', host,
        '--port', port,
        '--detailed_debug'
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down LiteLLM Gateway...")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting gateway: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()


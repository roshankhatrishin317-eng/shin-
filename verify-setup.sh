#!/bin/bash

# Script to verify that all components for Cloudflare Tunnel are properly set up

echo "=== Cloudflare Tunnel Setup Verification ==="
echo

# Check if cloudflared is installed
echo "1. Checking if cloudflared is installed..."
if command -v cloudflared &> /dev/null
then
    echo "   ✅ cloudflared is installed"
    cloudflared_version=$(cloudflared --version)
    echo "   Version: $cloudflared_version"
else
    echo "   ❌ cloudflared is not installed"
    echo "   Please install cloudflared first"
    exit 1
fi
echo

# Check if required files exist
echo "2. Checking required files..."
required_files=("run-tunnel.sh" "setup-permanent-tunnel.sh" "start-test-server.sh" "test-server.py" "cloudflared-config.yml")

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file exists"
    else
        echo "   ❌ $file is missing"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo "   Some required files are missing. Please check the installation."
    exit 1
else
    echo "   All required files are present"
fi
echo

# Check file permissions
echo "3. Checking file permissions..."
executable_files=("run-tunnel.sh" "setup-permanent-tunnel.sh" "start-test-server.sh" "test-server.py")

all_executable=true
for file in "${executable_files[@]}"; do
    if [ -x "$file" ]; then
        echo "   ✅ $file is executable"
    else
        echo "   ❌ $file is not executable"
        echo "   Run: chmod +x $file"
        all_executable=false
    fi
done

if [ "$all_executable" = false ]; then
    echo "   Some files are not executable. Please fix permissions."
    exit 1
else
    echo "   All script files are executable"
fi
echo

# Check if port 4000 is in use
echo "4. Checking port 4000 status..."
if ss -tuln | grep -q ":4000 "; then
    echo "   ⚠ Port 4000 is currently in use"
    echo "   Process information:"
    ss -tulnp | grep ":4000 " | head -1
    echo "   This may be your existing service or the test server"
else
    echo "   ℹ Port 4000 is available"
    echo "   You can start a service on this port"
fi
echo

# Summary
echo "=== Summary ==="
echo "✅ Cloudflare Tunnel setup verification completed"
echo
echo "Next steps:"
echo "1. If you want to test with the sample server:"
echo "   ./start-test-server.sh"
echo
echo "2. In another terminal, run one of these:"
echo "   ./run-tunnel.sh              # For temporary testing"
echo "   ./setup-permanent-tunnel.sh  # For permanent setup"
echo
echo "Note: For permanent setup, you'll need a Cloudflare account and domain."
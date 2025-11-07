#!/bin/bash

# Script to run Cloudflare Tunnel for localhost:4000
# This requires a Cloudflare account for permanent tunnels
# For temporary testing, we can use the --name option

echo "Setting up Cloudflare Tunnel for http://localhost:4000"

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null
then
    echo "cloudflared could not be found. Please install it first."
    exit 1
fi

# Run a temporary tunnel
echo "Creating temporary tunnel..."
cloudflared tunnel --name temp-tunnel-4000 --url http://localhost:4000

echo "Tunnel is now running. Press Ctrl+C to stop."
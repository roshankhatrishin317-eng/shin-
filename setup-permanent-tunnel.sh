#!/bin/bash

# Script to set up a permanent Cloudflare Tunnel for localhost:4000

echo "=== Cloudflare Tunnel Setup for localhost:4000 ==="

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null
then
    echo "ERROR: cloudflared could not be found. Please install it first."
    exit 1
fi

echo "✓ cloudflared is installed"

# Check if service is running on port 4000
if ss -tuln | grep -q ":4000 "
then
    echo "✓ Service detected on port 4000"
else
    echo "⚠ No service detected on port 4000. Please start your service before running the tunnel."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    fi
fi

echo
echo "=== Step 1: Login to Cloudflare ==="
echo "You will be redirected to Cloudflare to authenticate."
echo "Please complete the authentication in your browser."
echo "Press Enter to continue..."
read

cloudflared tunnel login

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to login to Cloudflare"
    exit 1
fi

echo
echo "=== Step 2: Create Tunnel ==="
read -p "Enter a name for your tunnel (e.g., my-local-service): " tunnel_name

if [ -z "$tunnel_name" ]; then
    echo "ERROR: Tunnel name cannot be empty"
    exit 1
fi

cloudflared tunnel create "$tunnel_name"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create tunnel"
    exit 1
fi

# Extract tunnel UUID
tunnel_info=$(cloudflared tunnel list | grep "$tunnel_name")
tunnel_uuid=$(echo "$tunnel_info" | awk '{print $1}')

echo "✓ Tunnel created with UUID: $tunnel_uuid"

echo
echo "=== Step 3: Configure DNS ==="
read -p "Enter your domain (e.g., example.com): " domain
read -p "Enter subdomain (e.g., local-service): " subdomain

if [ -z "$domain" ] || [ -z "$subdomain" ]; then
    echo "ERROR: Domain and subdomain cannot be empty"
    exit 1
fi

full_domain="$subdomain.$domain"
echo "Setting up DNS route for $full_domain"

cloudflared tunnel route dns "$tunnel_name" "$full_domain"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to set up DNS route"
    exit 1
fi

echo "✓ DNS route configured for $full_domain"

echo
echo "=== Step 4: Create Configuration File ==="

# Create config file
cat > ~/.cloudflared/config.yml << EOF
tunnel: $tunnel_uuid
credentials-file: ~/.cloudflared/$tunnel_uuid.json
ingress:
  - hostname: $full_domain
    service: http://localhost:4000
  - service: http_status:404
EOF

echo "✓ Configuration file created at ~/.cloudflared/config.yml"

echo
echo "=== Setup Complete ==="
echo "To run your tunnel, execute:"
echo "  cloudflared tunnel run $tunnel_name"
echo
echo "Your service will be accessible at: https://$full_domain"
echo
echo "To run the tunnel in the background:"
echo "  cloudflared tunnel run $tunnel_name &"
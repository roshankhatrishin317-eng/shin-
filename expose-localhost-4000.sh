#!/bin/bash

# Complete workflow script to expose localhost:4000 using Cloudflare Tunnel

echo "=== Expose localhost:4000 with Cloudflare Tunnel ==="
echo

# Function to check prerequisites
check_prerequisites() {
    echo "Checking prerequisites..."
    
    # Check if cloudflared is installed
    if ! command -v cloudflared &> /dev/null
    then
        echo "❌ ERROR: cloudflared is not installed"
        echo "Please install cloudflared first:"
        echo "  curl -L https://bin.equinox.io/c/VdrWfHFUsB/cloudflared-stable-linux-amd64.deb -o cloudflared.deb"
        echo "  sudo dpkg -i cloudflared.deb"
        exit 1
    else
        echo "✅ cloudflared is installed ($(cloudflared --version))"
    fi
    
    # Check if port 4000 is in use
    if ss -tuln | grep -q ":4000 "
    then
        echo "✅ Service detected on port 4000"
        service_info=$(ss -tulnp | grep ":4000 " | head -1)
        echo "   Service info: $service_info"
    else
        echo "⚠ No service detected on port 4000"
        echo "   You'll need to start a service before exposing it"
    fi
    
    echo
}

# Function for temporary exposure
temporary_exposure() {
    echo "=== Creating Temporary Tunnel ==="
    echo
    echo "This will create a temporary URL for your service."
    echo "No Cloudflare account required."
    echo
    
    read -p "Continue with temporary tunnel? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]
    then
        echo "Operation cancelled."
        exit 0
    fi
    
    echo "Starting temporary tunnel..."
    echo "Press Ctrl+C to stop"
    echo
    
    cloudflared tunnel --url http://localhost:4000
}

# Function for permanent exposure
permanent_exposure() {
    echo "=== Setting Up Permanent Tunnel ==="
    echo
    echo "This will create a permanent tunnel with a custom domain."
    echo "Requires a Cloudflare account and domain."
    echo
    
    read -p "Continue with permanent tunnel setup? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]
    then
        echo "Operation cancelled."
        exit 0
    fi
    
    # Run the setup script
    ./setup-permanent-tunnel.sh
}

# Main menu
main_menu() {
    echo "Choose an option:"
    echo "1) Quick temporary exposure (no account needed)"
    echo "2) Permanent exposure (requires Cloudflare account)"
    echo "3) Verify setup"
    echo "4) Exit"
    echo
    
    read -p "Enter choice (1-4): " choice
    
    case $choice in
        1)
            temporary_exposure
            ;;
        2)
            permanent_exposure
            ;;
        3)
            ./verify-setup.sh
            main_menu
            ;;
        4)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter 1, 2, 3, or 4."
            main_menu
            ;;
    esac
}

# Run the script
check_prerequisites
main_menu
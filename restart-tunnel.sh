#!/bin/bash

# Script to restart Cloudflare Tunnel for localhost:4000

echo "=== Restarting Cloudflare Tunnel for localhost:4000 ==="
echo

# Function to kill existing tunnel processes
kill_existing_tunnels() {
    echo "Checking for existing tunnel processes..."
    
    # Find cloudflared processes
    tunnel_pids=$(pgrep -f "cloudflared.*tunnel")
    
    if [ -n "$tunnel_pids" ]; then
        echo "Found existing tunnel processes: $tunnel_pids"
        echo "Killing them..."
        kill $tunnel_pids 2>/dev/null
        
        # Wait a moment for processes to terminate
        sleep 2
        
        # Force kill if still running
        kill -9 $tunnel_pids 2>/dev/null
        echo "Existing tunnel processes terminated."
    else
        echo "No existing tunnel processes found."
    fi
    echo
}

# Function to clean up tunnel connections
cleanup_tunnels() {
    echo "Cleaning up tunnel connections..."
    cloudflared tunnel cleanup --help >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        # Try to cleanup tunnels (this might fail if no tunnels exist)
        cloudflared tunnel cleanup 2>/dev/null
        echo "Tunnel cleanup attempted."
    else
        echo "Cleanup command not available in this version."
    fi
    echo
}

# Function to restart temporary tunnel
restart_temporary_tunnel() {
    echo "Restarting temporary tunnel..."
    
    # Kill existing tunnels
    kill_existing_tunnels
    
    # Clean up connections
    cleanup_tunnels
    
    echo "Starting new temporary tunnel..."
    echo "Press Ctrl+C to stop"
    echo "=========================================="
    
    # Start the tunnel
    cloudflared tunnel --url http://localhost:4000
}

# Function to restart permanent tunnel
restart_permanent_tunnel() {
    echo "Restarting permanent tunnel..."
    
    # Check if tunnel name is provided
    if [ -z "$1" ]; then
        echo "Available tunnels:"
        cloudflared tunnel list
        echo
        read -p "Enter tunnel name or UUID: " tunnel_name
    else
        tunnel_name="$1"
    fi
    
    if [ -z "$tunnel_name" ]; then
        echo "Error: No tunnel name provided"
        exit 1
    fi
    
    # Kill existing tunnels
    kill_existing_tunnels
    
    # Clean up connections
    cleanup_tunnels
    
    echo "Starting tunnel: $tunnel_name"
    echo "Press Ctrl+C to stop"
    echo "=========================================="
    
    # Start the tunnel
    cloudflared tunnel run "$tunnel_name"
}

# Main script
case "$1" in
    --temp|-t)
        restart_temporary_tunnel
        ;;
    --permanent|-p)
        restart_permanent_tunnel "$2"
        ;;
    --help|-h)
        echo "Usage: $0 [OPTION] [TUNNEL_NAME]"
        echo "Restart Cloudflare Tunnel for localhost:4000"
        echo
        echo "Options:"
        echo "  -t, --temp        Restart temporary tunnel"
        echo "  -p, --permanent   Restart permanent tunnel with optional name"
        echo "  -h, --help        Show this help message"
        echo
        echo "Examples:"
        echo "  $0                   # Interactive restart"
        echo "  $0 --temp            # Restart temporary tunnel"
        echo "  $0 --permanent my-tunnel  # Restart specific permanent tunnel"
        ;;
    *)
        # Interactive mode
        echo "Choose restart option:"
        echo "1) Temporary tunnel (no account needed)"
        echo "2) Permanent tunnel (requires tunnel name)"
        echo "3) Cancel"
        echo
        
        read -p "Enter choice (1-3): " choice
        
        case $choice in
            1)
                restart_temporary_tunnel
                ;;
            2)
                restart_permanent_tunnel
                ;;
            3|*)
                echo "Restart cancelled."
                exit 0
                ;;
        esac
        ;;
esac
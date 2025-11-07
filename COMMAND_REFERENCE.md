# Cloudflare Tunnel Command Reference

This document provides quick reference commands for working with Cloudflare Tunnel to expose localhost:4000.

## Quick Commands

### Temporary Tunnel (No Account Required)
```bash
# Run a temporary tunnel for localhost:4000
./run-tunnel.sh

# Or directly with cloudflared
cloudflared tunnel --url http://localhost:4000
```

### Permanent Tunnel Setup
```bash
# Login to Cloudflare
cloudflared tunnel login

# Create a new tunnel
cloudflared tunnel create TUNNEL_NAME

# Get tunnel UUID
cloudflared tunnel list

# Route DNS (requires domain)
cloudflared tunnel route dns TUNNEL_NAME SUBDOMAIN.DOMAIN.COM

# Run the tunnel
cloudflared tunnel run TUNNEL_NAME
```

### Restarting Tunnels
```bash
# Restart with our helper script
./restart-tunnel.sh

# Kill existing tunnel processes
pkill -f "cloudflared.*tunnel"

# Clean up tunnel connections
cloudflared tunnel cleanup

# Restart temporary tunnel
./restart-tunnel.sh --temp

# Restart permanent tunnel
./restart-tunnel.sh --permanent TUNNEL_NAME
```

## Essential cloudflared Commands

### Authentication
```bash
# Login to Cloudflare account
cloudflared tunnel login

# Show current credentials
cloudflared tunnel list
```

### Tunnel Management
```bash
# Create a new tunnel
cloudflared tunnel create TUNNEL_NAME

# List all tunnels
cloudflared tunnel list

# Delete a tunnel
cloudflared tunnel delete TUNNEL_NAME

# Get tunnel information
cloudflared tunnel info TUNNEL_NAME

# Clean up tunnel connections
cloudflared tunnel cleanup
```

### DNS Routing
```bash
# Route tunnel to DNS record
cloudflared tunnel route dns TUNNEL_NAME SUBDOMAIN.DOMAIN.COM

# Route tunnel to Load Balancer
cloudflared tunnel route lb TUNNEL_NAME LB_NAME LB_POOL

# List routes
cloudflared tunnel route dns --help
```

### Running Tunnels
```bash
# Run tunnel by name
cloudflared tunnel run TUNNEL_NAME

# Run tunnel with config file
cloudflared tunnel --config CONFIG_FILE run TUNNEL_NAME

# Run tunnel in background
cloudflared tunnel run TUNNEL_NAME &

# Run with custom URL
cloudflared tunnel --url http://localhost:4000
```

## Configuration

### Sample Configuration File (~/.cloudflared/config.yml)
```yaml
tunnel: TUNNEL_UUID
credentials-file: /path/to/credentials.json
ingress:
  - hostname: subdomain.domain.com
    service: http://localhost:4000
  - service: http_status:404
```

### Environment Variables
```bash
# Tunnel origin certificate path
export TUNNEL_ORIGIN_CERT=/path/to/cert.pem

# Tunnel URL
export TUNNEL_URL=http://localhost:4000

# Log level
export TUNNEL_LOGLEVEL=info
```

## Common Issues and Solutions

### Port Already in Use
```bash
# Check what's using port 4000
ss -tulnp | grep :4000

# Kill process using port 4000 (replace PID)
kill -9 PID
```

### Certificate Issues
```bash
# Re-authenticate
cloudflared tunnel login

# Check certificate location
ls -la ~/.cloudflared/
```

### Connection Problems
```bash
# Check tunnel status
cloudflared tunnel info TUNNEL_NAME

# Enable debug logging
export TUNNEL_LOGLEVEL=debug
cloudflared tunnel run TUNNEL_NAME
```

### Restart Issues
```bash
# Kill all cloudflared processes
pkill cloudflared

# Check for remaining processes
pgrep -f cloudflared

# Force kill if needed
kill -9 $(pgrep -f cloudflared)
```

## Useful URLs

- Cloudflare Dashboard: https://dash.cloudflare.com
- Tunnel Documentation: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- Troubleshooting Guide: https://developers.cloudflare.com/cloudflare-one/faq/

## File Locations

- Configuration files: `~/.cloudflared/`
- Credentials: `~/.cloudflared/TUNNEL_UUID.json`
- Certificates: `~/.cloudflared/cert.pem`
- Logs: Check terminal output or specify with `--logfile`
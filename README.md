# Cloudflare Tunnel Setup for Localhost:4000

This guide explains how to expose your local service running on `http://localhost:4000` to the internet using Cloudflare Tunnel.

## Important Note

There is already a service (`litellm`) running on port 4000. See [USING_EXISTING_SERVICE.md](USING_EXISTING_SERVICE.md) for specific instructions on using Cloudflare Tunnel with this existing service.

## Files in this Repository

1. `cloudflared-config.yml` - Sample configuration file for Cloudflare Tunnel
2. `run-tunnel.sh` - Script to run a temporary tunnel for quick testing
3. `setup-permanent-tunnel.sh` - Automated script for setting up a permanent tunnel
4. `start-test-server.sh` - Script to start the test server on port 4000
5. `test-server.py` - Simple Python HTTP server for testing the tunnel (only needed if no service is running on port 4000)
6. `verify-setup.sh` - Script to verify that all components are properly set up
7. `README.md` - This file
8. `USING_EXISTING_SERVICE.md` - Instructions for using Cloudflare Tunnel with the existing service on port 4000
9. `COMMAND_REFERENCE.md` - Quick reference for cloudflared commands
10. `expose-localhost-4000.sh` - Main workflow script with menu options
11. `restart-tunnel.sh` - Script to restart tunnel connections

## Prerequisites

1. A Cloudflare account (free tier is sufficient)
2. A domain name managed by Cloudflare
3. `cloudflared` installed (already done)

## Quick Start (Temporary Tunnel)

For quick testing without setting up a permanent tunnel:

```bash
./run-tunnel.sh
```

This will create a temporary tunnel and provide you with a URL to access your service.

## Restarting the Tunnel

To restart the tunnel:

```bash
./restart-tunnel.sh
```

This will:
1. Terminate any existing tunnel processes
2. Clean up tunnel connections
3. Start a fresh tunnel

Options:
- `./restart-tunnel.sh --temp` - Restart temporary tunnel
- `./restart-tunnel.sh --permanent TUNNEL_NAME` - Restart specific permanent tunnel

## Permanent Setup (Automated)

Run the automated setup script:

```bash
./setup-permanent-tunnel.sh
```

This interactive script will guide you through:
1. Logging into your Cloudflare account
2. Creating a new tunnel
3. Configuring DNS routing
4. Setting up the configuration file

## Testing the Setup (Only if no service is running on port 4000)

1. Start the test server:
   ```bash
   ./start-test-server.sh
   ```

2. In another terminal, run the tunnel:
   ```bash
   # For temporary testing:
   ./run-tunnel.sh
   
   # Or for permanent setup:
   ./setup-permanent-tunnel.sh
   ```

3. Access your service through the provided Cloudflare URL

## Manual Permanent Setup

### 1. Login to Cloudflare

```bash
cloudflared tunnel login
```

This will open a browser window where you can authenticate with your Cloudflare account.

### 2. Create a Tunnel

```bash
cloudflared tunnel create my-local-tunnel
```

This creates a new tunnel named "my-local-tunnel".

### 3. Configure the Tunnel

Edit the configuration file (usually located at `~/.cloudflared/<tunnel-uuid>.json`) or create a new one:

```yaml
# ~/.cloudflared/config.yml
tunnel: <tunnel-uuid>
credentials-file: /home/user/.cloudflared/<tunnel-uuid>.json
ingress:
  - hostname: your-subdomain.your-domain.com
    service: http://localhost:4000
  - service: http_status:404
```

### 4. Route Traffic to Your Tunnel

```bash
cloudflared tunnel route dns my-local-tunnel your-subdomain.your-domain.com
```

### 5. Run the Tunnel

```bash
cloudflared tunnel run my-local-tunnel
```

Your service will now be accessible at `https://your-subdomain.your-domain.com`.

## Configuration Files

- `cloudflared-config.yml`: Sample configuration file
- `run-tunnel.sh`: Script to run a temporary tunnel
- `setup-permanent-tunnel.sh`: Automated script for permanent tunnel setup
- `start-test-server.sh`: Script to start the test server
- `test-server.py`: Simple test server for port 4000
- `verify-setup.sh`: Verification script
- `USING_EXISTING_SERVICE.md`: Instructions for existing service
- `COMMAND_REFERENCE.md`: Command reference
- `expose-localhost-4000.sh`: Main workflow script
- `restart-tunnel.sh`: Tunnel restart script

## Troubleshooting

1. **Port already in use**: Check if another service is using port 4000:
   ```bash
   ss -tulnp | grep :4000
   ```

2. **Permission denied**: Make sure the scripts are executable:
   ```bash
   chmod +x *.sh
   ```

3. **Authentication issues**: Re-authenticate with Cloudflare:
   ```bash
   cloudflared tunnel login

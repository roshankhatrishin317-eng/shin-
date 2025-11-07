# Using Cloudflare Tunnel with Existing Service on Port 4000

There is already a service (`litellm`) running on port 4000 that you can expose to the internet using Cloudflare Tunnel.

## Current Service Information

From our verification, we can see:
```
Port 4000 is currently in use by:
litellm (process ID: 31549)
```

This means you don't need to start a test server - you can directly expose the existing service.

## Quick Start Options

### Option 1: Temporary Tunnel (No Account Required)

Run a temporary tunnel to quickly expose your service:

```bash
./run-tunnel.sh
```

This will generate a temporary URL that you can use to access your litellm service from anywhere.

### Option 2: Permanent Tunnel (Requires Cloudflare Account)

Set up a permanent tunnel with a custom subdomain:

```bash
./setup-permanent-tunnel.sh
```

Follow the prompts to:
1. Log in to your Cloudflare account
2. Create a named tunnel
3. Configure DNS routing
4. Set up your permanent URL

## Restarting the Tunnel

If you need to restart the tunnel connection:

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

## Accessing Your Service

Once the tunnel is running, you'll see a URL in the terminal output:

- For temporary tunnels: A randomly generated URL like `https://random-subdomain.trycloudflare.com`
- For permanent tunnels: Your custom domain like `https://your-subdomain.your-domain.com`

You can access your litellm service through this URL exactly as if you were accessing `http://localhost:4000` directly.

## Stopping the Tunnel

To stop the tunnel, press `Ctrl+C` in the terminal where the tunnel is running.

## Important Notes

1. **Security**: The litellm service will be accessible from the public internet when the tunnel is running. Ensure it's properly secured with authentication if needed.

2. **Performance**: Cloudflare Tunnel provides good performance with minimal latency overhead.

3. **Reliability**: The tunnel automatically handles connection interruptions and will reconnect when network issues occur.

4. **Logging**: Both cloudflared and your litellm service will continue to log requests normally.

## Troubleshooting

If you encounter issues:

1. **Check if the service is still running**:
   ```bash
   ss -tulnp | grep :4000
   ```

2. **Restart the tunnel**:
   Stop the tunnel with `Ctrl+C` and restart it with the same command, or use:
   ```bash
   ./restart-tunnel.sh
   ```

3. **Check cloudflared logs**:
   The tunnel output will show connection status and any errors.

4. **Verify firewall settings**:
   Cloudflare Tunnel works by establishing outbound connections, so it typically works even behind restrictive firewalls.
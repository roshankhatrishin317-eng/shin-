#!/bin/bash
# Manage Cloudflare Tunnel for LiteLLM Gateway

case "$1" in
  start)
    echo "🚀 Starting Cloudflare Tunnel..."
    ./cloudflared tunnel --url http://localhost:4000 > tunnel.log 2>&1 &
    echo $! > tunnel.pid
    sleep 5
    URL=$(grep -oP "https://[a-zA-Z0-9-]+\.trycloudflare\.com" tunnel.log | head -1)
    echo "✅ Tunnel started!"
    echo ""
    echo "🌐 Your public URL:"
    echo "   $URL"
    echo ""
    echo "📋 Base URL for apps:"
    echo "   $URL/v1"
    echo ""
    echo "🔑 Master Key:"
    grep LITELLM_MASTER_KEY .env | cut -d'=' -f2
    ;;
    
  stop)
    echo "🛑 Stopping tunnel..."
    kill $(cat tunnel.pid 2>/dev/null) 2>/dev/null
    rm -f tunnel.pid
    echo "✅ Tunnel stopped"
    ;;
    
  restart)
    echo "🔄 Restarting tunnel..."
    $0 stop
    sleep 2
    $0 start
    ;;
    
  status)
    if [ -f tunnel.pid ] && ps -p $(cat tunnel.pid) > /dev/null 2>&1; then
      echo "✅ Tunnel is running (PID: $(cat tunnel.pid))"
      URL=$(grep -oP "https://[a-zA-Z0-9-]+\.trycloudflare\.com" tunnel.log | head -1)
      echo "🌐 URL: $URL"
    else
      echo "❌ Tunnel is not running"
    fi
    ;;
    
  url)
    URL=$(grep -oP "https://[a-zA-Z0-9-]+\.trycloudflare\.com" tunnel.log | head -1)
    if [ -z "$URL" ]; then
      echo "❌ No URL found. Is tunnel running?"
    else
      echo "$URL"
    fi
    ;;
    
  *)
    echo "Usage: $0 {start|stop|restart|status|url}"
    echo ""
    echo "Commands:"
    echo "  start   - Start the tunnel"
    echo "  stop    - Stop the tunnel"
    echo "  restart - Restart the tunnel (new URL)"
    echo "  status  - Check tunnel status"
    echo "  url     - Show current public URL"
    exit 1
    ;;
esac


#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Cloudflare Tunnel Test Server</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        h1 {{
            color: #333;
        }}
        .status {{
            padding: 20px;
            background-color: #e8f5e8;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Cloudflare Tunnel Test Server</h1>
        <div class="status">
            <h2>✅ Server is Running Successfully</h2>
            <p>This page is being served from localhost:4000</p>
            <p>If you can see this page through Cloudflare Tunnel, the setup is working correctly!</p>
        </div>
        <div class="timestamp">
            <p>Current server time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Path requested: {self.path}</p>
        </div>
        <div>
            <h3>Next Steps:</h3>
            <ol style="text-align: left;">
                <li>Run one of the Cloudflare tunnel scripts:</li>
                <ul>
                    <li><code>./run-tunnel.sh</code> (temporary tunnel)</li>
                    <li><code>./setup-permanent-tunnel.sh</code> (permanent tunnel)</li>
                </ul>
                <li>Access your service through the provided Cloudflare URL</li>
            </ol>
        </div>
    </div>
</body>
</html>
        """
        
        self.wfile.write(html_content.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'success',
            'message': 'POST request received',
            'received_at': datetime.now().isoformat(),
            'data': post_data.decode('utf-8')
        }
        
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    server_address = ('localhost', 4000)
    httpd = HTTPServer(server_address, TestHandler)
    print("Starting test server on http://localhost:4000")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
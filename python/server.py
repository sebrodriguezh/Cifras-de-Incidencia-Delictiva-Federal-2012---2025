#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple HTTP Server for Local Development
Run this script to serve your HTML template on localhost
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def run_server(port=8000):
    """Run a simple HTTP server on the specified port"""
    
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    
    # Change to the current directory
    os.chdir(current_dir)
    
    # Create HTTP server
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"🚀 Server running at http://localhost:{port}")
        print(f"📁 Serving files from: {current_dir}")
        print("🌐 Opening browser automatically...")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Open browser automatically
        webbrowser.open(f'http://localhost:{port}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    # You can change the port here if 8000 is already in use
    PORT = 8000
    
    try:
        run_server(PORT)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print(f"💡 Try a different port or stop the process using port {PORT}")
            print(f"🔧 Alternative: python server.py --port {PORT + 1}")
        else:
            print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

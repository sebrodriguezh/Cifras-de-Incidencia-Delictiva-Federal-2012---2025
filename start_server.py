#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple startup script to run the local server
"""

import sys
import os
import subprocess

# Change to the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)

# Start the HTTP server from the project root
print("🚀 Starting server from project root...")
print(f"📁 Project directory: {project_root}")
print("🌐 Server will be available at: http://localhost:8000")
print("⏹️  Press Ctrl+C to stop the server")

try:
    # Use Python's built-in HTTP server from project root
    subprocess.run([sys.executable, "-m", "http.server", "8000", "--directory", project_root])
except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")

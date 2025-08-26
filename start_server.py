#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple startup script to run the local server
"""

import sys
import os

# Add the python directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))

# Import and run the server
from server import run_server

if __name__ == "__main__":
    run_server()

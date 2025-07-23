#!/usr/bin/env python3
"""
WSGI entry point for Sahayak production deployment
"""

from app.main import app

if __name__ == "__main__":
    app.run() 
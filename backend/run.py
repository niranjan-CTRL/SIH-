#!/usr/bin/env python
"""Startup script for H2S Sentinel backend"""
import os
import sys
import warnings
import asyncio

# Suppress numpy warnings
warnings.filterwarnings('ignore')

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.main import app
import uvicorn

if __name__ == "__main__":
    print("Starting H2S Sentinel API Server on http://127.0.0.1:8000")
    print("Swagger UI: http://127.0.0.1:8000/docs")
    try:
        # Use single process to avoid Windows subprocess issues
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info",
            loop="asyncio"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()


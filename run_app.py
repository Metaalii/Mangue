#!/usr/bin/env python3
"""
Run the Mangue web application

Usage:
    python run_app.py

Then open your browser to: http://localhost:8000
"""

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("🥭 Starting Mangue Ingredient Analysis App")
    print("=" * 60)
    print("\n📍 Open your browser to: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

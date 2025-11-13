#!/usr/bin/env python3
"""
Writers Factory Web Application Launcher

Starts both the FastAPI backend and opens the web interface in your browser.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    print("🚀 Starting Writers Factory Web Application...")
    print("=" * 70)

    # Get paths
    webapp_dir = Path(__file__).parent
    backend_path = webapp_dir / "backend" / "app.py"
    frontend_path = webapp_dir / "frontend" / "index.html"

    # Check if required files exist
    if not backend_path.exists():
        print("❌ Error: Backend not found at", backend_path)
        sys.exit(1)

    if not frontend_path.exists():
        print("❌ Error: Frontend not found at", frontend_path)
        sys.exit(1)

    print(f"✅ Backend: {backend_path}")
    print(f"✅ Frontend: {frontend_path}")
    print()

    # Check for required dependencies
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("❌ Missing dependencies. Installing...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "fastapi", "uvicorn[standard]", "websockets"
        ])
        print("✅ Dependencies installed")
        print()

    # Start the backend server
    print("🔧 Starting FastAPI backend on http://127.0.0.1:8000...")
    backend_process = subprocess.Popen(
        [sys.executable, str(backend_path)],
        cwd=str(webapp_dir.parent),  # Run from writers-factory-core root
    )

    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)

    # Open browser
    frontend_url = f"file://{frontend_path.absolute()}"
    print(f"🌐 Opening web interface: {frontend_url}")
    webbrowser.open(frontend_url)

    print()
    print("=" * 70)
    print("✨ Writers Factory is running!")
    print()
    print("Backend API:  http://127.0.0.1:8000")
    print("Frontend:     (opened in browser)")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)

    try:
        # Keep running until interrupted
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Writers Factory...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()

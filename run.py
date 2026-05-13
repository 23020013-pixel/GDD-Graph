import subprocess
import sys
import time
import os

def run_app():
    print("🚀 Starting Hetionet Explorer...")
    
    # Start Backend
    print("📦 Starting FastAPI Backend (Port 8000)...")
    backend = subprocess.Popen([sys.executable, "-m", "api.main"])
    
    # Give backend some time to start
    time.sleep(2)
    
    # Start Frontend
    print("🎨 Starting Streamlit Frontend (Port 8501)...")
    frontend = subprocess.Popen(["streamlit", "run", "ui/app.py", "--server.port", "8501"])
    
    try:
        while True:
            time.sleep(1)
            if backend.poll() is not None:
                print("❌ Backend stopped unexpectedly.")
                break
            if frontend.poll() is not None:
                print("❌ Frontend stopped unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nStopping application...")
    finally:
        backend.terminate()
        frontend.terminate()
        print("Goodbye!")

if __name__ == "__main__":
    run_app()

#!/usr/bin/env python3
"""
VisionFlow Demo Runner
Automatically starts both backend and frontend servers
"""

import subprocess
import sys
import time
import webbrowser
import os
from threading import Thread

def run_backend():
    """Start Flask backend server"""
    print("🚀 Starting Flask backend server...")
    os.chdir('backend')
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Backend server stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Start React frontend server"""
    print("⚛️ Starting React frontend server...")
    os.chdir('../frontend')
    try:
        subprocess.run(['npm', 'start'], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Frontend server stopped")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    backend_reqs = ['flask', 'openai', 'requests', 'bs4']
    missing_python = []
    
    for req in backend_reqs:
        try:
            __import__(req)
        except ImportError:
            missing_python.append(req)
    
    if missing_python:
        print(f"❌ Missing Python dependencies: {', '.join(missing_python)}")
        print("Run: cd backend && pip install -r requirements.txt")
        return False
    
    # Check Node dependencies
    if not os.path.exists('frontend/node_modules'):
        print("❌ Missing Node.js dependencies")
        print("Run: cd frontend && npm install")
        return False
    
    # Check OpenAI API key
    if not os.getenv('OPENAI_API_KEY') and not os.path.exists('backend/.env'):
        print("⚠️ OpenAI API key not set")
        print("🚀 Running setup assistant...")
        try:
            import subprocess
            result = subprocess.run([sys.executable, 'setup_api_key.py'], cwd=os.getcwd())
            if result.returncode != 0:
                print("❌ Setup assistant failed")
                print("📝 Please manually create backend/.env file with:")
                print("   OPENAI_API_KEY=your_key_here")
                print("   Get your API key from: https://platform.openai.com/account/api-keys")
                return False
        except Exception as e:
            print(f"❌ Could not run setup assistant: {e}")
            return False
        
        # Re-check after setup
        if not os.getenv('OPENAI_API_KEY') and not os.path.exists('backend/.env'):
            print("❌ Setup incomplete - please run again")
            return False
    
    print("✅ All dependencies found!")
    return True

def main():
    """Main demo runner"""
    print("=" * 60)
    print("🤖 VisionFlow: AI Workflow Automation Agent")
    print("=" * 60)
    
    if not check_dependencies():
        print("\n💡 Please install missing dependencies and try again.")
        return
    
    print("\n🎯 Starting VisionFlow demo...")
    print("📡 Backend will run on: http://localhost:5000")
    print("🌐 Frontend will run on: http://localhost:3000")
    print("🚀 Ready to extract data from any webpage!")
    print("\nPress Ctrl+C to stop all servers\n")
    
    # Start backend in background thread
    backend_thread = Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend in background thread
    frontend_thread = Thread(target=run_frontend, daemon=True)
    frontend_thread.start()
    
    # Wait for frontend to start and open browser
    time.sleep(8)
    webbrowser.open('http://localhost:3000')
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down VisionFlow...")
        print("👋 Thanks for trying VisionFlow!")

if __name__ == '__main__':
    main()

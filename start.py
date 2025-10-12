#!/usr/bin/env python3
"""
AI Resume Parser - Startup Script
Run this script to start the application with proper setup
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is suitable"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_env_file():
    """Check if .env file exists and guide user"""
    env_file = Path(".env")
    if not env_file.exists():
        print("\n⚠️  Environment file (.env) not found!")
        print("Please create a .env file with the following configuration:")
        print()
        print("# Copy .env.example to .env and fill in your values:")
        if platform.system() == "Windows":
            print("copy .env.example .env")
        else:
            print("cp .env.example .env")
        print()
        print("Required environment variables:")
        print("- GEMINI_API_KEY: Get from https://makersuite.google.com/app/apikey")
        print("- DATABASE_URL: PostgreSQL connection string")
        print()
        return False
    
    print("✅ Environment file found")
    return True

def check_database():
    """Check database connectivity"""
    try:
        # Try to import database module to check connectivity
        os.chdir("backend")
        import database
        print("✅ Database connection successful")
        os.chdir("..")
        return True
    except Exception as e:
        print(f"⚠️  Database connection issue: {e}")
        print("Make sure PostgreSQL is running and DATABASE_URL is correctly set")
        os.chdir("..")
        return False

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting AI Resume Parser...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🔄 To stop the server, press Ctrl+C")
    print()
    
    try:
        os.chdir("backend")
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
    finally:
        os.chdir("..")

def main():
    """Main startup function"""
    print("🤖 AI Resume Parser - Starting Application")
    print("=" * 50)
    
    # Check system requirements
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check environment configuration
    if not check_env_file():
        print("\n❌ Please configure your environment variables first.")
        return
    
    # Check database
    check_database()  # Non-blocking, just warn user
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()

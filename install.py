#!/usr/bin/env python3
"""
Lab Management System - Easy Installer
This script sets up the LMS application with all dependencies.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_step(step, message):
    print(f"\n{'='*50}")
    print(f"Step {step}: {message}")
    print(f"{'='*50}")

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               capture_output=True, text=True)
        print("✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.output}")
        return False

def check_python():
    """Check if Python is installed and version is compatible"""
    print_step(1, "Checking Python Installation")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} detected - Compatible!")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor} detected")
        print("❌ Please install Python 3.8 or higher from https://python.org")
        return False

def install_dependencies():
    """Install required Python packages from requirements.txt"""
    print_step(2, "Installing Dependencies")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt file not found!")
        print("Please ensure requirements.txt is in the same folder as this installer.")
        return False
    
    print("Installing packages from requirements.txt...")
    if not run_command("pip install -r requirements.txt", "Installing from requirements.txt"):
        print("❌ Failed to install packages from requirements.txt")
        print("You can try installing manually with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed successfully!")
    return True

def create_env_file():
    """Create .env file with default settings"""
    print_step(3, "Creating Configuration File")
    
    env_content = """# Lab Management System Configuration
# You can modify these settings if needed

# Database
DATABASE_URL=sqlite:///./lms.db

# Admin Credentials (Change these!)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Server Settings
HOST=127.0.0.1
PORT=8000

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Configuration file created (.env)")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def setup_database():
    """Initialize the database"""
    print_step(4, "Setting up Database")
    
    try:
        # Import after dependencies are installed
        from database import create_tables
        create_tables()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def create_startup_script():
    """Create a simple startup script"""
    print_step(5, "Creating Startup Script")
    
    if os.name == 'nt':  # Windows
        script_content = """@echo off
echo Starting Lab Management System...
echo.
echo Open your web browser and go to: http://localhost:8000
echo Default login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo.
python main.py
pause
"""
        script_name = "start_lms.bat"
    else:  # Linux/Mac
        script_content = """#!/bin/bash
echo "Starting Lab Management System..."
echo ""
echo "Open your web browser and go to: http://localhost:8000"
echo "Default login: admin / admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python3 main.py
"""
        script_name = "start_lms.sh"
    
    try:
        with open(script_name, 'w') as f:
            f.write(script_content)
        
        # Make executable on Unix systems
        if os.name != 'nt':
            os.chmod(script_name, 0o755)
        
        print(f"✅ Startup script created: {script_name}")
        return True
    except Exception as e:
        print(f"❌ Error creating startup script: {e}")
        return False

def main():
    """Main installation function"""
    print("🏥 Lab Management System - Easy Installer")
    print("This will install and configure the LMS application.")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    # Check Python version
    if not check_python():
        print("\n❌ Installation failed: Python version incompatible")
        input("Press Enter to exit...")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed: Could not install dependencies")
        input("Press Enter to exit...")
        return False
    
    # Create configuration
    if not create_env_file():
        print("\n❌ Installation failed: Could not create configuration")
        input("Press Enter to exit...")
        return False
    
    # Setup database
    if not setup_database():
        print("\n❌ Installation failed: Could not setup database")
        input("Press Enter to exit...")
        return False
    
    # Create startup script
    if not create_startup_script():
        print("\n❌ Installation failed: Could not create startup script")
        input("Press Enter to exit...")
        return False
    
    # Success message
    print("\n" + "="*60)
    print("🎉 INSTALLATION COMPLETED SUCCESSFULLY! 🎉")
    print("="*60)
    print("\nTo start the Lab Management System:")
    
    if os.name == 'nt':  # Windows
        print("1. Double-click 'start_lms.bat'")
    else:  # Linux/Mac
        print("1. Double-click 'start_lms.sh' or run: ./start_lms.sh")
    
    print("2. Open your web browser")
    print("3. Go to: http://localhost:8000")
    print("4. Login with: admin / admin123")
    print("\n⚠️  IMPORTANT: Change the default password after first login!")
    print("\n📁 All files are in this folder, keep them together.")
    print("\nPress Enter to exit...")
    input()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
#!/usr/bin/env python3
"""
PlacifyMe - Main Launcher
Run this file to start the system
"""

import os
import sys

def check_dependencies():
    """Check if required packages are installed"""
    required = ['customtkinter', 'PIL', 'matplotlib', 'pandas']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("Missing dependencies. Installing...")
        for package in missing:
            os.system(f'pip install {package}')
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = ['assets', 'temp', 'temp/uploads', 'temp/documents', 'temp/resumes']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def main():
    """Main entry point"""
    print("🚀 Starting PlacifyMe Placement Management System...")
    
    # Check dependencies
    check_dependencies()
    
    # Setup directories
    setup_directories()
    
    # Check if database exists
    if not os.path.exists('registration_student.db'):
        print("⚠️  Database not found. Running setup...")
        import setup_db
        print("✅ Database setup complete!")
    
    # Import and run enhanced main
    try:
        from common import PlacifyMe
        app = PlacifyMe()
        app.mainloop()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
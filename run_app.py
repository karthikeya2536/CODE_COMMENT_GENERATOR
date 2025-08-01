#!/usr/bin/env python3
"""
Streamlit App Runner for Code Comment Generator
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    print("🚀 Starting Code Comment Generator Streamlit App...")
    print("📱 Opening in your default web browser...")
    print("🔗 The app will be available at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        print("💡 Make sure you have installed the requirements:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main() 
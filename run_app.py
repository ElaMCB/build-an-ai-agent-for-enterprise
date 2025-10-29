"""Quick launcher for the Streamlit app."""

import subprocess
import sys
import os

if __name__ == "__main__":
    # Check if .env exists
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found. Please create one from .env.example")
        print("   Make sure to add your OPENAI_API_KEY")
    
    # Run Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/main.py"])


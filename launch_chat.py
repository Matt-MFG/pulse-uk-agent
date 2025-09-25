"""
Launch PULSE UK Agent Chat Interface
Simple launcher for the web-based chat
"""

import os
import sys
import webbrowser
import time
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Launch the PULSE agent chat interface"""

    print("\n" + "="*60)
    print("PULSE UK Cultural Intelligence Agent")
    print("Web Chat Interface Launcher")
    print("="*60)

    # Check for required packages
    print("\n[CHECK] Verifying dependencies...")

    try:
        import flask
        import flask_cors
        print("[OK] Flask installed")
    except ImportError:
        print("[INFO] Installing Flask...")
        os.system("pip install flask flask-cors -q")

    try:
        import google.generativeai
        print("[OK] Google Generative AI installed")
    except ImportError:
        print("[INFO] Installing google-generativeai...")
        os.system("pip install google-generativeai -q")

    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()

    if not os.getenv("GEMINI_API_KEY"):
        print("\n[ERROR] GEMINI_API_KEY not found!")
        print("Please add it to your .env file:")
        print("GEMINI_API_KEY=your_api_key_here")
        return

    print("[OK] API key configured")

    # Launch the web interface
    print("\n[LAUNCH] Starting PULSE web chat...")
    print("="*60)
    print("The chat interface will open in your browser")
    print("URL: http://localhost:8080")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")

    # Wait a moment then open browser
    time.sleep(2)
    webbrowser.open("http://localhost:8080")

    # Start the Flask server
    from web_chat import app, initialize

    if initialize():
        app.run(host='localhost', port=8080, debug=False, use_reloader=False)
    else:
        print("[ERROR] Failed to initialize agent")


if __name__ == "__main__":
    main()
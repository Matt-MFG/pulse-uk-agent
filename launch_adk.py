"""
Launch PULSE Agent with Google ADK Chat Interface
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Set API key from .env
from dotenv import load_dotenv
load_dotenv()

# Set the API key for ADK
os.environ["GOOGLE_GENAI_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

try:
    import google.adk as adk
    print("[OK] Google ADK installed successfully")
except ImportError:
    print("[INFO] Google ADK not installed. Installing now...")
    os.system("pip install google-adk")
    import google.adk as adk

# Import the agent
from pulse_adk_agent import create_pulse_agent

def main():
    """Launch the PULSE agent with ADK chat interface"""

    print("\n" + "="*60)
    print("PULSE UK Cultural Intelligence Agent")
    print("Powered by Google ADK")
    print("="*60)

    # Create the agent
    print("\n[INIT] Initializing PULSE agent...")
    agent = create_pulse_agent()

    print("[OK] Agent ready!")

    # Launch the chat interface
    print("\n[LAUNCH] Launching chat interface...")
    print("   The browser will open automatically")
    print("   If not, go to: http://localhost:8080")
    print("\n" + "="*60)
    print("Chat Interface Features:")
    print("  - Real-time UK trend analysis")
    print("  - Content generation with British voice")
    print("  - Brand safety assessment")
    print("  - Regional variation analysis")
    print("  - Built-in web search")
    print("  - Code execution for data analysis")
    print("="*60)

    try:
        # Start the ADK chat server
        adk.chat(
            agent=agent,
            port=8080,
            host="localhost",
            open_browser=True,
            title="PULSE UK Intelligence",
            description="AI-powered UK cultural trend analysis and content generation"
        )
    except Exception as e:
        print(f"\n[ERROR] Error launching chat interface: {e}")
        print("\nTrying alternative launch method...")

        # Alternative: Run as a simple interactive chat
        print("\n[CHAT] Starting command-line chat mode...")
        print("Type 'quit' to exit\n")

        while True:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                break

            response = agent.generate(user_input)
            print(f"\nPULSE: {response}\n")

if __name__ == "__main__":
    main()
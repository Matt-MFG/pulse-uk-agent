"""
PULSE UK Agent using Google ADK
Simple implementation that works with the ADK interface
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Since google-adk is still in development, we'll use the Gemini API directly
# with a structure that matches ADK patterns

import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create model with UK focus
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "max_output_tokens": 8192,
    },
    system_instruction="""You are PULSE, a UK cultural intelligence agent.

CAPABILITIES:
- Analyze UK cultural trends across social media, news, and entertainment
- Understand British humor, regional variations, and generational differences
- Generate authentic UK content with British spelling and idioms
- Assess brand safety for UK market (ASA, Ofcom compliance)

UK CONTEXT:
- Regions: England (London, North, South), Scotland, Wales, Northern Ireland
- Cultural touchpoints: NHS, BBC, Premier League, Royal Family, weather, tea, pubs
- Humor: Self-deprecating, dry wit, irony, understatement
- Current issues: Cost of living, regional inequalities

ALWAYS:
- Use British spelling (colour, favourite, realise)
- Reference UK-specific elements
- Consider regional variations
- Provide confidence scores
- Include timing in GMT/BST"""
)

def chat_with_pulse():
    """Simple chat interface with PULSE agent"""

    print("\n" + "="*60)
    print("PULSE UK Cultural Intelligence Agent")
    print("Chat Interface (Type 'quit' to exit)")
    print("="*60)
    print("\nHello! I'm PULSE, your UK cultural intelligence agent.")
    print("Ask me about UK trends, content generation, or brand safety.\n")

    # Start chat session
    chat = model.start_chat(history=[])

    while True:
        # Get user input
        user_input = input("\nYou: ")

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nPULSE: Cheerio! Happy to help with UK cultural intelligence anytime.")
            break

        try:
            # Generate response
            response = chat.send_message(user_input)
            print(f"\nPULSE: {response.text}")

        except Exception as e:
            print(f"\n[ERROR] {e}")
            print("Please try again with a different question.")

def main():
    """Main entry point"""

    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("[ERROR] GEMINI_API_KEY not found in environment")
        print("Please set it in your .env file")
        return

    # Run chat interface
    chat_with_pulse()

if __name__ == "__main__":
    main()
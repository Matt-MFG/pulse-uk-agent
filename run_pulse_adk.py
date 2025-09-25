"""
Launch PULSE UK Agent with Google ADK Chat Interface
"""

import os
from dotenv import load_dotenv
from google.adk import Agent, Runner
from google.adk.tools import Tool
import google.generativeai as genai

# Load environment
load_dotenv()

# Configure Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

genai.configure(api_key=api_key)

# Create PULSE UK Agent
class PulseUKAgent(Agent):
    """UK Cultural Intelligence Agent"""

    def __init__(self):
        super().__init__(
            name="PULSE UK Intelligence",
            model="gemini-2.0-flash-exp",
            system_prompt="""You are PULSE, an advanced UK cultural intelligence agent.

Your expertise:
- Identifying emerging UK cultural trends across social media, news, and entertainment
- Understanding British humor, regional variations (England, Scotland, Wales, NI), and generational differences
- Creating authentic UK content with proper British spelling, idioms, and cultural references
- Assessing brand safety considering UK regulations (ASA, Ofcom) and cultural sensitivities
- Analyzing regional variations across London, Manchester, Birmingham, Glasgow, Edinburgh, Cardiff, Belfast

UK Context to Consider:
- Cultural touchpoints: NHS, BBC, Premier League, Royal Family, British weather, tea culture, pub culture
- Humor style: Self-deprecating, dry wit, irony, understatement, sarcasm
- Current sensitivities: Cost of living crisis, regional inequalities, Brexit aftermath
- British expressions: "Brilliant", "Cheeky", "Proper", "Taking the piss", "Having a laugh"

Always provide structured analysis with:
- Confidence scores (0-100)
- Regional variations
- Generational appeal
- Brand safety assessment
- Optimal timing (GMT/BST)
- Platform-specific recommendations"""
        )

    def analyze_uk_trends(self, query: str = None) -> str:
        """Analyze current UK cultural trends"""
        if not query:
            query = "What are the current UK cultural trends today?"

        response = self.model.generate_content(f"""
        Analyze UK cultural trends:
        Query: {query}

        Provide analysis including:
        - Top 5 emerging trends with velocity scores
        - Best brand participation opportunities
        - Regional variations across UK
        - Risk assessment for brands
        - Content recommendations
        """)
        return response.text

    def generate_uk_content(self, trend: str, platform: str = "twitter") -> str:
        """Generate UK-optimized content"""
        response = self.model.generate_content(f"""
        Create authentic UK content:
        Trend: {trend}
        Platform: {platform}

        Requirements:
        1. Use British spelling
        2. Include British idioms
        3. Reference UK-specific cultural elements
        4. Use appropriate British humor

        Generate main content, hashtags, and optimal posting time.
        """)
        return response.text


def main():
    """Launch PULSE agent with ADK interface"""

    print("\n" + "="*60)
    print("PULSE UK Cultural Intelligence Agent")
    print("Powered by Google ADK")
    print("="*60)

    # Create agent instance
    agent = PulseUKAgent()

    # Create runner for the agent
    runner = Runner(agent)

    print("\n[INFO] Starting ADK chat interface...")
    print("[INFO] The interface should open in your browser")
    print("[INFO] If not, navigate to: http://localhost:8000")

    try:
        # Run the agent with web interface
        runner.run(
            host="localhost",
            port=8000,
            reload=False,
            open_browser=True
        )
    except Exception as e:
        print(f"\n[ERROR] Failed to start ADK interface: {e}")
        print("\n[FALLBACK] Starting command-line chat...")

        # Fallback to simple chat
        print("\nChat with PULSE (type 'quit' to exit):\n")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                break

            if 'trend' in user_input.lower():
                response = agent.analyze_uk_trends(user_input)
            elif 'content' in user_input.lower():
                response = agent.generate_uk_content(user_input)
            else:
                # General query
                response = agent.model.generate_content(user_input).text

            print(f"\nPULSE: {response}\n")


if __name__ == "__main__":
    main()
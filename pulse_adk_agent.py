"""
PULSE UK Cultural Intelligence Agent using Google ADK
This creates an agent with built-in tools and chat interface
"""

import os
from google import adk
from google.adk import agents
from google.adk.tools import Tool
from typing import Dict, List, Any
import google.generativeai as genai

# Configure your API key
os.environ["GOOGLE_GENAI_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

# Create the PULSE agent using ADK
class PulseUKAgent(agents.Agent):
    """UK Cultural Intelligence Agent with ADK"""

    def __init__(self):
        super().__init__(
            name="PULSE UK Cultural Intelligence",
            description="Analyzes UK cultural trends and generates brand content",
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
- Platform-specific recommendations""",
            tools=[
                # Built-in ADK tools
                "search",  # Web search for real-time trends
                "code_execution",  # For data analysis
                "file_handling"  # For reports
            ]
        )

    def analyze_uk_trends(self, query: str = None) -> Dict[str, Any]:
        """Analyze current UK cultural trends"""

        if not query:
            query = "What are the current UK cultural trends today?"

        prompt = f"""Analyze UK cultural trends:

Query: {query}

Use web search to find:
1. Current UK trending topics on social media
2. UK news headlines
3. Popular UK entertainment (TV, music, sports)
4. Viral UK memes or cultural moments

Provide analysis including:
- Top 5 emerging trends with velocity scores
- Best brand participation opportunities
- Regional variations across UK
- Risk assessment for brands
- Content recommendations

Format as structured JSON."""

        return self.generate(prompt)

    def generate_uk_content(
        self,
        trend: str,
        platform: str = "twitter",
        brand_voice: str = "professional yet approachable"
    ) -> str:
        """Generate UK-optimized content for a trend"""

        prompt = f"""Create authentic UK content:

Trend: {trend}
Platform: {platform}
Brand Voice: {brand_voice}

Requirements:
1. Use British spelling (colour, favourite, realise)
2. Include British idioms and expressions
3. Reference UK-specific cultural elements
4. Consider regional variations if relevant
5. Use appropriate British humor
6. Include UK timezone (GMT/BST)

Generate:
- Main content/copy
- Hashtags (UK-relevant)
- Optimal posting time
- Regional variations (if needed)
- Expected engagement level"""

        return self.generate(prompt)

    def assess_brand_safety(self, content: str) -> Dict[str, Any]:
        """Assess brand safety for UK market"""

        prompt = f"""Assess brand safety for UK market:

Content/Trend: {content}

Check against:
1. ASA (Advertising Standards Authority) guidelines
2. Ofcom broadcasting standards
3. UK cultural sensitivities
4. Political neutrality (Brexit, Scottish independence, etc.)
5. Regional considerations
6. Class dynamics
7. Current UK news context

Provide:
- Overall safety score (0-100)
- Specific risks identified
- Mitigation strategies
- Go/No-go recommendation
- Alternative approaches if risky

Return as JSON with detailed analysis."""

        return self.generate(prompt)

    def analyze_regional_variations(self, trend: str) -> Dict[str, Any]:
        """Analyze how trends vary across UK regions"""

        regions = [
            "London",
            "Manchester/North England",
            "Birmingham/Midlands",
            "Scotland (Glasgow/Edinburgh)",
            "Wales (Cardiff)",
            "Northern Ireland (Belfast)"
        ]

        prompt = f"""Analyze regional variations for trend: {trend}

For each UK region {regions}, assess:
1. Trend relevance/strength (0-100)
2. Local cultural context
3. Regional language/slang differences
4. Content adaptation needs
5. Local influencers or media
6. Optimal timing for region

Also identify:
- Which region is leading the trend
- Cross-regional opportunities
- Regional risks or sensitivities

Format as detailed JSON."""

        return self.generate(prompt)

# Create and configure the agent
def create_pulse_agent():
    """Create and return configured PULSE agent"""

    # Initialize the agent
    agent = PulseUKAgent()

    # Add custom tools if needed
    agent.add_tool(
        Tool(
            name="uk_news_check",
            description="Check latest UK news headlines",
            function=lambda: agent.search("UK news today BBC Guardian")
        )
    )

    agent.add_tool(
        Tool(
            name="trending_check",
            description="Check UK trending topics",
            function=lambda: agent.search("UK trending Twitter TikTok today")
        )
    )

    return agent

# Main execution
if __name__ == "__main__":
    # Create the agent
    pulse_agent = create_pulse_agent()

    # Launch the ADK chat interface
    print("Launching PULSE UK Cultural Intelligence Agent...")
    print("=" * 60)

    # Start the interactive chat
    adk.chat(
        agent=pulse_agent,
        port=8080,  # Local port for chat interface
        open_browser=True  # Automatically open browser
    )

    # The chat interface will now be available at http://localhost:8080
    # It provides:
    # - Interactive chat with the agent
    # - Built-in search capabilities
    # - Code execution for analysis
    # - File handling for reports
    # - Beautiful UI like in the GIF you showed
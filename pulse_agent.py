"""
PULSE UK Cultural Intelligence Agent
Works with Gemini API directly for chat functionality
"""

import os
import json
from typing import Dict, List, Any
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class PulseUKAgent:
    """UK Cultural Intelligence Agent using Gemini"""

    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "max_output_tokens": 8192,
            },
            system_instruction="""You are PULSE, an advanced UK cultural intelligence agent.

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
        self.chat = self.model.start_chat(history=[])

    def analyze_uk_trends(self, query: str = None) -> Dict[str, Any]:
        """Analyze current UK cultural trends"""

        if not query:
            query = "What are the current UK cultural trends today?"

        prompt = f"""Analyze UK cultural trends:

Query: {query}

Provide analysis including:
1. Top 5 emerging trends with velocity scores
2. Best brand participation opportunities
3. Regional variations across UK
4. Risk assessment for brands
5. Content recommendations

Format as structured JSON."""

        response = self.chat.send_message(prompt)
        try:
            return json.loads(response.text)
        except:
            return {"response": response.text}

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

        response = self.chat.send_message(prompt)
        return response.text

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

        response = self.chat.send_message(prompt)
        try:
            return json.loads(response.text)
        except:
            return {"response": response.text}

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

        response = self.chat.send_message(prompt)
        try:
            return json.loads(response.text)
        except:
            return {"response": response.text}

    def process_query(self, query: str) -> str:
        """Process a general query"""
        response = self.chat.send_message(query)
        return response.text


def main():
    """Main entry point for testing"""

    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("[ERROR] GEMINI_API_KEY not found in environment")
        print("Please set it in your .env file")
        return

    # Create agent
    agent = PulseUKAgent()

    print("\n" + "="*60)
    print("PULSE UK Cultural Intelligence Agent")
    print("="*60)
    print("\nAgent initialized successfully!")

    # Example usage
    print("\nExample: Analyzing current UK trends...")
    trends = agent.analyze_uk_trends("What UK social media trends are happening today?")
    print(json.dumps(trends, indent=2) if isinstance(trends, dict) else trends)


if __name__ == "__main__":
    main()
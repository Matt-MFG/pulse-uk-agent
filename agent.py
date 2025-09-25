"""
PULSE Cultural Intelligence Agent for Google ADK
This agent analyzes UK cultural trends and generates brand content opportunities
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from google.generativeai import protos

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class PulseAgent:
    """UK Cultural Intelligence Agent"""

    def __init__(self):
        """Initialize the PULSE agent with UK-focused configuration"""

        # System instruction for UK cultural intelligence
        self.system_instruction = """You are PULSE, an advanced UK cultural intelligence agent.

Your expertise includes:
1. Identifying emerging UK cultural trends across social media, news, and entertainment
2. Understanding British humor, regional variations, and generational differences
3. Spotting authentic brand participation opportunities in cultural conversations
4. Creating UK-appropriate content with proper tone, language, and cultural references
5. Evaluating brand safety considering UK regulations (ASA, Ofcom) and sensitivities

UK Context:
- Regions: England (London, North, South), Scotland, Wales, Northern Ireland
- Cultural touchpoints: NHS, BBC, Premier League, Royal Family, tea culture, weather
- Humor: Self-deprecating, dry wit, irony, understatement
- Current sensitivities: Cost of living, regional inequalities, political divisions

Always provide structured analysis with confidence scores and actionable recommendations."""

        # Initialize Gemini model
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "application/json",
            },
            system_instruction=self.system_instruction
        )

        # Tools configuration
        self.tools = self._configure_tools()

    def _configure_tools(self) -> List[protos.Tool]:
        """Configure agent tools for UK trend analysis"""

        analyze_trends_func = protos.FunctionDeclaration(
            name="analyze_uk_trends",
            description="Analyze UK cultural trends from various data sources",
            parameters=protos.Schema(
                type=protos.Type.OBJECT,
                properties={
                    "data_sources": protos.Schema(
                        type=protos.Type.ARRAY,
                        description="List of data sources to analyze",
                        items=protos.Schema(type=protos.Type.STRING)
                    ),
                    "time_window": protos.Schema(
                        type=protos.Type.STRING,
                        description="Time period to analyze (e.g., 'last 24 hours')"
                    ),
                    "focus_areas": protos.Schema(
                        type=protos.Type.ARRAY,
                        description="Areas to focus on (humor, politics, entertainment)",
                        items=protos.Schema(type=protos.Type.STRING)
                    )
                },
                required=["data_sources"]
            )
        )

        generate_content_func = protos.FunctionDeclaration(
            name="generate_uk_content",
            description="Generate UK-optimized social media content",
            parameters=protos.Schema(
                type=protos.Type.OBJECT,
                properties={
                    "trend": protos.Schema(
                        type=protos.Type.STRING,
                        description="The trend to create content about"
                    ),
                    "platform": protos.Schema(
                        type=protos.Type.STRING,
                        description="Target platform (twitter, instagram, tiktok, linkedin)"
                    ),
                    "brand_voice": protos.Schema(
                        type=protos.Type.STRING,
                        description="Brand personality and tone"
                    )
                },
                required=["trend", "platform"]
            )
        )

        assess_safety_func = protos.FunctionDeclaration(
            name="assess_brand_safety",
            description="Evaluate brand safety for UK market",
            parameters=protos.Schema(
                type=protos.Type.OBJECT,
                properties={
                    "content": protos.Schema(
                        type=protos.Type.STRING,
                        description="Content or trend to assess"
                    ),
                    "brand_values": protos.Schema(
                        type=protos.Type.ARRAY,
                        description="Brand values and guidelines",
                        items=protos.Schema(type=protos.Type.STRING)
                    )
                },
                required=["content"]
            )
        )

        regional_analysis_func = protos.FunctionDeclaration(
            name="analyze_uk_regions",
            description="Analyze how trends vary across UK regions",
            parameters=protos.Schema(
                type=protos.Type.OBJECT,
                properties={
                    "trend": protos.Schema(
                        type=protos.Type.STRING,
                        description="The trend to analyze"
                    ),
                    "regions": protos.Schema(
                        type=protos.Type.ARRAY,
                        description="UK regions to compare",
                        items=protos.Schema(type=protos.Type.STRING)
                    )
                },
                required=["trend"]
            )
        )

        return [protos.Tool(
            function_declarations=[
                analyze_trends_func,
                generate_content_func,
                assess_safety_func,
                regional_analysis_func
            ]
        )]

    async def analyze_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze UK cultural trends"""

        prompt = f"""Analyze these UK cultural trends and provide comprehensive insights:

Data: {json.dumps(data, indent=2)}

Provide analysis including:
1. Top 5 emerging trends with velocity scores
2. Best brand participation opportunities
3. Regional variations across UK
4. Generational appeal differences
5. Content recommendations for each trend
6. Risk assessment and brand safety scores
7. Optimal timing for engagement

Format as structured JSON."""

        response = self.model.generate_content(prompt)
        return json.loads(response.text)

    async def generate_content(
        self,
        trend: str,
        platform: str,
        brand_voice: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate UK-optimized content for a specific trend and platform"""

        prompt = f"""Create authentic UK content for this trend:

Trend: {trend}
Platform: {platform}
Brand Voice: {brand_voice or "Professional yet approachable"}

Generate content that:
1. Uses British spelling and idioms
2. Includes regional references if relevant
3. Matches platform best practices
4. Avoids American terminology
5. Considers UK timezone (GMT/BST)

Include:
- Main content/copy
- Hashtags (UK-relevant)
- Visual description (if applicable)
- Optimal posting time (UK time)
- Expected engagement level
- Regional variations (if needed)

Format as JSON."""

        response = self.model.generate_content(prompt)
        return json.loads(response.text)

    async def assess_brand_safety(
        self,
        content: str,
        brand_values: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Assess brand safety for UK market"""

        prompt = f"""Evaluate brand safety for UK market:

Content/Trend: {content}
Brand Values: {brand_values or ["Professional", "Inclusive", "Authentic"]}

Assess against:
1. ASA advertising standards
2. Ofcom broadcasting guidelines
3. UK cultural sensitivities
4. Political neutrality requirements
5. Regional considerations
6. Class dynamics
7. Current UK news context

Provide:
- Overall safety score (0-100)
- Specific risks identified
- Mitigation strategies
- Go/No-go recommendation
- Alternative approaches if risky

Format as JSON."""

        response = self.model.generate_content(prompt)
        return json.loads(response.text)

    async def analyze_regions(
        self,
        trend: str,
        regions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze trend variations across UK regions"""

        uk_regions = regions or ["London", "North England", "Scotland", "Wales", "Northern Ireland"]

        prompt = f"""Analyze how this trend varies across UK regions:

Trend: {trend}
Regions: {json.dumps(uk_regions)}

For each region, provide:
1. Trend strength/relevance (0-100)
2. Local cultural context
3. Regional language/terminology differences
4. Content adaptation suggestions
5. Timing considerations
6. Local influencers or media

Also identify:
- Which region is leading the trend
- Regional conflicts or sensitivities
- Cross-regional appeal opportunities

Format as JSON."""

        response = self.model.generate_content(prompt)
        return json.loads(response.text)

    async def run_workflow(self, query: str) -> Dict[str, Any]:
        """Run the complete PULSE workflow"""

        # Start with user query
        workflow_prompt = f"""As PULSE, the UK cultural intelligence agent, help with this request:

{query}

Execute the appropriate workflow:
1. If asking about trends -> Analyze current UK cultural trends
2. If asking for content -> Generate UK-optimized content
3. If asking about safety -> Assess brand safety
4. If asking about regions -> Analyze regional variations

Provide comprehensive, actionable insights formatted as JSON."""

        response = self.model.generate_content(workflow_prompt)

        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"response": response.text}


# ADK Entry Points
def initialize() -> PulseAgent:
    """Initialize the PULSE agent for ADK"""
    return PulseAgent()

async def process_message(agent: PulseAgent, message: str) -> Dict[str, Any]:
    """Process incoming messages through the agent"""
    return await agent.run_workflow(message)

async def analyze_trends(agent: PulseAgent, data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze UK cultural trends"""
    return await agent.analyze_trends(data)

async def generate_content(
    agent: PulseAgent,
    trend: str,
    platform: str,
    brand_voice: Optional[str] = None
) -> Dict[str, Any]:
    """Generate UK-optimized content"""
    return await agent.generate_content(trend, platform, brand_voice)

async def assess_safety(
    agent: PulseAgent,
    content: str,
    brand_values: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Assess brand safety for UK market"""
    return await agent.assess_brand_safety(content, brand_values)

async def analyze_regions(
    agent: PulseAgent,
    trend: str,
    regions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Analyze regional variations"""
    return await agent.analyze_regions(trend, regions)
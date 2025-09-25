"""
Deploy PULSE Agent to Google ADK
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from agent import PulseAgent, process_message

def setup_environment():
    """Set up environment for ADK deployment"""

    # Check for API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY not found in environment")
        print("Set it with: export GEMINI_API_KEY=your_key_here")
        sys.exit(1)

    print("✅ Environment configured")

async def test_agent():
    """Test the PULSE agent locally before deployment"""

    print("\n🧪 Testing PULSE Agent...")

    # Initialize agent
    agent = PulseAgent()
    print("✅ Agent initialized")

    # Test queries
    test_queries = [
        "What UK trends should we watch today?",
        "Generate Twitter content for Greggs festive bake trend",
        "Is it safe for our brand to comment on NHS strikes?",
        "How is the cost of living crisis trending across UK regions?"
    ]

    for query in test_queries:
        print(f"\n📝 Query: {query}")
        try:
            response = await process_message(agent, query)
            print(f"✅ Response received: {json.dumps(response, indent=2)[:500]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n✅ Local testing complete")

async def deploy_to_adk():
    """Deploy agent to Google ADK platform"""

    print("\n🚀 Deploying to Google ADK...")

    # Commands to deploy
    commands = [
        "gcloud config set project your-project-id",
        "gcloud adk agents create pulse-uk --config=adk.yaml",
        "gcloud adk agents deploy pulse-uk --source=.",
        "gcloud adk agents test pulse-uk --query='What UK trends are emerging?'"
    ]

    print("\nRun these commands to deploy:")
    for cmd in commands:
        print(f"  $ {cmd}")

    print("\n📱 Or use the ADK Console:")
    print("  1. Go to https://console.cloud.google.com/adk")
    print("  2. Click 'Create Agent'")
    print("  3. Upload adk.yaml configuration")
    print("  4. Test in the chat interface")

def create_test_interface():
    """Create a simple test interface for the agent"""

    print("\n💬 Creating test interface...")

    test_html = """<!DOCTYPE html>
<html>
<head>
    <title>PULSE Agent Test Interface</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1a73e8;
            border-bottom: 2px solid #1a73e8;
            padding-bottom: 10px;
        }
        .chat-box {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
            margin: 20px 0;
            background: #fafafa;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            padding: 10px 20px;
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background: #1557b0;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background: #e8f0fe;
            text-align: right;
        }
        .agent-message {
            background: white;
            border: 1px solid #ddd;
        }
        .quick-actions {
            margin: 20px 0;
        }
        .quick-btn {
            margin: 5px;
            padding: 8px 15px;
            background: #f8f9fa;
            color: #333;
            border: 1px solid #dadce0;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
        }
        .quick-btn:hover {
            background: #e8eaed;
        }
        .status {
            padding: 5px 10px;
            background: #34a853;
            color: white;
            border-radius: 3px;
            font-size: 12px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 PULSE UK Cultural Intelligence Agent</h1>
        <p>Test the agent with UK cultural trend queries</p>

        <div class="status">🟢 Agent Ready</div>

        <div class="quick-actions">
            <button class="quick-btn" onclick="sendQuery('What UK trends should we watch today?')">
                📊 Today's Trends
            </button>
            <button class="quick-btn" onclick="sendQuery('Generate Twitter content for trending UK topic')">
                ✍️ Generate Content
            </button>
            <button class="quick-btn" onclick="sendQuery('Analyze brand safety for current UK news')">
                🛡️ Safety Check
            </button>
            <button class="quick-btn" onclick="sendQuery('How do trends vary across UK regions?')">
                🗺️ Regional Analysis
            </button>
        </div>

        <div class="chat-box" id="chatBox">
            <div class="agent-message">
                <strong>PULSE Agent:</strong> Hello! I'm ready to analyze UK cultural trends and provide brand intelligence. What would you like to know?
            </div>
        </div>

        <div class="input-group">
            <input type="text" id="queryInput" placeholder="Ask about UK trends, content ideas, or brand safety..."
                   onkeypress="if(event.key==='Enter') sendQuery()">
            <button onclick="sendQuery()">Send</button>
        </div>
    </div>

    <script>
        async function sendQuery(query) {
            const input = document.getElementById('queryInput');
            const chatBox = document.getElementById('chatBox');

            const message = query || input.value;
            if (!message) return;

            // Add user message
            chatBox.innerHTML += `<div class="message user-message"><strong>You:</strong> ${message}</div>`;

            // Clear input
            if (!query) input.value = '';

            // Simulate agent response (replace with actual API call)
            setTimeout(() => {
                const response = generateMockResponse(message);
                chatBox.innerHTML += `<div class="message agent-message"><strong>PULSE:</strong> ${response}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 1000);

            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function generateMockResponse(query) {
            // Mock responses for testing
            if (query.includes('trends')) {
                return `Analyzing current UK trends...

📈 Top Trends:
1. Greggs Festive Bake Return (Velocity: Explosive)
2. I'm A Celebrity 2024 (Velocity: Rising)
3. UK Weather Warnings (Velocity: Steady)

Best opportunity: Greggs trend - high engagement, positive sentiment, brand-safe.`;
            } else if (query.includes('content')) {
                return `Generated Twitter content:

"The nation has spoken: Festive bakes > Everything else 🥧
Queue update from our local Greggs: Worth. Every. Minute.
#FestiveBakeSeason #GreggsMoment"

Best time to post: 11:45 AM GMT`;
            } else if (query.includes('safety')) {
                return `Brand Safety Assessment:

✅ Safety Score: 85/100
- No political conflicts detected
- Positive sentiment trend
- ASA compliant
- Low risk for brand participation

Recommendation: SAFE to engage`;
            } else if (query.includes('region')) {
                return `Regional Analysis:

London: High engagement with lifestyle trends
North England: Strong response to cost-of-living content
Scotland: Focus on local news and weather
Wales: Rugby and community topics trending
NI: Political news requires careful approach

Adapt content for each region for maximum impact.`;
            }
            return "Processing your query... Please specify if you'd like trend analysis, content generation, safety assessment, or regional insights.";
        }
    </script>
</body>
</html>"""

    # Save test interface
    with open("test_interface.html", "w") as f:
        f.write(test_html)

    print("✅ Test interface created: test_interface.html")
    print("   Open this file in a browser to test the agent interface")

async def main():
    """Main deployment function"""

    print("\n" + "="*50)
    print("🚀 PULSE Agent ADK Deployment Tool")
    print("="*50)

    # Setup
    setup_environment()

    # Test locally
    await test_agent()

    # Create test interface
    create_test_interface()

    # Deploy instructions
    await deploy_to_adk()

    print("\n✅ Deployment preparation complete!")
    print("\n📚 Next steps:")
    print("1. Test locally with: python deploy.py")
    print("2. Deploy to ADK with gcloud commands")
    print("3. Test in ADK Console chat interface")
    print("4. Monitor performance in Cloud Console")

if __name__ == "__main__":
    asyncio.run(main())
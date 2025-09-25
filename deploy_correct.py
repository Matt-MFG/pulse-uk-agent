"""
Deploy PULSE Agent using Google's Gemini API
Since ADK CLI doesn't exist, we'll use direct Gemini API integration
"""

import os
import sys
import json
import asyncio
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PulseAgentDeployment:
    """Deploy and test PULSE agent with Gemini"""

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("[ERROR] GEMINI_API_KEY not found in .env file")
            sys.exit(1)

        genai.configure(api_key=self.api_key)
        print("[OK] Gemini API configured")

    async def test_agent_locally(self):
        """Test the agent with Gemini API directly"""

        print("\n[TEST] Testing PULSE Agent with Gemini API...")

        # Initialize model with UK focus
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "max_output_tokens": 8192,
            },
            system_instruction="""You are PULSE, a UK cultural intelligence agent.
            Analyze UK trends, generate British content, and provide brand safety assessments.
            Always consider regional variations and British cultural context."""
        )

        # Test queries
        test_queries = [
            {
                "name": "Trend Analysis",
                "query": "What are the top 3 UK cultural trends today? Include social media trends, news, and entertainment. Format as JSON with trend name, velocity, and opportunity score."
            },
            {
                "name": "Content Generation",
                "query": "Generate a Twitter post about Greggs festive bake returning. Use British humor and include hashtags."
            },
            {
                "name": "Brand Safety",
                "query": "Assess brand safety for commenting on NHS staff strikes. Consider UK sensitivities and ASA guidelines."
            },
            {
                "name": "Regional Analysis",
                "query": "How does the cost of living crisis trend differently across London, Manchester, and Scotland?"
            }
        ]

        for test in test_queries:
            print(f"\n[TEST] {test['name']}")
            print(f"   Query: {test['query'][:100]}...")

            try:
                response = model.generate_content(test['query'])
                print(f"[OK] Response:")
                print(f"   {response.text[:300]}...")
            except Exception as e:
                print(f"[ERROR] {e}")

        print("\n[DONE] Local testing complete")

    def create_cloud_function(self):
        """Generate Cloud Function code for the agent"""

        cloud_function_code = '''import functions_framework
import google.generativeai as genai
import json
import os

# Configure Gemini
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

@functions_framework.http
def pulse_agent(request):
    """PULSE UK Cultural Intelligence Agent Cloud Function"""

    # Parse request
    request_json = request.get_json(silent=True)
    if not request_json or 'query' not in request_json:
        return json.dumps({'error': 'No query provided'}), 400

    query = request_json['query']

    # Initialize model
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        system_instruction="""You are PULSE, a UK cultural intelligence agent.
        Analyze UK trends, generate content, assess brand safety.
        Focus on British culture, humor, and regional variations."""
    )

    try:
        # Generate response
        response = model.generate_content(query)

        return json.dumps({
            'status': 'success',
            'response': response.text,
            'query': query
        })

    except Exception as e:
        return json.dumps({
            'status': 'error',
            'error': str(e)
        }), 500
'''

        # Save Cloud Function code
        with open("main.py", "w") as f:
            f.write(cloud_function_code)

        # Create requirements.txt for Cloud Function
        requirements = """google-generativeai==0.8.3
functions-framework==3.*"""

        with open("requirements.txt", "w") as f:
            f.write(requirements)

        print("\n[CLOUD] Cloud Function files created:")
        print("   - main.py (function code)")
        print("   - requirements.txt (dependencies)")

    def generate_deployment_commands(self):
        """Generate the correct deployment commands"""

        print("\n[DEPLOY] Deployment Options:")

        print("\n1. Deploy as Cloud Function:")
        print("   ```")
        print("   gcloud functions deploy pulse-agent \\")
        print("     --runtime python312 \\")
        print("     --trigger-http \\")
        print("     --allow-unauthenticated \\")
        print("     --entry-point pulse_agent \\")
        print("     --region europe-west2 \\")
        print("     --set-env-vars GEMINI_API_KEY=your_key_here")
        print("   ```")

        print("\n2. Deploy as Cloud Run Service:")
        print("   ```")
        print("   # Build container")
        print("   gcloud builds submit --tag gcr.io/mfg-open-apps/pulse-agent")
        print("   ")
        print("   # Deploy to Cloud Run")
        print("   gcloud run deploy pulse-agent \\")
        print("     --image gcr.io/mfg-open-apps/pulse-agent \\")
        print("     --platform managed \\")
        print("     --region europe-west2 \\")
        print("     --allow-unauthenticated \\")
        print("     --set-env-vars GEMINI_API_KEY=your_key_here")
        print("   ```")

        print("\n3. Use Vertex AI Agent Builder (Recommended):")
        print("   1. Go to: https://console.cloud.google.com/vertex-ai/agent-builder")
        print("   2. Click 'Create Agent'")
        print("   3. Choose 'Conversational Agent'")
        print("   4. Select 'Gemini 2.0 Flash'")
        print("   5. Paste the system instruction from agent.py")
        print("   6. Test in the console")

        print("\n4. Use AI Studio for Testing:")
        print("   1. Go to: https://aistudio.google.com/")
        print("   2. Create new prompt")
        print("   3. Select Gemini 2.0 Flash")
        print("   4. Add system instructions")
        print("   5. Test with UK trend queries")

    def create_dockerfile(self):
        """Create Dockerfile for Cloud Run deployment"""

        dockerfile = """FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080

# Run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app"""

        with open("Dockerfile", "w") as f:
            f.write(dockerfile)

        # Create Flask app for Cloud Run
        flask_app = """from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# Initialize model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction=\"\"\"You are PULSE, a UK cultural intelligence agent.
    Analyze UK trends, generate content, assess brand safety.
    Focus on British culture, humor, and regional variations.\"\"\"
)

@app.route('/')
def index():
    return jsonify({
        'name': 'PULSE UK Cultural Intelligence Agent',
        'version': '1.0.0',
        'endpoints': {
            '/analyze': 'POST - Analyze UK trends',
            '/generate': 'POST - Generate UK content',
            '/safety': 'POST - Assess brand safety'
        }
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    query = data.get('query', 'What are the current UK trends?')

    try:
        response = model.generate_content(f"Analyze UK trends: {query}")
        return jsonify({
            'status': 'success',
            'analysis': response.text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    trend = data.get('trend', '')
    platform = data.get('platform', 'twitter')

    try:
        prompt = f"Generate {platform} content for UK trend: {trend}. Use British humor and language."
        response = model.generate_content(prompt)
        return jsonify({
            'status': 'success',
            'content': response.text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/safety', methods=['POST'])
def safety():
    data = request.get_json()
    content = data.get('content', '')

    try:
        prompt = f"Assess brand safety for UK market: {content}. Consider ASA and Ofcom guidelines."
        response = model.generate_content(prompt)
        return jsonify({
            'status': 'success',
            'assessment': response.text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))"""

        with open("app.py", "w") as f:
            f.write(flask_app)

        # Update requirements for Flask
        requirements_flask = """google-generativeai==0.8.3
flask==3.0.0
gunicorn==21.2.0"""

        with open("requirements.txt", "w") as f:
            f.write(requirements_flask)

        print("\n[DOCKER] Cloud Run files created:")
        print("   - Dockerfile")
        print("   - app.py (Flask application)")
        print("   - requirements.txt (updated for Flask)")

async def main():
    """Main deployment function"""

    print("\n" + "="*60)
    print("PULSE Agent Deployment (Corrected)")
    print("="*60)

    deployment = PulseAgentDeployment()

    # Test locally
    await deployment.test_agent_locally()

    # Create deployment files
    deployment.create_cloud_function()
    deployment.create_dockerfile()

    # Show deployment options
    deployment.generate_deployment_commands()

    print("\n[DONE] Deployment files created!")
    print("\nChoose your deployment method:")
    print("1. Cloud Function - Best for simple HTTP endpoints")
    print("2. Cloud Run - Best for containerized deployment")
    print("3. Vertex AI Agent Builder - Best for conversational AI")
    print("4. AI Studio - Best for testing and prototyping")

if __name__ == "__main__":
    asyncio.run(main())
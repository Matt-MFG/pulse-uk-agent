#!/usr/bin/env python
"""Direct deployment script for PULSE UK Agent using Vertex AI SDK"""

import os
import sys
from pathlib import Path
import vertexai
from vertexai.preview import reasoning_engines

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Import the agent
from agents.pulse_uk.agent import root_agent

def main():
    """Deploy the PULSE UK agent directly to Agent Engine"""

    # Configuration
    PROJECT_ID = "mfg-open-apps"
    LOCATION = "us-central1"
    STAGING_BUCKET = "gs://mfg-pulse-uk-agent-staging"

    print("Initializing Vertex AI...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    print("Creating reasoning engine...")

    try:
        # Create the reasoning engine
        reasoning_engine = reasoning_engines.ReasoningEngine.create(
            root_agent,
            display_name="PULSE UK Cultural Intelligence Agent",
            description="Advanced UK cultural intelligence agent with real-time data from Reddit, YouTube, and The Guardian.",
            requirements=[
                "google-cloud-aiplatform[adk,agent_engines]>=1.112",
                "praw",
                "google-api-python-client",
                "requests",
                "python-dotenv"
            ]
        )

        print(f"Deployment successful!")
        print(f"Reasoning Engine ID: {reasoning_engine.resource_name}")
        print(f"Project: {PROJECT_ID}")
        print(f"Location: {LOCATION}")

        # Save deployment info
        with open("deployment_info.txt", "w") as f:
            f.write(f"Reasoning Engine ID: {reasoning_engine.resource_name}\n")
            f.write(f"Project: {PROJECT_ID}\n")
            f.write(f"Location: {LOCATION}\n")
            f.write(f"Staging Bucket: {STAGING_BUCKET}\n")

        return reasoning_engine

    except Exception as e:
        print(f"Deployment failed: {e}")
        raise

if __name__ == "__main__":
    main()
"""Deploy PULSE UK Agent to Agent Engine"""

import os
import vertexai
from vertexai import agent_engines
from agents.pulse_uk.agent import root_agent

def main():
    """Deploy the PULSE UK agent to Agent Engine"""

    # Load environment variables from parent directory
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)

    # Initialize Vertex AI client
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "pulse-uk-agent")
    location = "us-central1"

    client = vertexai.Client(
        project=project_id,
        location=location
    )

    try:
        print("Starting deployment to Agent Engine...")

        # Create ADK App for Agent Engine
        app = agent_engines.AdkApp(agent=root_agent)

        # Deploy to Agent Engine using the correct API
        remote_app = client.agent_engines.create(
            agent=app,
            config={
                "display_name": "PULSE UK Cultural Intelligence Agent",
                "requirements": ["google-cloud-aiplatform[agent_engines,adk]>=1.112"]
            }
        )

        print("Deployment successful!")
        print(f"Agent deployed to: {remote_app.name}")
        print(f"Agent resource name: {remote_app.resource_name}")

        # Save deployment info
        with open("deployment_info.txt", "w") as f:
            f.write(f"Agent Name: {remote_app.name}\n")
            f.write(f"Agent Resource: {remote_app.resource_name}\n")
            f.write(f"Project ID: {project_id}\n")

        return remote_app

    except Exception as e:
        print(f"Deployment failed: {e}")
        raise

if __name__ == "__main__":
    main()
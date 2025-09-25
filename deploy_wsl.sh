#!/bin/bash
# PULSE UK Agent WSL Deployment Script

echo "=================================================="
echo "PULSE UK Agent - WSL Deployment Script"
echo "=================================================="

# Set variables
PROJECT_ID="mfg-open-apps"
REGION="us-central1"
STAGING_BUCKET="gs://mfg-pulse-uk-agent-staging"
SERVICE_NAME="pulse-uk-agent"

# Check if we're in the right directory
if [ ! -d "agents/pulse_uk" ]; then
    echo "Error: agents/pulse_uk directory not found!"
    echo "Make sure you're in the pulse-poc/adk-agent directory"
    exit 1
fi

# Step 1: Install dependencies if needed
echo ""
echo "Step 1: Checking Python and pip..."
if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
fi

# Step 2: Create virtual environment
echo ""
echo "Step 2: Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Step 3: Install Google Cloud SDK if not present
echo ""
echo "Step 3: Checking Google Cloud SDK..."
if ! command -v gcloud &> /dev/null; then
    echo "Installing Google Cloud SDK..."
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.asc
    sudo apt-get update && sudo apt-get install -y google-cloud-cli
fi

# Step 4: Install ADK and required packages
echo ""
echo "Step 4: Installing ADK and dependencies..."
pip install --upgrade pip
pip install google-adk
pip install "google-cloud-aiplatform[adk,agent_engines]>=1.112"
pip install python-dotenv praw google-api-python-client requests

# Add the local pip bin directory to PATH
export PATH=$PATH:$HOME/.local/bin

# Step 5: Authenticate with Google Cloud
echo ""
echo "Step 5: Authenticating with Google Cloud..."
echo "You may need to authenticate if not already done:"
gcloud auth application-default login
gcloud config set project $PROJECT_ID

# Step 6: Copy .env file to WSL location if it exists
if [ -f "/mnt/c/Users/matth/socialresearch/pulse-poc/.env" ]; then
    echo ""
    echo "Step 6: Copying environment file..."
    cp /mnt/c/Users/matth/socialresearch/pulse-poc/.env ../
fi

# Step 7: Deploy to Agent Engine
echo ""
echo "Step 7: Deploying to Agent Engine..."
echo "=================================================="

adk deploy agent_engine \
    --project=$PROJECT_ID \
    --region=$REGION \
    --staging_bucket=$STAGING_BUCKET \
    --display_name="PULSE UK Cultural Intelligence Agent" \
    --description="Advanced UK cultural intelligence agent with real-time data from Reddit, YouTube, and The Guardian." \
    --absolutize_imports=false \
    agents/pulse_uk

# Check deployment result
if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✅ Deployment successful!"
    echo "=================================================="
else
    echo ""
    echo "=================================================="
    echo "❌ Deployment failed. Trying Cloud Run as alternative..."
    echo "=================================================="

    # Try Cloud Run deployment as fallback
    adk deploy cloud_run \
        --project=$PROJECT_ID \
        --region=$REGION \
        --service_name=$SERVICE_NAME \
        --with_ui \
        agents/pulse_uk

    if [ $? -eq 0 ]; then
        echo ""
        echo "=================================================="
        echo "✅ Cloud Run deployment successful!"
        echo "=================================================="
    fi
fi

echo ""
echo "Deployment script completed."
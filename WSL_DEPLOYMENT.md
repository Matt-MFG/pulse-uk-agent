# WSL Deployment Instructions for PULSE UK Agent

## Quick Start Commands

Open WSL Ubuntu terminal and run these commands:

```bash
# 1. Navigate to your project directory
cd /mnt/c/Users/matth/socialresearch/pulse-poc/adk-agent

# 2. Make deployment script executable
chmod +x deploy_wsl.sh

# 3. Run deployment
./deploy_wsl.sh
```

## Manual Step-by-Step (if script fails)

### Step 1: Open WSL and navigate to project
```bash
cd /mnt/c/Users/matth/socialresearch/pulse-poc/adk-agent
```

### Step 2: Set up Python environment
```bash
# Install Python if needed
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install --upgrade pip
pip install google-adk
pip install "google-cloud-aiplatform[adk,agent_engines]>=1.112"
pip install python-dotenv praw google-api-python-client requests
```

### Step 4: Copy .env file
```bash
cp /mnt/c/Users/matth/socialresearch/pulse-poc/.env ../
```

### Step 5: Authenticate with Google Cloud
```bash
gcloud auth application-default login
gcloud config set project mfg-open-apps
```

### Step 6: Deploy to Agent Engine
```bash
adk deploy agent_engine \
    --project=mfg-open-apps \
    --region=us-central1 \
    --staging_bucket=gs://mfg-pulse-uk-agent-staging \
    --display_name="PULSE UK Cultural Intelligence Agent" \
    --description="UK cultural intelligence agent with real-time data" \
    --absolutize_imports=false \
    agents/pulse_uk
```

### Alternative: Deploy to Cloud Run (if Agent Engine fails)
```bash
adk deploy cloud_run \
    --project=mfg-open-apps \
    --region=us-central1 \
    --service_name=pulse-uk-agent \
    --with_ui \
    agents/pulse_uk
```

## Expected Output

After successful deployment, you'll receive:
- **Agent Engine**: A reasoning engine ID and endpoint URL
- **Cloud Run**: A service URL like `https://pulse-uk-agent-xxxxx-uc.a.run.app`

## Troubleshooting

1. **Permission Denied**: Make sure to use `chmod +x deploy_wsl.sh`
2. **Auth Issues**: Run `gcloud auth login` and select your Google account
3. **Python Issues**: Ensure you're using Python 3.9+
4. **Path Issues**: Make sure you're in the correct directory

## Next Steps

Once deployed, your PULSE UK agent will be accessible via the cloud URL provided. You can:
- Access the web UI at the provided URL
- Make API calls to the agent endpoint
- Monitor logs in Google Cloud Console
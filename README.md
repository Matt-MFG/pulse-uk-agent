# PULSE UK Cultural Intelligence Agent

An advanced AI agent that provides real-time UK cultural intelligence by monitoring and analyzing data from Reddit, YouTube, and The Guardian.

## Features

- 🔍 **Real-time Data Collection**: Monitors UK subreddits, YouTube trends, and Guardian news
- 🧠 **Advanced Synthesis**: Cross-platform pattern analysis and trend detection
- 📊 **Cultural Weather Reports**: Comprehensive UK cultural landscape analysis
- 📚 **Academic Citations**: Harvard-style source attribution for all insights
- 🚀 **Google ADK Integration**: Built on Google's Agent Development Kit

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pulse-uk-agent.git
cd pulse-uk-agent
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run locally:
```bash
adk web --port 8080 agents/
```

Access the agent at http://localhost:8080

### Cloud Deployment (Google Cloud Shell)

1. Open [Google Cloud Console](https://console.cloud.google.com)
2. Click the Cloud Shell icon (terminal in top right)
3. Clone and deploy:

```bash
# Clone the repository
git clone https://github.com/yourusername/pulse-uk-agent.git
cd pulse-uk-agent

# Copy your .env file or set environment variables
cp .env.example .env
nano .env  # Add your API keys

# Install ADK
pip install google-adk

# Deploy to Agent Engine
adk deploy agent_engine \
  --project=mfg-open-apps \
  --region=us-central1 \
  --staging_bucket=gs://mfg-pulse-uk-agent-staging \
  --display_name="PULSE UK Cultural Intelligence Agent" \
  --description="UK cultural intelligence with real-time data" \
  --absolutize_imports=false \
  agents/pulse_uk
```

## API Keys Required

- **Gemini API**: For AI processing
- **Reddit API**: Client ID and Secret
- **YouTube API**: Data API v3
- **Guardian API**: Content API

## Project Structure

```
pulse-uk-agent/
├── agents/
│   └── pulse_uk/
│       ├── agent.py           # Main agent definition
│       ├── uk_data_tools.py   # Data collection tools
│       ├── synthesis_engine.py # Analysis engine
│       ├── advanced_tools.py  # Advanced analysis tools
│       └── source_formatter.py # Citation formatting
├── pyproject.toml             # Project configuration
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Available Commands

The agent responds to various queries about UK culture:

- **Trend Analysis**: "What are the current UK cultural trends?"
- **Reddit Insights**: "What's trending on UK Reddit?"
- **YouTube Trends**: "Show me UK YouTube trends"
- **News Analysis**: "What's in UK news today?"
- **Cultural Weather**: "Generate a UK cultural weather report"
- **Cross-platform Analysis**: "Compare trends across platforms"

## Troubleshooting

### Windows Deployment Issues
If encountering Unicode errors on Windows, use Google Cloud Shell for deployment.

### API Rate Limits
Ensure your API keys have sufficient quota for:
- Reddit: 60 requests/minute
- YouTube: 10,000 units/day
- Guardian: 5,000 calls/day

## License

MIT

## Contact

For issues or questions, please open an issue on GitHub.
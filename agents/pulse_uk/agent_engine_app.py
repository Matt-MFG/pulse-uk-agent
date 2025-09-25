"""Agent Engine App for PULSE UK Agent"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the agent
from pulse_uk.agent import root_agent

# This is the agent that will be deployed to Agent Engine
agent = root_agent
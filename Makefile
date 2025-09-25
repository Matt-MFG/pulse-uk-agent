# Makefile for PULSE UK Agent deployment

.PHONY: setup-dev-env backend clean

# Setup development environment
setup-dev-env:
	@echo "Setting up development environment..."
	gcloud auth application-default login
	gcloud services enable aiplatform.googleapis.com
	gcloud services enable storage.googleapis.com

# Deploy backend to Agent Engine
backend:
	@echo "Deploying PULSE UK Agent to Agent Engine..."
	python deploy_agent.py

# Clean up resources
clean:
	@echo "Cleaning up resources..."
	python cleanup_agent.py
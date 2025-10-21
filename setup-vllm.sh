#!/bin/bash

# Setup vLLM Server - Installation Script
# This script helps you set up a vLLM server for testing

echo "=========================================="
echo "vLLM Server Setup for Translation"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create vLLM directory
echo "Creating vLLM directory..."
mkdir -p vllm-server
cd vllm-server

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv vllm-env

# Activate virtual environment
echo "Activating virtual environment..."
source vllm-env/bin/activate  # On Windows: vllm-env\Scripts\activate

# Install vLLM
echo "Installing vLLM (this may take a few minutes)..."
pip install vllm

echo ""
echo "=========================================="
echo "✓ vLLM Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Download a translation model (e.g., from HuggingFace)"
echo "2. Run vLLM server with your model"
echo ""
echo "Example command to run vLLM:"
echo "python -m vllm.entrypoints.openai.api_server \\"
echo "  --model YOUR_MODEL_NAME \\"
echo "  --port 8001"
echo ""

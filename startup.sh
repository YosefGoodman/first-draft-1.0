#!/bin/bash
# ===================================
# AI Chatbot Startup Script
# ===================================
# Instructions:
# 1. Updates pip and installs new dependencies
# 2. Starts Flask chatbot server
# 3. Can be configured to run at boot (Linux/macOS) or via Task Scheduler (Windows)

echo "=== Updating dependencies ==="
python -m pip install --upgrade pip
pip install -r requirements.txt --upgrade

echo "=== Starting Flask server ==="
python app.py


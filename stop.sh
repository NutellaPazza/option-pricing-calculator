#!/bin/bash
# Stop script for Streamlit Option Pricing App

echo "🛑 Stopping Streamlit server..."

# Kill all Streamlit processes
pkill -f streamlit

# Double check port 8501
lsof -ti:8501 | xargs kill -9 2>/dev/null || true

echo "✅ Server stopped successfully!"

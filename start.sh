#!/bin/bash
# Automatic startup script for Streamlit Option Pricing App
# This script ensures the server starts correctly every time

cd "$(dirname "$0")"

echo "🚀 Starting Option Pricing Calculator..."

# Kill any existing Streamlit processes on port 8501
echo "🔍 Checking for existing Streamlit processes..."
lsof -ti:8501 | xargs kill -9 2>/dev/null || true
sleep 2

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Start Streamlit
echo "🌐 Starting Streamlit server..."
streamlit run app.py --server.headless=true --server.port=8501 &

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 5

# Check if server is running
if curl -s http://localhost:8501 > /dev/null; then
    echo "✅ Server started successfully!"
    echo "🌐 Access the app at: http://localhost:8501"
    echo ""
    echo "📝 To stop the server, press Ctrl+C or run: pkill -f streamlit"
else
    echo "❌ Server failed to start. Checking for errors..."
    echo "Try running manually: source venv/bin/activate && streamlit run app.py"
fi

# Keep script running to show logs
wait

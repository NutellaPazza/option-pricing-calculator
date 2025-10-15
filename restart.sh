#!/bin/bash
# Restart script for Streamlit Option Pricing App

cd "$(dirname "$0")"

echo "🔄 Restarting Option Pricing Calculator..."

# Stop existing server
./stop.sh

# Wait a moment
sleep 2

# Start new server
./start.sh

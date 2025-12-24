#!/bin/bash
# Quick deployment script using ngrok
# Perfect for tonight's Christmas present!

echo "🎄 CB Cabrera Basketball Dashboard - Quick Deployment"
echo "======================================================"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "📦 Installing ngrok..."
    brew install ngrok
fi

echo "🚀 Starting deployment..."
echo ""

# Check if dashboard is running
if ! lsof -i :8080 > /dev/null 2>&1; then
    echo "⚠️  Dashboard not running. Starting it now..."
    python3 web_dashboard.py > /dev/null 2>&1 &
    sleep 3
fi

echo "✅ Dashboard is running on http://localhost:8080"
echo ""

# Check if ngrok is configured
if ! ngrok config check > /dev/null 2>&1; then
    echo "⚠️  ngrok not configured yet!"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to https://dashboard.ngrok.com/signup"
    echo "2. Sign up (it's free!)"
    echo "3. Get your auth token from https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "4. Run: ngrok config add-authtoken YOUR_TOKEN"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

echo "🌍 Creating public URL..."
echo ""
echo "Your dashboard will be available at a URL like:"
echo "https://abc123-def456.ngrok-free.app"
echo ""
echo "📋 IMPORTANT: Copy the URL and send it to the president!"
echo ""
echo "Press Ctrl+C to stop when you're done."
echo ""
echo "Starting ngrok..."
echo "======================================================"
echo ""

ngrok http 8080

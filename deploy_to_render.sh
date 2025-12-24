#!/bin/bash
# Deploy CB Cabrera Dashboard to Render.com
# Permanent hosting solution

echo "🚀 CB Cabrera Dashboard - Render.com Deployment"
echo "================================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Step 1: Initializing Git repository..."
    git init
    git add .
    git commit -m "CB Cabrera Basketball Dashboard - Christmas 2024 🎄"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "📋 Step 2: GitHub Repository Setup"
echo "=================================="
echo ""
echo "Please follow these steps:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Repository name: cb-cabrera-dashboard"
echo "3. Description: Basketball statistics dashboard for CB Cabrera"
echo "4. Make it PUBLIC (Render free tier requires public repos)"
echo "5. Do NOT initialize with README (we already have one)"
echo "6. Click 'Create repository'"
echo ""
read -p "Press ENTER when you've created the GitHub repository..."

echo ""
echo "📤 Step 3: What's your GitHub username?"
read -p "Username: " GITHUB_USERNAME

echo ""
echo "🔗 Connecting to GitHub..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/${GITHUB_USERNAME}/cb-cabrera-dashboard.git"
git branch -M main

echo ""
echo "⬆️  Pushing to GitHub..."
echo ""
echo "⚠️  You'll need to enter your GitHub credentials:"
echo "   Username: ${GITHUB_USERNAME}"
echo "   Password: Use a Personal Access Token (not your password!)"
echo ""
echo "   To create a token:"
echo "   1. Go to https://github.com/settings/tokens"
echo "   2. Click 'Generate new token (classic)'"
echo "   3. Select: repo (all permissions)"
echo "   4. Generate and copy the token"
echo "   5. Use it as your password below"
echo ""
read -p "Press ENTER to continue with git push..."

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Code pushed to GitHub successfully!"
    echo ""
    echo "================================================"
    echo "📋 Step 4: Deploy to Render.com"
    echo "================================================"
    echo ""
    echo "Now follow these steps:"
    echo ""
    echo "1. Go to https://render.com"
    echo "2. Sign up / Log in (use GitHub to sign in for easy setup)"
    echo "3. Click 'New +' → 'Web Service'"
    echo "4. Click 'Connect' next to your GitHub account"
    echo "5. Select 'cb-cabrera-dashboard' repository"
    echo "6. Click 'Connect'"
    echo ""
    echo "Configuration:"
    echo "   Name: cb-cabrera-dashboard"
    echo "   Environment: Python 3"
    echo "   Build Command: pip install -r requirements.txt"
    echo "   Start Command: gunicorn web_dashboard:app --bind 0.0.0.0:\$PORT"
    echo ""
    echo "7. Click 'Create Web Service'"
    echo "8. Wait 5-10 minutes for deployment"
    echo ""
    echo "🎉 You'll get a URL like:"
    echo "   https://cb-cabrera-dashboard.onrender.com"
    echo ""
    echo "================================================"
    echo "✅ DEPLOYMENT COMPLETE!"
    echo "================================================"
    echo ""
    echo "Your dashboard will be online 24/7!"
    echo "Share the URL with coaches and the president!"
    echo ""
    echo "Bon Nadal! 🎄🏀"
else
    echo ""
    echo "❌ Git push failed. Please check:"
    echo "   - GitHub repository exists"
    echo "   - You used a Personal Access Token (not password)"
    echo "   - Token has 'repo' permissions"
    echo ""
    echo "Try again or contact me for help!"
fi

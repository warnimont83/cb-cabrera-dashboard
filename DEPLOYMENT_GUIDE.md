# 🎄 CB Cabrera Basketball Dashboard - Deployment Guide

## Quick Deployment Options for Tonight

### Option 1: ngrok (Fastest - 5 minutes)

**Perfect for tonight!** Create a public URL instantly.

```bash
# 1. Install ngrok
brew install ngrok

# 2. Create account at https://ngrok.com and get auth token
ngrok config add-authtoken YOUR_AUTH_TOKEN

# 3. Start the dashboard
python3 web_dashboard.py

# 4. In another terminal, create public URL
ngrok http 8080

# You'll get a URL like: https://abc123.ngrok.io
```

**Pros:**
- Ready in 5 minutes
- Free tier available
- HTTPS included
- Share link immediately

**Cons:**
- URL changes every time you restart (unless paid plan)
- Your computer must stay on

---

### Option 2: Render.com (Best free option - 15 minutes)

**Recommended for production!** Free hosting with custom domain support.

#### Step 1: Prepare the app

```bash
cd /Users/enric.sola/Documents/Basket

# Create requirements.txt
cat > requirements.txt << EOF
Flask==3.0.0
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.1.4
plotly==5.18.0
gunicorn==21.2.0
EOF

# Create Procfile for Render
echo "web: gunicorn web_dashboard:app --bind 0.0.0.0:\$PORT" > Procfile

# Create render.yaml
cat > render.yaml << EOF
services:
  - type: web
    name: cb-cabrera-dashboard
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn web_dashboard:app --bind 0.0.0.0:\$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
EOF
```

#### Step 2: Push to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "CB Cabrera Basketball Dashboard - Christmas 2024"

# Create GitHub repo and push
# (Create repo on github.com first)
git remote add origin https://github.com/YOUR_USERNAME/cb-cabrera-dashboard.git
git branch -M main
git push -u origin main
```

#### Step 3: Deploy to Render

1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Select your repository
5. Click "Create Web Service"
6. Wait 5-10 minutes for deployment

**You'll get a URL like:** `https://cb-cabrera-dashboard.onrender.com`

**Pros:**
- Free tier (no credit card needed)
- Automatic HTTPS
- Custom domain support
- Auto-deploys on git push
- Stays online 24/7

**Cons:**
- Free tier sleeps after 15 minutes of inactivity (wakes up in ~30 seconds)

---

### Option 3: Railway.app (Alternative - 15 minutes)

Similar to Render, but with $5/month free credit.

```bash
# Install Railway CLI
brew install railway

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

**You'll get a URL like:** `https://cb-cabrera-dashboard.up.railway.app`

---

### Option 4: Run on Your Mac (Local network access)

If you just want the president to access it while on the same WiFi:

```bash
# Start the dashboard (already configured to listen on all interfaces)
python3 web_dashboard.py

# Share this URL with the president:
# http://YOUR_LOCAL_IP:8080
# (You can find your IP with: ipconfig getifaddr en0)
```

---

## Production Improvements (Do these first!)

### 1. Install Gunicorn (Production Server)

```bash
pip3 install gunicorn
```

### 2. Update web_dashboard.py for production

Add this at the bottom of `web_dashboard.py`:

```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    # Use debug=False for production
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 3. Run with Gunicorn

```bash
gunicorn web_dashboard:app --bind 0.0.0.0:8080 --workers 2
```

---

## Recommended Approach for Tonight:

### Quick & Easy (Option 1 - ngrok):
1. Install ngrok: `brew install ngrok`
2. Start dashboard: `python3 web_dashboard.py`
3. Create tunnel: `ngrok http 8080`
4. Share the ngrok URL ✅

### Better & Free (Option 2 - Render):
1. Create requirements.txt and Procfile (commands above)
2. Push to GitHub
3. Deploy to Render.com
4. Share the Render URL ✅

---

## Custom Domain (Optional)

If you want `basquet.club-cabrera.cat` or similar:

1. Deploy to Render/Railway
2. In your domain DNS settings, add:
   - CNAME record: `basquet` → `cb-cabrera-dashboard.onrender.com`
3. In Render dashboard, add custom domain

---

## Security Considerations

### For Public Deployment:

1. **Add Basic Authentication** (optional):
```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "cabrera": "ChristmasBàsquet2024!"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    ...
```

2. **Or add IP whitelisting in Render/Railway**

3. **Environment variables for sensitive data** (if needed)

---

## Testing Before Sharing

```bash
# Test locally first
python3 web_dashboard.py

# Open in browser
open http://localhost:8080

# Check all pages:
# ✓ Home page
# ✓ Team listings
# ✓ Team details with standings
# ✓ Player statistics
# ✓ Match details
# ✓ Rival scouting
```

---

## Christmas Presentation Tips 🎄

1. **Title slide**: "Tauler de Bàsquet CB Cabrera"
2. **Show key features**:
   - 30 equips amb estadístiques completes
   - Classificacions de lliga en temps real
   - Anàlisi de rivals
   - Historial de partits
   - Estadístiques de jugadors
3. **Demo path**:
   - Home → Select Mini Masculí 1r Any
   - Show CB Cabrera Vermell team page
   - Show league standings
   - Click "Scout Team" on a rival
   - Show player statistics
   - Click into a match for details

---

## Support & Updates

After deployment, you can update anytime:

```bash
# Update data
./scrape_all_cabrera.sh

# Recalculate standings
./calculate_all_standings.sh

# If using Git deployment (Render/Railway)
git add .
git commit -m "Update data"
git push  # Auto-deploys!
```

---

## Troubleshooting

**Dashboard not loading?**
- Check Python version: `python3 --version` (need 3.9+)
- Check all dependencies installed: `pip3 list`
- Check port not in use: `lsof -i :8080`

**Data not showing?**
- Verify data folders exist: `ls CLUB_BASQUET_CABRERA/`
- Check standings calculated: `./calculate_all_standings.sh`

**Slow loading?**
- Normal on first load (parsing all JSON files)
- Consider adding caching in production

---

## Next Steps (After Christmas)

1. Add caching for better performance
2. Add export to PDF/Excel
3. Add player comparison features
4. Add season-over-season trends
5. Mobile responsive improvements
6. Add notifications for new matches

Bon Nadal! 🎄🏀

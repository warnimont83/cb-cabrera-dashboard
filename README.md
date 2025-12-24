# 🏀 CB Cabrera Basketball Dashboard

Professional basketball statistics and analytics dashboard for Club Bàsquet Cabrera.

## Features

- ✅ 30 teams with complete statistics
- 📊 Real-time league standings
- 🎯 Rival team scouting and analysis
- 👥 Detailed player statistics
- 📈 Match history and play-by-play
- 🇨🇦 Catalan/English language support

## Live Demo

🔗 [CB Cabrera Dashboard](https://your-url-here.onrender.com)

## Tech Stack

- **Backend**: Python Flask
- **Data Source**: Federació Catalana de Bàsquet API
- **Hosting**: Render.com
- **Scraping**: BeautifulSoup4, Requests

## Local Development

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run dashboard
python3 web_dashboard.py

# Visit http://localhost:8080
```

## Data Updates

```bash
# Scrape all teams
./scrape_all_cabrera.sh

# Calculate standings
./calculate_all_standings.sh
```

## Deployment

Automatically deploys to Render.com on push to main branch.

---

🎄 **Bon Nadal 2024** - Created as a Christmas gift for CB Cabrera

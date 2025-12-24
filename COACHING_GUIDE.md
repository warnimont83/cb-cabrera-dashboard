# CB Cabrera Coaching Dashboard - User Guide

## Overview
This dashboard is designed specifically for CB Cabrera coaches to analyze team performance, track player statistics, and scout rival teams.

## Features

### 🏠 Home Page
- **CB Cabrera Overview**: All teams organized by category (just like the federation website)
- **Quick Stats**: Win/loss records, player counts, and match totals per team
- **Season Filter**: Switch between seasons or view all-time statistics
- **Quick Links**: Jump directly to Calendar, Rivals, or Club Stats

### 📅 Calendar View
- **All Matches**: View every CB Cabrera match across all teams
- **Organized by Month**: Matches grouped chronologically
- **Category Tags**: Quickly identify which team played
- **Result Highlighting**: CB Cabrera teams highlighted for easy identification

### 🎯 Rival Teams Analysis
This is a powerful scouting tool for coaches:

#### Rivals Page
- **Complete List**: All opponent teams you've faced
- **Key Metrics**:
  - Matches played against each rival
  - Win/Loss record (from rival's perspective)
  - Average points scored
  - Categories they compete in
- **Search Function**: Quickly find specific rival teams
- **Sortable Columns**: Sort by any metric (games played, win %, avg points)

#### Rival Detail View
Click on any rival team to see:
- **Player Statistics**: Full roster stats including:
  - Points per game (PPG)
  - Minutes played
  - Shooting percentages
  - Rebounds, assists (when tracked)
  - Efficiency ratings
- **Match History**: All games against this rival with:
  - Dates and scores
  - Result indicators (Win/Loss)
  - Direct links to full match details
- **Scouting Intel**: Identify their top scorers and key players

### 👥 Team Pages
- **Player Statistics**: All CB Cabrera players with full stats
- **Season Filtering**: Focus on current or past seasons
- **Sortable Stats**: Click any column header to sort
- **Player Links**: Click player names for individual profiles

### 👤 Player Pages
Individual player profiles showing:
- Season totals (games, points, minutes)
- Season averages (PPG, MPG, rebounds, assists)
- Game-by-game statistics
- Shooting percentages

## How to Use This for Coaching

### 1. Pre-Game Preparation
Before playing a rival team:
1. Go to **Rivals** page
2. Find the opponent team
3. Click **View Details**
4. Review their top scorers and key players
5. Note shooting percentages and play styles
6. Check previous match results against them

### 2. Player Development
Track individual player progress:
1. Navigate to your team
2. Click on a player's name
3. Review their game-by-game performance
4. Identify trends (improving, declining, consistent)
5. Use data for coaching conversations

### 3. Team Analysis
Evaluate team performance:
1. View team statistics page
2. Compare players side-by-side
3. Sort by different metrics (PPG, efficiency, etc.)
4. Identify team strengths and weaknesses

### 4. Season Planning
Use the calendar to:
- Review upcoming opponents
- Plan practice sessions based on rival strengths
- Track improvement across the season

## Access
- **Local**: http://127.0.0.1:8080
- **Network**: http://192.168.0.25:8080
- **Mobile-Friendly**: Access from phone or tablet on the same network

## Data Privacy
- All data is scraped from public federation statistics
- Only CB Cabrera and rival team data is shown
- No personal information beyond what's publicly available on basquetcatala.cat

## Tips for Coaches

### Scouting Rivals
- Focus on PPG (points per game) to identify primary scorers
- Check FT% and FG% to understand shooting reliability
- Look at games played to see who their regular starters are
- Review match history to see how they've improved over time

### Player Development
- Compare players in the same position across PPG, efficiency
- Track improvement by comparing different seasons
- Use shooting percentages to guide practice focus
- Monitor playing time distribution

### Match Preparation
- Review rival's last 3-5 games before playing them
- Identify their lineup patterns
- Note their scoring distribution (one star vs balanced team)
- Check if they've improved since last meeting

## Updating Data
To get the latest match data:
```bash
make run-cabrera
# or
./venv/bin/python club_scraper.py 59 tot
```

Then refresh the web dashboard - new matches will automatically appear.

## Support
For issues or feature requests, check the logs or contact the system administrator.

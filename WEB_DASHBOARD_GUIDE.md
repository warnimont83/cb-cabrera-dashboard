# Web Dashboard - Complete Guide

## What's New?

The web dashboard has been completely redesigned with:

### Hierarchical Navigation
- **Home**: Browse all clubs
- **Club Page**: View categories within a club
- **Team Page**: See player statistics and all matches
- **Match Page**: Detailed statistics for individual matches

### Complete Statistics Display
- **Player Stats**: Points, rebounds, assists, shooting percentages, and more
- **Match History**: Full list of all matches with scores
- **Individual Match Details**: Complete box scores for both teams
- **Aggregated Data**: Season totals and averages

## How to Use

### 1. Start the Dashboard

```bash
# Make sure dependencies are installed
source venv/bin/activate
pip install -r requirements.txt

# Start the web server
make serve
# or
python3 web_dashboard.py
```

Open your browser to: **http://localhost:8080**

### 2. Navigation Flow

```
Home Page (All Clubs)
  ↓
  Click on a club
  ↓
Club Page (Categories)
  ↓
  Click on a team
  ↓
Team Page (Player Stats + Matches)
  ↓
  Click on a match
  ↓
Match Details (Full Box Score)
```

## Features

### Home Page
- Overview of all clubs in your database
- Quick stats: total clubs, teams, and matches
- Organized by club with expandable categories
- Direct links to all teams

### Club Page
- All categories for the selected club
- Number of teams per category
- Quick access to any team

### Team Page
Shows:
- **Player Statistics Table**:
  - Games played
  - Total points and PPG (points per game)
  - Minutes, rebounds, assists
  - Field goal percentage
  - 3-point shooting
  - Player rating

- **Matches List**:
  - Date and time
  - Opponent
  - Final score
  - Click any match for details

### Match Details Page
Complete box score showing:
- Final score (big scoreboard)
- Player statistics for both teams:
  - Minutes played
  - Points scored
  - Free throws (FT)
  - 2-point field goals (2PT)
  - 3-point field goals (3PT)
  - Rebounds, assists, steals, blocks
  - Fouls
  - Player rating

## Example Use Cases

### View Your Kids' Team Stats
1. Go to home page
2. Click "CLUB_BASQUET_CABRERA"
3. Find the category (e.g., "C.T._MINI_MASCULÍ")
4. Click on your team
5. See all player statistics and matches

### Check a Specific Match
1. Navigate to the team page
2. Scroll to "Matches" section
3. Click on any match card
4. View complete statistics for both teams

### Compare Players
1. Go to team page
2. Look at the player statistics table
3. Sort mentally by any column (PPG, rebounds, assists, etc.)
4. Players are sorted by total points by default

## Tips

- **Bookmarks**: Bookmark your favorite teams for quick access
- **Mobile Friendly**: The dashboard works on phones and tablets
- **Real-time Data**: Refresh after running the scraper to see new data
- **Navigation**: Use the breadcrumb links to go back

## Troubleshooting

### No data showing?
- Run the scraper first: `make run-cabrera`
- Check that JSON files exist in team directories

### Players not aggregating correctly?
- The dashboard looks at ALL matches in a team directory
- Player stats are totaled across all games
- Averages are calculated automatically

### Match details not showing?
- Ensure the JSON file exists
- Check file permissions
- Look for error messages in the terminal

## Technical Details

### Data Source
- Reads directly from JSON files in team directories
- No database queries needed for display
- Fast loading times

### Supported Statistics
All statistics from the JSON files are displayed:
- Scoring: 1PT, 2PT, 3PT, total points
- Advanced: rebounds, assists, steals, blocks
- Efficiency: shooting percentages, player rating
- Usage: minutes played, fouls

### Filtering (Coming Soon)
Future features:
- Filter by date range
- Filter by phase (fase1, fase2)
- Search players across all teams
- Export to CSV

## Comparison: Old vs New

| Feature | Old Dashboard | New Dashboard |
|---------|---------------|---------------|
| Navigation | Flat team list | Hierarchical (Club → Team) |
| Player Stats | Not showing | ✅ Complete table |
| Matches | Not visible | ✅ Full list with scores |
| Match Details | Not available | ✅ Complete box scores |
| Aggregation | Limited | ✅ Totals + Averages |
| Data Quality | Partial | ✅ All fields displayed |

---

**Enjoy your enhanced basketball statistics dashboard!**

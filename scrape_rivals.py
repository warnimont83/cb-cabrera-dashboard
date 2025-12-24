#!/usr/bin/env python3
"""
Rival Teams Scraper
Automatically detects and scrapes statistics for teams competing against CB Cabrera
"""

import requests
from bs4 import BeautifulSoup
import re
import subprocess
import json
from pathlib import Path
import time


BASE_URL = "https://www.basquetcatala.cat"


def get_competition_id(team_id):
    """Get competition ID for a team by scraping their team page"""
    url = f"{BASE_URL}/equip/{team_id}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to retrieve team page for team {team_id}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for "Veure resultats" link
        results_link = soup.find('a', string=lambda text: text and 'Veure resultats' in text)
        if not results_link:
            print(f"⚠️  No competition results link found for team {team_id}")
            return None

        href = results_link.get('href', '')
        # Extract competition ID from /competicions/resultats/XXXXX
        match = re.search(r'/competicions/resultats/(\d+)', href)
        if match:
            comp_id = match.group(1)
            print(f"✅ Found competition ID: {comp_id}")
            return comp_id
        else:
            print(f"⚠️  Could not extract competition ID from: {href}")
            return None

    except Exception as e:
        print(f"❌ Error getting competition ID: {e}")
        return None


def get_teams_in_competition(competition_id):
    """Get all team IDs and standings from a competition"""
    url = f"{BASE_URL}/competicions/resultats/{competition_id}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to retrieve competition page {competition_id}")
            return [], {}

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract team IDs from links
        team_ids = []
        team_links = soup.find_all('a', href=re.compile(r'/equip/\d+'))
        for link in team_links:
            match = re.search(r'/equip/(\d+)', link['href'])
            if match:
                team_id = match.group(1)
                if team_id not in team_ids:
                    team_ids.append(team_id)

        # Extract standings/classification table
        standings = {}
        competition_name = ""

        # Try to find competition name
        comp_title = soup.find('h1')
        if comp_title:
            competition_name = comp_title.text.strip()

        # Try to find standings table
        table = soup.find('table', class_='table')
        if table:
            rows = table.find_all('tr')[1:]  # Skip header
            standings_list = []

            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 7:
                    # Extract team name and link
                    team_link = row.find('a', href=re.compile(r'/equip/\d+'))
                    team_id_match = re.search(r'/equip/(\d+)', team_link['href']) if team_link else None

                    # Handle both 8-column and 9-column tables (some have "No-Shows" column)
                    # Columns: Position, Team, Matches, Wins, Losses, [No-Shows], PF, PA, Total Points
                    if len(cols) >= 9:
                        # Table has No-Shows column
                        pf_idx, pa_idx, total_idx = 6, 7, 8
                    else:
                        # Standard table without No-Shows
                        pf_idx, pa_idx, total_idx = 5, 6, 7

                    standings_list.append({
                        'position': cols[0].text.strip(),
                        'team_name': cols[1].text.strip(),
                        'team_id': team_id_match.group(1) if team_id_match else None,
                        'matches': cols[2].text.strip(),
                        'wins': cols[3].text.strip(),
                        'losses': cols[4].text.strip(),
                        'points_for': cols[pf_idx].text.strip(),
                        'points_against': cols[pa_idx].text.strip(),
                        'total_points': cols[total_idx].text.strip() if len(cols) > total_idx else '0'
                    })

            if standings_list:
                standings = {
                    'competition_id': competition_id,
                    'competition_name': competition_name,
                    'teams': standings_list
                }

        print(f"✅ Found {len(team_ids)} teams in competition {competition_id}")

        return team_ids, standings

    except Exception as e:
        print(f"❌ Error getting teams from competition: {e}")
        return [], {}


def scrape_rival_team(team_id, phase="tot"):
    """Scrape a rival team's statistics"""
    print(f"\n{'='*60}")
    print(f"Scraping rival team: {team_id}")
    print(f"{'='*60}")

    try:
        # Run team_scraper.py for this specific team
        result = subprocess.run(
            ["python3", "team_scraper.py", str(team_id), phase],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ Successfully scraped team {team_id}")
            return True
        else:
            print(f"❌ team_scraper.py failed for team {team_id}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False

    except FileNotFoundError:
        print(f"❌ team_scraper.py not found in current directory")
        return False
    except Exception as e:
        print(f"❌ Error scraping rival team {team_id}: {e}")
        return False


def save_standings(team_id, standings):
    """Save standings data for a team"""
    if not standings:
        print(f"⚠️  No standings data to save")
        return

    # Search for the team folder
    base_dir = Path(".")
    print(f"🔍 Looking for team folder with pattern: **/{team_id}_*")

    team_folders = list(base_dir.glob(f"**/{team_id}_*"))

    if not team_folders:
        print(f"⚠️  Could not find folder for team {team_id}")
        print(f"   Searched in: {base_dir.absolute()}")
        # Try to list what folders exist
        all_team_folders = list(base_dir.glob("**/*/8*_*"))
        if all_team_folders:
            print(f"   Found these team folders:")
            for folder in all_team_folders[:5]:
                print(f"     - {folder}")
        return

    team_folder = team_folders[0]
    standings_file = team_folder / "standings.json"

    print(f"📂 Saving to: {standings_file}")

    try:
        with open(standings_file, 'w', encoding='utf-8') as f:
            json.dump(standings, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved standings to {standings_file}")
    except Exception as e:
        print(f"❌ Error saving standings: {e}")


def calculate_standings_from_matches(team_id, team_folder, competition_team_ids):
    """
    Calculate standings from match results for a team's competition

    Args:
        team_id: CB Cabrera team ID
        team_folder: Path to team folder containing match JSONs
        competition_team_ids: List of team IDs in this competition

    Returns:
        dict: Standings data structure
    """
    import json
    from collections import defaultdict
    from pathlib import Path

    team_path = Path(team_folder)
    if not team_path.exists():
        print(f"⚠️  Team folder not found: {team_path}")
        return None

    # Collect all teams and their match results
    team_stats = defaultdict(lambda: {
        'name': '',
        'team_id': '',
        'matches': 0,
        'wins': 0,
        'losses': 0,
        'points_for': 0,
        'points_against': 0
    })

    # Find team folders for teams in this competition only
    base_dir = Path(".")
    all_team_folders = []

    for tid in competition_team_ids:
        folders = list(base_dir.glob(f"**/{tid}_*"))
        if folders:
            all_team_folders.append(folders[0])

    print(f"📊 Found {len(all_team_folders)}/{len(competition_team_ids)} team folders in competition")

    # Collect all unique matches (to avoid double-counting)
    processed_matches = set()
    match_files = []

    for folder in all_team_folders:
        for match_file in folder.glob("*_stats.json"):
            # Use match ID from filename to avoid duplicates
            match_id = match_file.stem.split('_')[0]
            if match_id not in processed_matches:
                processed_matches.add(match_id)
                match_files.append(match_file)

    print(f"📊 Processing {len(match_files)} unique matches")

    for match_file in match_files:
        try:
            with open(match_file, 'r', encoding='utf-8') as f:
                match_data = json.load(f)

            teams = match_data.get('teams', [])
            if len(teams) != 2:
                continue

            # Extract team IDs, names, and scores
            team_info = []
            for team in teams:
                tid = str(team.get('teamIdExtern', ''))
                if not tid:
                    continue

                team_name = team.get('name', f'Team {tid}')

                # Get score from first player (all players have same teamScore)
                players = team.get('players', [])
                team_score = 0
                opp_score = 0
                if players:
                    team_score = players[0].get('teamScore', 0)
                    opp_score = players[0].get('oppScore', 0)

                team_info.append({
                    'id': tid,
                    'name': team_name,
                    'score': team_score,
                    'opp_score': opp_score
                })

                # Initialize team if first time seeing them
                if not team_stats[tid]['name']:
                    team_stats[tid]['name'] = team_name
                    team_stats[tid]['team_id'] = tid

            if len(team_info) != 2:
                continue

            # Determine winner
            team1_score = team_info[0]['score']
            team2_score = team_info[1]['score']
            team1_id = team_info[0]['id']
            team2_id = team_info[1]['id']

            if team1_score > team2_score:
                team_stats[team1_id]['wins'] += 1
                team_stats[team2_id]['losses'] += 1
            elif team2_score > team1_score:
                team_stats[team2_id]['wins'] += 1
                team_stats[team1_id]['losses'] += 1

            team_stats[team1_id]['matches'] += 1
            team_stats[team2_id]['matches'] += 1
            team_stats[team1_id]['points_for'] += team1_score
            team_stats[team1_id]['points_against'] += team2_score
            team_stats[team2_id]['points_for'] += team2_score
            team_stats[team2_id]['points_against'] += team1_score

        except Exception as e:
            print(f"⚠️  Error processing {match_file.name}: {e}")
            continue

    # Calculate total points (wins * 2 + losses * 1)
    standings_list = []
    for tid, stats in team_stats.items():
        if stats['matches'] > 0:
            total_points = stats['wins'] * 2 + stats['losses'] * 1
            standings_list.append({
                'team_id': stats['team_id'],
                'team_name': stats['name'],
                'matches': str(stats['matches']),
                'wins': str(stats['wins']),
                'losses': str(stats['losses']),
                'points_for': str(stats['points_for']),
                'points_against': str(stats['points_against']),
                'total_points': str(total_points)
            })

    # Sort by total points (descending), then by point differential
    standings_list.sort(key=lambda x: (
        -int(x['total_points']),
        -(int(x['points_for']) - int(x['points_against']))
    ))

    # Add positions
    for i, team in enumerate(standings_list, 1):
        team['position'] = str(i)

    if standings_list:
        print(f"✅ Calculated standings for {len(standings_list)} teams")
        return {
            'competition_id': 'calculated',
            'competition_name': 'Calculated from Match Results',
            'teams': standings_list
        }

    return None


def scrape_rivals_for_team(team_id, phase="tot", scrape_rivals=True):
    """
    Main function to scrape rivals for a CB Cabrera team

    Args:
        team_id: CB Cabrera team ID
        phase: Competition phase (tot, fase1, fase2)
        scrape_rivals: If True, also scrape rival team statistics
    """
    print(f"\n{'='*60}")
    print(f"Processing rivals for CB Cabrera team: {team_id}")
    print(f"{'='*60}\n")

    # Step 1: Get competition ID
    competition_id = get_competition_id(team_id)
    if not competition_id:
        print(f"⚠️  Could not find competition for team {team_id}")
        return False

    # Step 2: Get all teams in competition and standings
    team_ids, standings = get_teams_in_competition(competition_id)
    if not team_ids:
        print(f"⚠️  No teams found in competition {competition_id}")
        return False

    # Step 3: If standings table not available (JavaScript-loaded), calculate from matches
    if not standings:
        print(f"ℹ️  Standings table not found (JavaScript-loaded page)")
        print(f"ℹ️  Calculating standings from match results instead...")

        # Find team folder
        base_dir = Path(".")
        team_folders = list(base_dir.glob(f"**/{team_id}_*"))
        if team_folders:
            standings = calculate_standings_from_matches(team_id, team_folders[0], team_ids)

    # Step 4: Save standings
    save_standings(team_id, standings)

    # Step 4: Scrape rival teams (optional)
    if scrape_rivals:
        print(f"\n📊 Found {len(team_ids)} teams total in competition")
        rival_teams = [tid for tid in team_ids if str(tid) != str(team_id)]
        print(f"🎯 Will scrape {len(rival_teams)} rival teams\n")

        for i, rival_id in enumerate(rival_teams, 1):
            scrape_rival_team(rival_id, phase)
            # Add delay between requests to avoid rate limiting
            if i < len(rival_teams):
                print(f"⏳ Waiting 2 seconds before next team...")
                time.sleep(2)
    else:
        print(f"\n⏭️  Skipping rival team scraping (scrape_rivals=False)")

    print(f"\n✅ Completed rival detection for team {team_id}")
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 scrape_rivals.py <team_id> [phase] [--no-scrape]")
        print("Example: python3 scrape_rivals.py 81385 tot")
        print("         python3 scrape_rivals.py 81385 fase1 --no-scrape")
        sys.exit(1)

    team_id = sys.argv[1]
    phase = sys.argv[2] if len(sys.argv) > 2 else "tot"
    scrape_rivals = "--no-scrape" not in sys.argv

    scrape_rivals_for_team(team_id, phase, scrape_rivals)

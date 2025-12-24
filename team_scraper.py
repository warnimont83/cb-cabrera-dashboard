#!/usr/bin/env python3
"""
Individual Team Scraper
Scrapes statistics for a single team using the existing matches_by_team.py infrastructure
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import subprocess
import sys
from pathlib import Path
from config_loader import config


BASE_URL = config.base_url


def get_team_info(team_id):
    """Get team name, club, and category from team page"""
    url = f"{BASE_URL}/equip/{team_id}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None, None, None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Get team name
        team_name_elem = soup.find('h1', class_='notranslate')
        team_name = team_name_elem.text.strip() if team_name_elem else f"Team_{team_id}"

        # Get club name (parent link)
        club_link = soup.find('a', href=re.compile(r'/club/\d+'))
        club_name = "Unknown_Club"

        if club_link:
            club_name = club_link.text.strip()

        # Get category from the page
        category = "Unknown_Category"
        # Try to find category in the team info section
        info_section = soup.find('div', class_='col-md-8')
        if info_section:
            text = info_section.get_text()
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            # Category is usually one of the first lines after team name
            if len(lines) > 1:
                for line in lines:
                    if any(keyword in line.upper() for keyword in ['MASCULÍ', 'FEMENÍ', 'MINI', 'INFANTIL', 'CADET', 'JÚNIOR', 'SÈNIOR', 'PRIMERA', 'SEGONA', 'TERCERA', 'TERRITORIAL']):
                        category = line
                        break

        # Clean names for folder structure
        club_name = re.sub(r'[^\w\s-]', '', club_name).replace(' ', '_').upper()
        category = re.sub(r'[^\w\s.-]', '_', category).replace(' ', '_')
        team_name = re.sub(r'[^\w\s-]', '', team_name).replace(' ', '_').upper()

        return club_name, category, team_name

    except Exception as e:
        print(f"❌ Error getting team info: {e}")
        return None, None, None


def create_team_directory(club_name, category, team_id, team_name):
    """Create directory structure for the team"""
    team_folder_name = f"{team_id}_{team_name}"
    team_path = Path(club_name) / category / team_folder_name
    team_path.mkdir(parents=True, exist_ok=True)
    return team_path


def scrape_team(team_id, phase="tot"):
    """
    Main function to scrape a single team

    Args:
        team_id: Team ID to scrape
        phase: Competition phase (not used in this version, just for compatibility)

    Returns:
        Path to team folder, or None if failed
    """
    print(f"\n{'='*60}")
    print(f"Scraping Team: {team_id}")
    print(f"{'='*60}\n")

    # Step 1: Get team info
    club_name, category, team_name = get_team_info(team_id)
    if not all([club_name, category, team_name]):
        print(f"❌ Could not get team information")
        return None

    print(f"📋 Club: {club_name}")
    print(f"📋 Category: {category}")
    print(f"📋 Team: {team_name}")
    print()

    # Step 2: Create directory structure
    team_path = create_team_directory(club_name, category, team_id, team_name)
    print(f"📂 Created directory: {team_path}")
    print()

    # Step 3: Use existing matches_by_team.py to download matches
    print(f"⬇️  Fetching matches using matches_by_team.py...")
    try:
        result = subprocess.run(
            ["python3", "matches_by_team.py", club_name, str(team_id)],
            check=False
        )

        if result.returncode == 0:
            print(f"\n✅ Team {team_id} scraped successfully!")
            print(f"📂 Data saved to: {team_path}\n")
            return team_path
        else:
            print(f"\n⚠️  matches_by_team.py completed with warnings")
            return team_path

    except Exception as e:
        print(f"❌ Error running matches_by_team.py: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 team_scraper.py <team_id> [phase]")
        print("Example: python3 team_scraper.py 82618 tot")
        print("\nNote: phase parameter is ignored, included for compatibility")
        sys.exit(1)

    team_id = sys.argv[1]
    phase = sys.argv[2] if len(sys.argv) > 2 else "tot"

    result = scrape_team(team_id, phase)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)

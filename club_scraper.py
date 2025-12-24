import requests
from bs4 import BeautifulSoup
import os
import argparse
import re
import subprocess
import mysql.connector
from config_loader import config

BASE_URL = config.base_url
DB_CONFIG = config.db_config

def get_teams_from_club(club_id):
    """Fetches the list of teams and the correct club name given a club ID."""
    url = f"{BASE_URL}/club/{club_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Failed to retrieve data for club {club_id}")
        return [], f"Club_{club_id}"

    soup = BeautifulSoup(response.text, 'html.parser')

    teams = []
    club_name_tag = soup.find('h1', class_='notranslate')
    club_name = re.sub(r"[^\w\s]", "", club_name_tag.text.strip()).replace(" ", "_") if club_name_tag else f"Club_{club_id}"

    team_section = soup.find('div', class_='col-md-8 notranslate')
    if not team_section:
        print("❌ Could not find the teams section on the page.")
        return [], club_name

    team_blocks = team_section.find_all('div', class_='table-responsive')

    for block in team_blocks:
        category = block.text.split('|')[0].strip()
        team_links = block.find_all('a', class_='c-0')

        for link in team_links:
            scraped_team_id = link['href'].split('/')[-1]
            team_name = re.sub(r"[^\w\s]", "", link.text.strip()).replace(" ", "_")

            teams.append({
                'category': category,
                'team_name': f"{scraped_team_id}_{team_name}",
                'team_id': scraped_team_id,
                'team_id_extern': scraped_team_id  # Store the external ID (teamIdExtern)
            })

    return teams, club_name

def create_directory_structure(club_name, teams):
    """Creates the folder structure for the club and its teams inside the script's directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    club_dir = os.path.join(script_dir, club_name)
    os.makedirs(club_dir, exist_ok=True)

    for team in teams:
        category_dir = os.path.join(club_dir, team['category'].replace(" ", "_"))
        team_dir = os.path.join(category_dir, team['team_name'])
        os.makedirs(team_dir, exist_ok=True)
        print(f"📂 Created directory: {team_dir}")

def is_estadistiques_id_stored(team_id):
    """Checks if all estadistiques IDs for a team are already stored in MySQL."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM matches WHERE team_id = %s", (team_id,))
    result = cursor.fetchone()[0]

    conn.close()

    return result > 0  # Returns True if team has stored estadistiquesIDs

def download_matches_for_all_teams(club_name, teams, skip_downloads=False, skip_id_checks=False):
    """Calls matches_by_team.py for each team, only if matches or IDs are missing."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for team in teams:
        team_id = team['team_id']

        if skip_downloads:
            print(f"⏩ Skipping match downloads for {team['team_name']} (Flag: --skip-downloads)")
            continue

        if skip_id_checks and is_estadistiques_id_stored(team_id):
            print(f"⏩ Skipping estadistiquesID retrieval for {team['team_name']} (Flag: --skip-id-checks)")
            continue

        print(f"\n⬇️ Fetching matches for team {team_id} ({team['team_name']}) in {club_name}...")

        # Call matches_by_team.py
        subprocess.run(["python3", "matches_by_team.py", club_name, team_id], cwd=script_dir)

def generate_reports_for_all_teams(club_name, teams, phase):
    """Calls generate_excel.py for each team to create Excel reports."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    estadistiques_folder = os.path.join(script_dir, club_name, "estadistiques")
    os.makedirs(estadistiques_folder, exist_ok=True)

    for team in teams:
        team_id = team['team_id']
        print(f"\n📊 Generating Excel report for team {team_id} ({team['team_name']}) in {club_name}...")

        # Call generate_excel.py
        subprocess.run(["python3", "generate_excel.py", club_name, team_id, phase], cwd=script_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape a club's teams, download matches, and generate reports.")
    parser.add_argument("club_id", type=str, help="The ID of the club to scrape.")
    parser.add_argument("--skip-downloads", action="store_true", help="Skip downloading JSON match data.")
    parser.add_argument("--skip-id-checks", action="store_true", help="Skip retrieving estadistiquesID (if already stored in MySQL).")
    parser.add_argument("phase", nargs="?", default="tot", choices=["fase1", "fase2", "tot"], help="Phase: fase1 (Aug-Dec), fase2 (Jan-Jun), tot (default)")


    args = parser.parse_args()

    teams, club_name = get_teams_from_club(args.club_id)
    create_directory_structure(club_name, teams)

    # ✅ Skip downloading matches and ID checks if the flags are set
    download_matches_for_all_teams(club_name, teams, skip_downloads=args.skip_downloads, skip_id_checks=args.skip_id_checks)

    # ✅ Always generate reports
    generate_reports_for_all_teams(club_name, teams, args.phase)

    print("\n✅ Full process completed successfully!")

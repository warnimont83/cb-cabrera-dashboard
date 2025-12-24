import requests
import json
import sys
import os
from datetime import datetime
import warnings
from urllib3.exceptions import NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
from config_loader import config


def fetch_match_data(match_id, output_dir="."):
    # API URLs for matchStats and matchMoves
    api_url = config.api_url
    url_stats = f"{api_url}/getJsonWithMatchStats/{match_id}?currentSeason=true"
    url_moves = f"{api_url}/getJsonWithMatchMoves/{match_id}?currentSeason=true"

    # Fetch JSON data for both
    response_stats = requests.get(url_stats)
    response_moves = requests.get(url_moves)

    if response_stats.status_code == 200 and response_moves.status_code == 200:
        match_stats = response_stats.json()
        match_moves = response_moves.json()

        # Extract match details
        match_time_str = match_stats.get("time", "unknown_date")

        # Extract team names from "teams" section
        teams = match_stats.get("teams", [])
        if len(teams) >= 2:
            team1 = teams[0].get("name", "UnknownTeam1").replace(" ", "_")
            team2 = teams[1].get("name", "UnknownTeam2").replace(" ", "_")
        else:
            team1, team2 = "UnknownTeam1", "UnknownTeam2"

        # Convert date format from "Jan 18, 2025 10:00:00 AM" to "YYYYMMDD_HHMM"
        try:
            match_time = datetime.strptime(match_time_str, "%b %d, %Y %I:%M:%S %p")
            formatted_date = match_time.strftime("%Y%m%d_%H%M")
        except ValueError:
            formatted_date = "unknown_date"

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Generate filenames with full paths
        filename_stats = os.path.join(output_dir, f"{match_id}_{formatted_date}_{team1}_vs_{team2}_stats.json")
        filename_moves = os.path.join(output_dir, f"{match_id}_{formatted_date}_{team1}_vs_{team2}_moves.json")

        # Save JSONs to files
        with open(filename_stats, "w", encoding="utf-8") as file:
            json.dump(match_stats, file, indent=4)

        with open(filename_moves, "w", encoding="utf-8") as file:
            json.dump(match_moves, file, indent=4)

        print(f"Match data saved in {output_folder} as:")
        print(f" - {filename_stats}")
        print(f" - {filename_moves}")

    else:
        print(f"Failed to retrieve data. Status codes: Stats - {response_stats.status_code}, Moves - {response_moves.status_code}")

# Run script with match_id and optional output_folder
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_match.py <match_id> [output_folder]")
    else:
        match_id = sys.argv[1]
        output_folder = sys.argv[2] if len(sys.argv) > 2 else "."
        fetch_match_data(match_id, output_folder)

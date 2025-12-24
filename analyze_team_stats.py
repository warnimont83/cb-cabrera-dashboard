import os
import json
import argparse

def find_team_folder(main_folder, team_id):
    """Searches for the team folder based on the team ID in the directory structure."""
    base_path = os.path.join(os.getcwd(), main_folder)

    for root, dirs, _ in os.walk(base_path):
        for dir_name in dirs:
            if dir_name.startswith(team_id):
                return os.path.join(root, dir_name)

    print(f"Error: Could not find folder for team {team_id} in {base_path}")
    return None

def extract_player_stats(json_file, team_name):
    """Extracts and prints player stats for the given team from a JSON file."""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    match_date = data.get("time", "Unknown Date")
    teams = data.get("teams", [])

    # Find the correct team
    team_data = None
    for team in teams:
        if team_name.lower() in team["name"].lower():
            team_data = team
            break

    if not team_data:
        print(f"No stats found for team {team_name} in match on {match_date}")
        return

    print(f"\n🏀 Match Date: {match_date}")
    print(f"🔹 Team: {team_data['name']}")

    print("\n📊 Player Statistics:")
    print(f"{'Dorsal':<6} {'Player Name':<45} {'PTS':<5} {'2P':<6} {'3P':<8} {'FT':<8} {'FLS':<5}")
    print("-" * 95)

    for player in team_data.get("players", []):
        name = player["name"]
        dorsal = player["dorsal"]
        points = player["data"]["score"]
        two_made = player["data"]["shotsOfTwoSuccessful"]
        two_attempted = player["data"]["shotsOfTwoAttempted"]
        three_made = player["data"]["shotsOfThreeSuccessful"]
        three_attempted = player["data"]["shotsOfThreeAttempted"]
        ft_made = player["data"]["shotsOfOneSuccessful"]
        ft_attempted = player["data"]["shotsOfOneAttempted"]
        fouls = player["data"]["faults"]

        print(f"{dorsal:<6} {name:<45} {points:<5} {two_made}/{two_attempted:<6} {three_made}/{three_attempted:<8} {ft_made}/{ft_attempted:<8} {fouls:<5}")

def process_team_stats(main_folder, team_name):
    """Finds and processes all match JSON files for a given team."""
    # Find the correct team folder
    team_folder = find_team_folder(main_folder, team_name)
    if not team_folder:
        return

    print(f"Found team folder: {team_folder}")

    print(f"\n📂 Processing match files for team {team_name} in {team_folder}")

    # Find JSON files containing the team name in their filename
    json_files = [f for f in os.listdir(team_folder) if f.endswith("_stats.json")]

    if not json_files:
        print("No match statistics files found!")
        return

    for json_file in sorted(json_files):
        extract_player_stats(os.path.join(team_folder, json_file), main_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract player statistics from match JSON files.")
    parser.add_argument("main_folder", type=str, help="The main team folder (e.g., 'Cabrera').")
    parser.add_argument("team_id", type=str, help="The ID of the team to fetch matches for.")
    args = parser.parse_args()

    process_team_stats(args.main_folder, args.team_id)

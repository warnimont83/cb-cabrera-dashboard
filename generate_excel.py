import os
import json
import pandas as pd
import argparse
import re
from unidecode import unidecode

def extract_match_stats(json_file, club_name, team_id):
    """Extract player stats from a match JSON file for the given team."""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    match_date = data.get("time", "Unknown Date")
    score = data.get("score", [])
    local_score, visitor_score = (score[-1]["local"], score[-1]["visit"]) if score else ("-", "-")

    teams = data.get("teams", [])

    # ✅ Extract team name matching logic
    cleaned_club_name = club_name.replace("_", " ")
    club_keywords = {word for word in cleaned_club_name.lower().split() if word not in {"club", "basquet"}}

    # ✅ Normalize club name and team names for better matching
    cleaned_club_name = unidecode(club_name.replace("_", " ")).lower()
    club_keywords = {word for word in cleaned_club_name.split() if word not in {"club", "basquet"}}

    # ✅ Match team using teamIdExtern instead of text-based matching
    team_data = next((team for team in teams if str(team["teamIdExtern"]) == str(team_id)), None)

    if team_data is None:
        print(f"❌ No matching team found for club: {club_name}")
        return None, None, None

    match_stats = []
    for player in team_data.get("players", []):
        match_stats.append({
            "Jugador": player["name"],
            "Dorsal": int(player["dorsal"]),
            "Punts": pd.to_numeric(player["data"]["score"], errors="coerce"),
            "Minuts": pd.to_numeric(player["timePlayed"], errors="coerce"),
            "Faltes": pd.to_numeric(player["data"]["faults"], errors="coerce"),
            "Valoració": pd.to_numeric(player["data"]["valoration"], errors="coerce"),
            "Tirs Totals": pd.to_numeric(player["data"]["shotsOfOneAttempted"] + player["data"]["shotsOfTwoAttempted"] + player["data"]["shotsOfThreeAttempted"], errors="coerce"),
            "Tirs 1P": pd.to_numeric(player["data"]["shotsOfOneAttempted"], errors="coerce"),
            "Encerts 1P": pd.to_numeric(player["data"]["shotsOfOneSuccessful"], errors="coerce"),
            "Tirs 2P": pd.to_numeric(player["data"]["shotsOfTwoAttempted"], errors="coerce"),
            "Encerts 2P": pd.to_numeric(player["data"]["shotsOfTwoSuccessful"], errors="coerce"),
            "Tirs 3P": pd.to_numeric(player["data"]["shotsOfThreeAttempted"], errors="coerce"),
            "Encerts 3P": pd.to_numeric(player["data"]["shotsOfThreeSuccessful"], errors="coerce"),
        })

    # ✅ Extract match details
    local_team_id = data.get("localId", None)
    visitor_team_id = data.get("visitId", None)

    local_team = next((team["name"] for team in data["teams"] if team["teamIdIntern"] == local_team_id), "Unknown Local Team")
    visitor_team = next((team["name"] for team in data["teams"] if team["teamIdIntern"] == visitor_team_id), "Unknown Visitor Team")

    match_details = pd.DataFrame({
        "Jugador": ["Date", "Time", "Local Team", "Visitor Team", "Score"],
        "Punts": [match_date.split()[0], " ".join(match_date.split()[1:]), local_team, visitor_team, f"{local_score} - {visitor_score}"]
    })

    # ✅ Append match details at the bottom
    match_df = pd.concat([pd.DataFrame(match_stats), match_details], ignore_index=True)

    return match_date, f"{local_score} - {visitor_score}", match_df

def find_team_folder(club_name, team_id):
    """Search for the correct team folder based on the team ID inside the club folder."""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script location
    club_path = os.path.join(script_dir, club_name)

    for root, dirs, _ in os.walk(club_path):
        for dir_name in dirs:
            if dir_name.startswith(team_id):
                category_name = os.path.basename(root)  # Extract the category folder name
                return os.path.join(root, dir_name), dir_name, category_name

    print(f"❌ Error: Could not find folder for team {team_id} in {club_path}")
    return None, None

def generate_excel_report(club_name, team_id, phase="tot"):
    """Generate an Excel report and store it in {club_name}/estadistiques/ instead of inside the team folder."""
    team_folder, team_folder_name, category_name = find_team_folder(club_name, team_id)
    if not team_folder:
        return

    print(f"\n📂 Checking match files for team {team_folder_name} in {team_folder}")

    json_files = sorted([f for f in os.listdir(team_folder) if f.endswith("_stats.json")])
    if not json_files:
        print(f"✅ No new matches found for {team_folder_name}. Skipping report generation.")
        return  # ✅ Skip report generation if no new matches exist

    def get_json_month(filename):
        """Extracts the month (MM) from a filename that starts with match_id_YYYYMMDD_..."""
        try:
            # Format: {match_id}_{YYYYMMDD}_{...}_stats.json
            parts = filename.split("_")
            if len(parts) >= 2 and len(parts[1]) >= 6:
                return int(parts[1][4:6])  # Extract MM
        except:
            pass
        return None

    if phase == "fase1":
        json_files = [f for f in json_files if (get_json_month(f) is not None and 8 <= get_json_month(f) <= 12)]
    elif phase == "fase2":
        json_files = [f for f in json_files if (get_json_month(f) is not None and 1 <= get_json_month(f) <= 6)]


    # ✅ Ensure /estadistiques/ folder exists
    estadistiques_folder = os.path.join(os.path.dirname(os.path.dirname(team_folder)), "estadistiques")
    os.makedirs(estadistiques_folder, exist_ok=True)

    print(f"\n📊 Generating Excel report for team {team_folder_name} in {club_name}...")

    all_match_stats = []
    match_sheets = {}

    # ✅ Avoid duplicate sheets
    existing_sheets = set()

    for json_file in json_files:
        match_date, match_score, match_df = extract_match_stats(os.path.join(team_folder, json_file), club_name, team_id)
        if match_df is not None:
            sheet_name = f"J{len(existing_sheets) + 1}"

            # ✅ Skip if the sheet already exists
            if sheet_name in existing_sheets:
                print(f"⚠️ Sheet {sheet_name} already exists. Skipping duplicate entry.")
                continue

            existing_sheets.add(sheet_name)
            match_sheets[sheet_name] = match_df
            all_match_stats.append(match_df)

    if not all_match_stats:
        print("❌ No valid matches found. Skipping Excel generation.")
        return

    all_matches_df = pd.concat(all_match_stats, ignore_index=True)
    # ✅ Keep only real player rows (numeric Dorsal)
    player_rows = all_matches_df.copy()
    player_rows["Dorsal"] = pd.to_numeric(player_rows["Dorsal"], errors="coerce")
    player_rows = player_rows[player_rows["Dorsal"].notna()].copy()

    # ✅ Ensure numeric dtype for all stat columns
    numeric_cols = [
        "Punts", "Minuts", "Faltes", "Valoració",
        "Tirs Totals", "Tirs 1P", "Encerts 1P",
        "Tirs 2P", "Encerts 2P", "Tirs 3P", "Encerts 3P"
    ]
    for c in numeric_cols:
        if c in player_rows.columns:
            player_rows[c] = pd.to_numeric(player_rows[c], errors="coerce")

    # ✅ Group and calculate totals
    totals_df = player_rows.groupby(["Jugador", "Dorsal"], as_index=False)[numeric_cols].sum()
    totals_df.insert(2, "Partits", player_rows.groupby(["Jugador", "Dorsal"])["Punts"].count().values)
    totals_df = totals_df.sort_values(by="Dorsal").reset_index(drop=True)

    # ✅ Guard against division by zero
    totals_df["Partits"] = pd.to_numeric(totals_df["Partits"], errors="coerce")
    totals_df["Partits"].replace(0, pd.NA, inplace=True)

    # ✅ Compute averages safely
    mitges_df = totals_df[["Jugador", "Dorsal", "Partits"]].copy()
    mitges_df["Punts/partit"] = (totals_df["Punts"] / totals_df["Partits"]).round(1)
    mitges_df["Minuts/partit"] = (totals_df["Minuts"] / totals_df["Partits"]).round(1)
    mitges_df["Faltes/partit"] = (totals_df["Faltes"] / totals_df["Partits"]).round(1)
    mitges_df["Tirs/partit"] = (totals_df["Tirs Totals"] / totals_df["Partits"]).round(1)
    mitges_df["Valoració/partit"] = (totals_df["Valoració"] / totals_df["Partits"]).round(1)

    mitges_df = mitges_df.sort_values(by="Dorsal").reset_index(drop=True)

    # ✅ Store all Excel files in {club_name}/estadistiques/
    output_file = os.path.join(estadistiques_folder, f"{category_name}_{team_folder_name}_{phase}.xlsx")

    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        totals_df.to_excel(writer, sheet_name="TOTALS", index=False)
        mitges_df.to_excel(writer, sheet_name="MITGES", index=False)

        # ✅ Ensure columns are expanded AFTER sheets are created
        worksheet_totals = writer.sheets["TOTALS"]
        worksheet_mitges = writer.sheets["MITGES"]
        one_decimal_format = writer.book.add_format({
            "num_format": "0.0",
            "align": "center",
            "valign": "vcenter"
        })

        worksheet_totals.set_column("A:A", 35)  # Expand player name column in TOTALS
        writer.sheets["MITGES"].set_column("A:A", 35)  # ✅ Fix: Ensure MITGES column A expands

        # ✅ Apply formatting to all columns in MITGES
        # ✅ Apply decimal formatting only to columns O to S (0-based index 14 to 18)
        for col_num in range(3, mitges_df.shape[1]):
            worksheet_mitges.set_column(col_num, col_num, 16, one_decimal_format)

        # ✅ Expand column A (Jugador) in MITGES
        worksheet_mitges.set_column("A:A", 35)

        for sheet_name, df in match_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.sheets[sheet_name].set_column("A:A", 35)  # ✅ Expand player name column in all match sheets

    print(f"✅ Report saved in: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an Excel report for a basketball team.")
    parser.add_argument("club_name", type=str)
    parser.add_argument("team_id", type=str)
    parser.add_argument("phase", nargs="?", default="tot", choices=["fase1", "fase2", "tot"], help="Phase: fase1 (Aug-Dec), fase2 (Jan-Jun), tot (default)")
    args = parser.parse_args()

    generate_excel_report(args.club_name, args.team_id, args.phase)

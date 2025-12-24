import requests
from bs4 import BeautifulSoup
import mysql.connector
import argparse
import os
import subprocess
import warnings
from urllib3.exceptions import NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
from urllib.parse import urljoin, urlparse
from config_loader import config

BASE_URL = config.base_url
DB_CONFIG = config.db_config

def is_match_already_stored(team_id, match_url):
    """Checks if the match is already stored in the database."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM matches WHERE team_id = %s AND match_url = %s", (team_id, match_url))
    result = cursor.fetchone()[0]

    conn.close()

    return result > 0  # Returns True if match exists, False otherwise

def setup_database():
    """Ensures the database and table exist in MySQL."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INT AUTO_INCREMENT PRIMARY KEY,
            team_id INT NOT NULL,
            month INT NOT NULL,
            match_url TEXT NOT NULL,
            estadistiques_id VARCHAR(255) NOT NULL,
            UNIQUE (match_url(255))  -- Ensure no duplicate match URLs
        )
    ''')

    conn.commit()
    conn.close()

def store_match(team_id, month, match_url, estadistiques_id):
    """Stores a match entry in the MySQL database, avoiding duplicates."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO matches (team_id, month, match_url, estadistiques_id)
            VALUES (%s, %s, %s, %s)
        ''', (team_id, month, match_url, estadistiques_id))
        conn.commit()
    except mysql.connector.errors.IntegrityError:
        print(f"Duplicate entry skipped: {match_url}")

    conn.close()

def get_match_links(team_id, month):
    """Fetches match information links for a given team and month."""
    match_links = []

    url = f"{BASE_URL}/partits/calendari_equip_mensual/11/{team_id}/{month:02d}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"⚠️ Failed to retrieve calendar for team {team_id} in month {month}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find match information links
    info_cells = soup.find_all('td', class_='text-left')
    for cell in info_cells:
        info_link = cell.find('a', href=True)
        if info_link and 'llistatpartits' in info_link['href']:
            match_links.append(BASE_URL + info_link['href'])

    return match_links

def get_estadistiques_id(match_url):
    """Extract the estadístiques ID from a match page, handling alphanumeric IDs and different link variants."""
    try:
        resp = requests.get(
            match_url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0 (compatible; StatsBot/1.0)"}
        )
    except Exception as e:
        print(f"Request error for {match_url}: {e}")
        return None

    if resp.status_code != 200:
        print(f"Failed to retrieve match details: {match_url} (HTTP {resp.status_code})")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Find a link to /estadistiques/... (text or icon)
    link = None
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/estadistiques/" in href:
            link = a
            break
        # fallback: anchor with the stats icon inside
        img = a.find("img", src=True)
        if img and ("ico_stats" in img["src"]):
            link = a
            break

    if not link:
        print(f"No estadístiques link found in {match_url}")
        return None

    href = link.get("href", "")
    abs_href = urljoin(BASE_URL, href)

    # Extract the last non-empty path segment (the ID), even if alphanumeric
    parsed = urlparse(abs_href)
    parts = [p for p in parsed.path.split("/") if p]
    try:
        idx = parts.index("estadistiques")
        if idx + 1 < len(parts):
            estad_id = parts[idx + 1]
        else:
            # fallback to last segment if structure is unexpected
            estad_id = parts[-1]
    except ValueError:
        # No 'estadistiques' in path; fall back to last segment
        estad_id = parts[-1] if parts else None

    if not estad_id:
        print(f"Couldn't extract estadístiques ID from href: {abs_href} (match: {match_url})")
        return None

    return estad_id

def find_team_folder(club_folder_name, team_id):
    """Searches for the team folder based on the team ID inside the correct club folder."""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script location
    club_path = os.path.join(script_dir, club_folder_name)  # Use provided club folder name

    for root, dirs, _ in os.walk(club_path):
        for dir_name in dirs:
            if dir_name.startswith(team_id):
                return os.path.join(root, dir_name)

    print(f"❌ Error: Could not find folder for team {team_id} in {club_path}")
    return None

def download_match_json(match_id, save_dir):
    """Download the JSON for a match stats page, skipping if it already exists."""
    os.makedirs(save_dir, exist_ok=True)

    # Skip if a non-empty *_stats.json already exists for this match
    existing = [f for f in os.listdir(save_dir) if match_id in f and f.endswith("_stats.json")]
    if existing:
        path = os.path.join(save_dir, existing[0])
        try:
            if os.path.getsize(path) > 0:
                print(f"✅ JSON already exists for match {match_id}, skipping download.")
                return
        except OSError:
            pass

    print(f"⬇️ JSON missing or corrupted, downloading: {match_id}")

    # Call fetch_match.py <match_id> <save_dir>
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fetch_path = os.path.join(script_dir, "fetch_match.py")
    if not os.path.exists(fetch_path):
        print(f"❌ fetch_match.py not found at {fetch_path}")
        return

    try:
        subprocess.run(["python3", fetch_path, match_id, save_dir], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ fetch_match.py failed for {match_id}: {e}")

def get_stored_estadistiques_id(team_id, match_url):
    """Retrieves the estadistiques ID from MySQL if the match is already stored."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT estadistiques_id FROM matches WHERE team_id = %s AND match_url = %s", (team_id, match_url))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None  # Returns the estadistiques ID if found, else None

def json_exists(match_id, save_dir):
    """Checks if a JSON file containing match_id exists and is not empty."""
    if not os.path.exists(save_dir):
        return False  # Directory doesn't exist, JSON is missing

    # ✅ Search for any JSON file that contains match_id
    existing_files = [f for f in os.listdir(save_dir) if match_id in f and f.endswith("_stats.json")]

    if existing_files:
        json_path = os.path.join(save_dir, existing_files[0])  # Take the first matching file
        if os.path.getsize(json_path) > 0:
            return True  # JSON exists and is valid

    return False  # JSON missing or corrupted


def main(club_folder_name, team_id):
    setup_database()  # Ensure database and table exist

    # Find the correct team folder
    team_folder = find_team_folder(club_folder_name, team_id)
    if not team_folder:
        return

    print(f"✅ Found team folder: {team_folder}")

    for month in range(1, 13):  # ✅ Ensure all 12 months are checked
        print(f"\n📅 Checking Month: {month:02d}")
        match_links = get_match_links(team_id, month)

        if not match_links:
            print(f"⚠️ No matches found for month {month:02d}")
            continue

        for match_url in match_links:
            # ✅ Skip if match is already stored in MySQL
            # ✅ Check if JSON exists before skipping the match
            stored_estadistiques_id = get_stored_estadistiques_id(team_id, match_url)  # Get from MySQL
            if stored_estadistiques_id and json_exists(stored_estadistiques_id, team_folder):
                print(f"✅ JSON already exists for match {match_url}, skipping download.")
                continue

            estadistiques_id = get_estadistiques_id(match_url)
            if estadistiques_id:
                print(f"📊 Match: {match_url} → Estadístiques ID: {estadistiques_id}")
                store_match(team_id, month, match_url, estadistiques_id)  # Store in DB
                download_match_json(estadistiques_id, team_folder)  # Download JSON to team folder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch match statistics IDs for a team and download JSONs.")
    parser.add_argument("club_folder_name", type=str, help="The exact name of the club folder (e.g., 'CLUB_BASQUET_CABRERA').")
    parser.add_argument("team_id", type=str, help="The ID of the team to fetch matches for.")
    args = parser.parse_args()

    main(args.club_folder_name, args.team_id)

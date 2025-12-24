#!/usr/bin/env python3
"""
Basketball Statistics Web Dashboard
Flask application to visualize team and player statistics
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from pathlib import Path
from datetime import datetime
from config_loader import config
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
from season_utils import get_current_season, filter_matches_by_season, get_available_seasons, get_season_from_date
from translations import get_all_translations

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Memory optimization settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300  # Cache static files for 5 minutes

# Set default language to Catalan
DEFAULT_LANG = 'ca'

@app.context_processor
def inject_translations():
    """Make translations available to all templates"""
    lang = request.args.get('lang', DEFAULT_LANG)
    return {
        't': get_all_translations(lang),
        'lang': lang
    }

@app.template_filter('format_team_name')
def format_team_name(name):
    """Format team name: replace underscores with spaces and capitalize properly"""
    if not name:
        return name
    # Replace underscores with spaces
    formatted = name.replace('_', ' ')
    return formatted


def get_club_id_by_name(club_name):
    """Get club ID from config by club name"""
    # Try exact match first
    for club in config.clubs:
        if club['name'] == club_name:
            return club['id']

    # Try normalized match
    normalized_search = club_name.replace('_', ' ').upper()
    for club in config.clubs:
        normalized_club = club['name'].replace('_', ' ').upper()
        if normalized_club == normalized_search:
            return club['id']

    return None


def get_club_structure():
    """Get complete club/category/team structure"""
    structure = {}
    script_dir = Path(__file__).parent

    for club_dir in script_dir.iterdir():
        if not club_dir.is_dir() or club_dir.name.startswith('.'):
            continue

        # Skip special directories
        if club_dir.name in ['venv', 'templates', 'static', '__pycache__', 'docs', 'logs'] or club_dir.name.startswith('backup_'):
            continue

        club_name = club_dir.name
        club_id = get_club_id_by_name(club_name)
        structure[club_name] = {'categories': {}, 'club_id': club_id}

        for category_dir in club_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name == 'estadistiques':
                continue

            category_name = category_dir.name
            structure[club_name]['categories'][category_name] = {'teams': []}

            for team_dir in category_dir.iterdir():
                if not team_dir.is_dir():
                    continue

                json_files = list(team_dir.glob('*_stats.json'))
                if json_files:
                    structure[club_name]['categories'][category_name]['teams'].append({
                        'name': team_dir.name,
                        'path': str(team_dir.relative_to(script_dir)),
                        'match_count': len(json_files)
                    })

    return structure


def load_team_matches(team_path):
    """Load all match data for a team with full details"""
    team_dir = Path(__file__).parent / team_path
    matches = []

    for json_file in sorted(team_dir.glob('*_stats.json')):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                match_data = json.load(f)

                # Extract match info
                match_time = match_data.get('time', 'Unknown')
                teams = match_data.get('teams', [])

                local_team = teams[0] if len(teams) > 0 else {}
                visit_team = teams[1] if len(teams) > 1 else {}

                # Calculate final score from last score entry
                scores = match_data.get('score', [])
                final_score = scores[-1] if scores else {'local': 0, 'visit': 0}

                matches.append({
                    'file': json_file.name,
                    'date': match_time,
                    'local_team': local_team.get('name', 'Unknown'),
                    'visit_team': visit_team.get('name', 'Unknown'),
                    'local_score': final_score.get('local', 0),
                    'visit_score': final_score.get('visit', 0),
                    'data': match_data
                })
        except Exception as e:
            print(f"Error loading {json_file}: {e}")

    return matches


def get_all_cabrera_matches(selected_season='all'):
    """Get all matches from all CB Cabrera teams"""
    cabrera_club_name = "CLUB_BASQUET_CABRERA"
    structure = get_club_structure()

    if cabrera_club_name not in structure:
        return []

    all_matches = []
    cabrera_data = structure[cabrera_club_name]

    for category_name, category_data in cabrera_data['categories'].items():
        for team in category_data['teams']:
            matches = load_team_matches(team['path'])

            # Filter by season
            if selected_season != 'all':
                matches = filter_matches_by_season(matches, selected_season)

            # Add category and team info to each match
            for match in matches:
                match['cabrera_team'] = team['name']
                match['cabrera_category'] = category_name
                match['team_path'] = team['path']

            all_matches.extend(matches)

    # Sort by date (newest first)
    all_matches.sort(key=lambda x: x['date'], reverse=True)

    return all_matches


def extract_rival_teams(matches):
    """Extract unique rival teams from match data"""
    rivals = {}

    for match in matches:
        teams = match['data'].get('teams', [])

        # Find the rival team (not CB Cabrera)
        for team in teams:
            team_name = team.get('name', '')
            team_id = team.get('teamIdExtern')

            # Skip if this is a Cabrera team
            if 'CABRERA' in team_name.upper():
                continue

            if team_id not in rivals:
                rivals[team_id] = {
                    'id': team_id,
                    'name': team_name,
                    'matches_played': 0,
                    'wins_against_us': 0,
                    'losses_against_us': 0,
                    'total_points_scored': 0,
                    'total_points_conceded': 0,
                    'categories': set()
                }

            rival = rivals[team_id]
            rival['matches_played'] += 1
            rival['categories'].add(match.get('cabrera_category', 'Unknown'))

            # Determine if rival won
            is_local = (teams.index(team) == 0)
            if is_local:
                rival['total_points_scored'] += match['local_score']
                rival['total_points_conceded'] += match['visit_score']
                if match['local_score'] > match['visit_score']:
                    rival['wins_against_us'] += 1
                else:
                    rival['losses_against_us'] += 1
            else:
                rival['total_points_scored'] += match['visit_score']
                rival['total_points_conceded'] += match['local_score']
                if match['visit_score'] > match['local_score']:
                    rival['wins_against_us'] += 1
                else:
                    rival['losses_against_us'] += 1

    # Convert categories set to list
    for rival in rivals.values():
        rival['categories'] = list(rival['categories'])
        rival['avg_points_scored'] = round(rival['total_points_scored'] / rival['matches_played'], 1) if rival['matches_played'] > 0 else 0

    return list(rivals.values())


def aggregate_player_stats(matches, team_id):
    """Aggregate player statistics across all matches for a specific team"""
    players = {}

    for match in matches:
        teams = match['data'].get('teams', [])

        for team in teams:
            # Only process players from our team (match by teamIdExtern)
            if str(team.get('teamIdExtern')) != str(team_id):
                continue

            for player in team.get('players', []):
                name = player.get('name', 'Unknown')
                dorsal = player.get('dorsal', '')
                minutes_played = player.get('timePlayed', 0)

                # Skip this game if player didn't play (0 minutes)
                if minutes_played == 0:
                    continue

                key = f"{name}_{dorsal}"

                if key not in players:
                    players[key] = {
                        'name': name,
                        'dorsal': dorsal,
                        'games': 0,
                        'total_points': 0,
                        'total_minutes': 0,
                        'total_fouls': 0,
                        'total_valoration': 0,
                        'total_rebounds': 0,
                        'total_assists': 0,
                        'total_steals': 0,
                        'total_blocks': 0,
                        'total_1p_attempted': 0,
                        'total_1p_successful': 0,
                        'total_2p_attempted': 0,
                        'total_2p_successful': 0,
                        'total_3p_attempted': 0,
                        'total_3p_successful': 0,
                    }

                player_data = players[key]
                player_data['games'] += 1

                data = player.get('data', {})
                player_data['total_points'] += data.get('score', 0)
                player_data['total_minutes'] += minutes_played
                player_data['total_fouls'] += data.get('faults', 0)
                player_data['total_valoration'] += data.get('valoration', 0)
                player_data['total_rebounds'] += data.get('rebounds', 0)
                player_data['total_assists'] += data.get('assists', 0)
                player_data['total_steals'] += data.get('steals', 0)
                player_data['total_blocks'] += data.get('blocks', 0)
                player_data['total_1p_attempted'] += data.get('shotsOfOneAttempted', 0)
                player_data['total_1p_successful'] += data.get('shotsOfOneSuccessful', 0)
                player_data['total_2p_attempted'] += data.get('shotsOfTwoAttempted', 0)
                player_data['total_2p_successful'] += data.get('shotsOfTwoSuccessful', 0)
                player_data['total_3p_attempted'] += data.get('shotsOfThreeAttempted', 0)
                player_data['total_3p_successful'] += data.get('shotsOfThreeSuccessful', 0)

    # Calculate averages
    for player in players.values():
        games = player['games'] or 1
        player['avg_points'] = round(player['total_points'] / games, 1)
        player['avg_minutes'] = round(player['total_minutes'] / games, 1)
        player['avg_fouls'] = round(player['total_fouls'] / games, 1)
        player['avg_valoration'] = round(player['total_valoration'] / games, 1)
        player['avg_rebounds'] = round(player['total_rebounds'] / games, 1)
        player['avg_assists'] = round(player['total_assists'] / games, 1)
        player['avg_1p_attempted'] = round(player['total_1p_attempted'] / games, 1)
        player['avg_1p_successful'] = round(player['total_1p_successful'] / games, 1)

        # Calculate FG%
        total_fg_attempted = player['total_2p_attempted'] + player['total_3p_attempted']
        total_fg_made = player['total_2p_successful'] + player['total_3p_successful']
        player['fg_percentage'] = round((total_fg_made / total_fg_attempted * 100) if total_fg_attempted > 0 else 0, 1)

        # Calculate FT% (Free Throw Percentage)
        player['ft_percentage'] = round((player['total_1p_successful'] / player['total_1p_attempted'] * 100) if player['total_1p_attempted'] > 0 else 0, 1)

    players_list = list(players.values())

    # Check if rebounds/assists are tracked (if all players have 0, they're not tracked)
    has_rebounds = any(p['total_rebounds'] > 0 for p in players_list)
    has_assists = any(p['total_assists'] > 0 for p in players_list)

    # Check if field goals are properly tracked (if any player has more attempts than makes, they're tracked)
    # In youth categories, they often only record made shots, so attempts = makes
    has_fg_stats = any(
        (p['total_2p_attempted'] > p['total_2p_successful']) or
        (p['total_3p_attempted'] > p['total_3p_successful'])
        for p in players_list
    )

    return players_list, has_rebounds, has_assists, has_fg_stats


@app.route('/')
def index():
    """Home page - CB Cabrera teams dashboard"""
    selected_season = request.args.get('season', get_current_season())

    # Focus only on CB Cabrera
    cabrera_club_name = "CLUB_BASQUET_CABRERA"
    structure = get_club_structure()

    if cabrera_club_name not in structure:
        return "CB Cabrera data not found. Please run the scraper first.", 404

    cabrera_data = structure[cabrera_club_name]

    # Define custom category order (top to bottom as in federation)
    # Note: Using underscore format to match folder names
    category_order = [
        "C.C._PRIMERA_CATEGORIA_MASCULINA",
        "2A._TERRITORIAL_SÈNIOR_MASCULÍ",
        "C.C._SOTS-20_MASCULÍ_NIVELL_A-1",
        "C.C._JÚNIOR_MASCULÍ_NIVELL_A",
        "C.T._JÚNIOR_MASCULÍ_PROMOCIÓ",
        "C.T._CADET_MASCULÍ_PROMOCIÓ",
        "C.T._INFANTIL_MASCULÍ_PROMOCIÓ",
        "C.T._MINI_MASCULÍ",
        "C.T._MINI_MASCULÍ_1R._ANY",
        "C.T._PRE-MINI_MASCULÍ_1R._ANY",
        "2A._TERRITORIAL_SÈNIOR_FEMENÍ",
        "C.T._INFANTIL_FEMENÍ_PROMOCIÓ",
        "ESCOBOL_(LLIGA)"
    ]

    # Organize teams by category
    teams_by_category = {}
    all_matches = []

    for category_name, category_data in cabrera_data['categories'].items():
        teams_list = []
        for team in category_data['teams']:
            # Load team matches for stats
            matches = load_team_matches(team['path'])
            all_matches.extend(matches)

            # Filter by season if needed
            if selected_season != 'all':
                season_matches = filter_matches_by_season(matches, selected_season)
            else:
                season_matches = matches

            # Get team ID for player stats
            team_id = team['name'].split('_')[0] if '_' in team['name'] else None

            # Calculate win/loss record
            wins = 0
            losses = 0
            for match in season_matches:
                teams = match['data'].get('teams', [])
                for t in teams:
                    if str(t.get('teamIdExtern')) == str(team_id):
                        # Determine if this team is local or visitor
                        is_local = (teams.index(t) == 0)
                        if is_local:
                            if match['local_score'] > match['visit_score']:
                                wins += 1
                            else:
                                losses += 1
                        else:
                            if match['visit_score'] > match['local_score']:
                                wins += 1
                            else:
                                losses += 1
                        break

            # Get player count
            players, _, _, _ = aggregate_player_stats(season_matches, team_id)

            # Clean team display name
            display_name = ' '.join(team['name'].split('_')[1:]) if '_' in team['name'] else team['name']

            # Only show teams that have matches in the selected season
            if len(season_matches) > 0:
                teams_list.append({
                    'name': team['name'],
                    'path': team['path'],
                    'display_name': display_name,
                    'match_count': len(season_matches),
                    'player_count': len(players),
                    'record': {'wins': wins, 'losses': losses} if season_matches else None
                })

        if teams_list:
            # Sort teams by match count (descending), then by name
            teams_list.sort(key=lambda x: (-x['match_count'], x['display_name']))
            teams_by_category[category_name] = teams_list

    # Get available seasons from all matches
    available_seasons = get_available_seasons(all_matches)

    total_categories = len(teams_by_category)
    total_teams = sum(len(teams) for teams in teams_by_category.values())
    total_matches = sum(team['match_count'] for teams in teams_by_category.values() for team in teams)

    # Sort categories by custom order
    sorted_categories = []
    for cat in category_order:
        if cat in teams_by_category:
            sorted_categories.append((cat, teams_by_category[cat]))

    return render_template('cabrera_home.html',
                         teams_by_category=sorted_categories,
                         total_categories=total_categories,
                         total_teams=total_teams,
                         total_matches=total_matches,
                         selected_season=selected_season,
                         available_seasons=available_seasons,
                         current_season=get_current_season(),
                         title="CB Cabrera - Coaching Dashboard")


# Old club browsing route removed - now focused only on CB Cabrera
# @app.route('/club/<path:club_name>')
# def club_detail(club_name):
#     """Club detail page - show categories"""
#     # Removed for CB Cabrera-only focus


@app.route('/team/<path:team_path>')
def team_detail(team_path):
    """Team detail page with statistics and matches"""
    # Get season filter from query parameter
    selected_season = request.args.get('season', get_current_season())

    # Load all matches
    all_matches = load_team_matches(team_path)

    # Get available seasons
    available_seasons = get_available_seasons(all_matches)

    # Filter matches by season
    if selected_season == "all":
        matches = all_matches
    else:
        matches = filter_matches_by_season(all_matches, selected_season)

    # Get team info from path
    path_parts = Path(team_path).parts
    team_info = {
        'club': path_parts[0] if len(path_parts) >= 1 else 'Unknown',
        'category': path_parts[1] if len(path_parts) >= 2 else 'Unknown',
        'name': path_parts[2] if len(path_parts) >= 3 else 'Unknown'
    }

    # Extract team ID from folder name (e.g., "79391_TEAM_NAME" -> "79391")
    team_id = team_info['name'].split('_')[0] if '_' in team_info['name'] else None

    # Aggregate stats only for our team's players
    players, has_rebounds, has_assists, has_fg_stats = aggregate_player_stats(matches, team_id)

    # Sort players by total points
    players.sort(key=lambda x: x['total_points'], reverse=True)

    # Extract rivals for this specific team
    team_rivals = {}
    for match in matches:
        teams_in_match = match['data'].get('teams', [])

        for team in teams_in_match:
            rival_team_id = str(team.get('teamIdExtern'))
            rival_team_name = team.get('name', '')

            # Skip if this is our team
            if rival_team_id == str(team_id):
                continue

            # Skip if this is a Cabrera team
            if 'CABRERA' in rival_team_name.upper():
                continue

            if rival_team_id not in team_rivals:
                team_rivals[rival_team_id] = {
                    'id': rival_team_id,
                    'name': rival_team_name,
                    'matches': 0,
                    'wins': 0,
                    'losses': 0,
                    'points_for': 0,
                    'points_against': 0
                }

            rival = team_rivals[rival_team_id]
            rival['matches'] += 1

            # Determine result
            is_local = (teams_in_match.index(team) == 0)
            if is_local:
                rival_score = match['local_score']
                our_score = match['visit_score']
            else:
                rival_score = match['visit_score']
                our_score = match['local_score']

            rival['points_for'] += rival_score
            rival['points_against'] += our_score

            if rival_score > our_score:
                rival['wins'] += 1
            else:
                rival['losses'] += 1

    # Convert to list and sort by matches played
    rivals_list = list(team_rivals.values())
    rivals_list.sort(key=lambda x: x['matches'], reverse=True)

    # Load standings if available
    team_dir = Path(__file__).parent / team_path
    standings_file = team_dir / "standings.json"
    standings = None

    if standings_file.exists():
        try:
            with open(standings_file, 'r', encoding='utf-8') as f:
                standings = json.load(f)
        except Exception as e:
            print(f"Error loading standings: {e}")

    return render_template('team_new.html',
                         team_info=team_info,
                         team_path=team_path,
                         team_id=team_id,
                         players=players,
                         matches=matches,
                         match_count=len(matches),
                         rivals=rivals_list,
                         standings=standings,
                         has_rebounds=has_rebounds,
                         has_assists=has_assists,
                         has_fg_stats=has_fg_stats,
                         selected_season=selected_season,
                         available_seasons=available_seasons,
                         current_season=get_current_season(),
                         title=f"{team_info['name']} - {config.web_title}")


@app.route('/player/<path:team_path>/<player_name>/<player_dorsal>')
def player_detail(team_path, player_name, player_dorsal):
    """Individual player detail page"""
    # Get season filter
    selected_season = request.args.get('season', get_current_season())

    # Load all matches
    all_matches = load_team_matches(team_path)
    available_seasons = get_available_seasons(all_matches)

    # Filter by season
    if selected_season != "all":
        matches = filter_matches_by_season(all_matches, selected_season)
    else:
        matches = all_matches

    # Get team info
    path_parts = Path(team_path).parts
    team_info = {
        'club': path_parts[0],
        'category': path_parts[1],
        'name': path_parts[2]
    }
    team_id = team_info['name'].split('_')[0]

    # Collect player's game-by-game stats
    player_games = []

    for match in matches:
        teams = match['data'].get('teams', [])

        for team in teams:
            if str(team.get('teamIdExtern')) != str(team_id):
                continue

            for player in team.get('players', []):
                if player.get('name') == player_name and player.get('dorsal') == player_dorsal:
                    minutes = player.get('timePlayed', 0)
                    if minutes > 0:  # Only count games played
                        data = player.get('data', {})
                        player_games.append({
                            'date': match.get('date'),
                            'opponent': match.get('visit_team') if match.get('local_team') == team.get('name') else match.get('local_team'),
                            'score': f"{match.get('local_score')}-{match.get('visit_score')}",
                            'minutes': minutes,
                            'points': data.get('score', 0),
                            'fouls': data.get('faults', 0),
                            'valoration': data.get('valoration', 0),
                            'rebounds': data.get('rebounds', 0),
                            'assists': data.get('assists', 0),
                            'ft_made': data.get('shotsOfOneSuccessful', 0),
                            'ft_attempted': data.get('shotsOfOneAttempted', 0),
                            '2pt_made': data.get('shotsOfTwoSuccessful', 0),
                            '2pt_attempted': data.get('shotsOfTwoAttempted', 0),
                            '3pt_made': data.get('shotsOfThreeSuccessful', 0),
                            '3pt_attempted': data.get('shotsOfThreeAttempted', 0),
                        })

    # Calculate totals and averages
    if player_games:
        games_played = len(player_games)
        totals = {
            'games': games_played,
            'total_minutes': sum(g['minutes'] for g in player_games),
            'total_points': sum(g['points'] for g in player_games),
            'total_fouls': sum(g['fouls'] for g in player_games),
            'total_rebounds': sum(g['rebounds'] for g in player_games),
            'total_assists': sum(g['assists'] for g in player_games),
            'total_ft_made': sum(g['ft_made'] for g in player_games),
            'total_ft_attempted': sum(g['ft_attempted'] for g in player_games),
            'avg_minutes': round(sum(g['minutes'] for g in player_games) / games_played, 1),
            'avg_points': round(sum(g['points'] for g in player_games) / games_played, 1),
            'avg_fouls': round(sum(g['fouls'] for g in player_games) / games_played, 1),
            'avg_rebounds': round(sum(g['rebounds'] for g in player_games) / games_played, 1),
            'avg_assists': round(sum(g['assists'] for g in player_games) / games_played, 1),
        }

        # Calculate shooting percentages
        totals['ft_percentage'] = round((totals['total_ft_made'] / totals['total_ft_attempted'] * 100) if totals['total_ft_attempted'] > 0 else 0, 1)
    else:
        totals = {}

    return render_template('player.html',
                         player_name=player_name,
                         player_dorsal=player_dorsal,
                         team_info=team_info,
                         team_path=team_path,
                         player_games=player_games,
                         totals=totals,
                         selected_season=selected_season,
                         available_seasons=available_seasons,
                         title=f"{player_name} #{player_dorsal} - {config.web_title}")


@app.route('/calendar')
def calendar_view():
    """Calendar view - all CB Cabrera matches"""
    selected_season = request.args.get('season', get_current_season())

    # Get all Cabrera matches
    matches = get_all_cabrera_matches(selected_season)
    available_seasons = get_available_seasons(matches) if matches else []

    # Group matches by month
    matches_by_month = {}
    for match in matches:
        try:
            date_obj = datetime.strptime(match['date'].split('_')[0], "%b %d, %Y %I:%M:%S %p")
            month_key = date_obj.strftime("%Y-%m")
            month_name = date_obj.strftime("%B %Y")

            if month_key not in matches_by_month:
                matches_by_month[month_key] = {
                    'name': month_name,
                    'matches': []
                }

            matches_by_month[month_key]['matches'].append(match)
        except:
            continue

    # Sort months (newest first)
    sorted_months = sorted(matches_by_month.items(), reverse=True)

    return render_template('calendar.html',
                         matches_by_month=sorted_months,
                         total_matches=len(matches),
                         selected_season=selected_season,
                         available_seasons=available_seasons,
                         current_season=get_current_season(),
                         title="Calendar - CB Cabrera")


@app.route('/rivals')
def rivals_view():
    """Rivals analysis - all opponent teams"""
    selected_season = request.args.get('season', get_current_season())

    # Get all Cabrera matches
    matches = get_all_cabrera_matches(selected_season)
    available_seasons = get_available_seasons(matches) if matches else []

    # Extract rival teams
    rivals = extract_rival_teams(matches)

    # Sort by matches played (most frequent opponents first)
    rivals.sort(key=lambda x: x['matches_played'], reverse=True)

    return render_template('rivals.html',
                         rivals=rivals,
                         total_rivals=len(rivals),
                         selected_season=selected_season,
                         available_seasons=available_seasons,
                         current_season=get_current_season(),
                         title="Rival Teams - CB Cabrera")


@app.route('/rival/<rival_id>')
def rival_detail(rival_id):
    """Rival team detail - player statistics and match history"""
    selected_season = request.args.get('season', get_current_season())
    from_team = request.args.get('from_team')  # Which Cabrera team is scouting

    # Try to find the rival team's folder (if they've been scraped)
    base_dir = Path(__file__).parent
    rival_folders = list(base_dir.glob(f"**/{rival_id}_*"))

    if rival_folders:
        # Rival team has been scraped - show their full team page
        rival_folder = rival_folders[0]
        team_path = str(rival_folder.relative_to(base_dir))

        # Get full team data
        all_matches = load_team_matches(team_path)

        # Filter by season
        matches = []
        for match in all_matches:
            match_date = match['date']
            match_season = get_season_from_date(match_date)
            if selected_season == 'all' or match_season == selected_season:
                matches.append(match)

        players, has_rebounds, has_assists, has_fg_stats = aggregate_player_stats(matches, rival_id)
        players.sort(key=lambda x: x['total_points'], reverse=True)

        # Get team info
        parts = team_path.split('/')
        club_name = parts[0] if len(parts) > 0 else "Unknown"
        category = parts[1] if len(parts) > 1 else "Unknown"
        team_folder_name = parts[2] if len(parts) > 2 else f"{rival_id}_Unknown"
        team_name = team_folder_name.split('_', 1)[1] if '_' in team_folder_name else team_folder_name

        # Try to get better team name from match data
        if matches:
            teams = matches[0]['data'].get('teams', [])
            for team in teams:
                if str(team.get('teamIdExtern')) == str(rival_id):
                    team_name = team.get('name', team_name)
                    break

        # Load standings if available
        standings_file = rival_folder / "standings.json"
        standings = None
        if standings_file.exists():
            try:
                with open(standings_file, 'r', encoding='utf-8') as f:
                    standings = json.load(f)
            except Exception as e:
                print(f"Error loading standings: {e}")

        team_info = {
            'name': team_name,
            'club': club_name.replace('_', ' '),
            'category': category.replace('_', ' ')
        }

        return render_template('team_new.html',
                             team_info=team_info,
                             team_path=team_path,
                             team_id=rival_id,
                             players=players,
                             matches=matches,
                             match_count=len(matches),
                             rivals=[],  # Don't show rivals section for rival teams
                             standings=standings,
                             has_rebounds=has_rebounds,
                             has_assists=has_assists,
                             has_fg_stats=has_fg_stats,
                             selected_season=selected_season,
                             available_seasons=get_available_seasons(matches),
                             current_season=get_current_season(),
                             title=f"{team_name} (Rival Analysis)",
                             is_rival_view=True,
                             from_team=from_team)
    else:
        # Rival hasn't been scraped yet - show limited data from Cabrera matches only
        all_matches = get_all_cabrera_matches(selected_season)

        rival_matches = []
        rival_name = "Unknown"

        for match in all_matches:
            teams = match['data'].get('teams', [])
            for team in teams:
                if str(team.get('teamIdExtern')) == str(rival_id):
                    rival_name = team.get('name', 'Unknown')
                    rival_matches.append(match)
                    break

        players, has_rebounds, has_assists, has_fg_stats = aggregate_player_stats(rival_matches, rival_id)
        players.sort(key=lambda x: x['total_points'], reverse=True)

        return render_template('rival_detail.html',
                             rival_name=rival_name,
                             rival_id=rival_id,
                             players=players,
                             matches=rival_matches,
                             match_count=len(rival_matches),
                             has_rebounds=has_rebounds,
                             has_assists=has_assists,
                             has_fg_stats=has_fg_stats,
                             selected_season=selected_season,
                             from_team=from_team,
                             title=f"{rival_name} - Rival Analysis (Limited Data)",
                             is_scraped=False)


@app.route('/match/<path:team_path>/<match_file>')
def match_detail(team_path, match_file):
    """Individual match detail page"""
    team_dir = Path(__file__).parent / team_path
    json_file = team_dir / match_file

    if not json_file.exists():
        return "Match not found", 404

    with open(json_file, 'r', encoding='utf-8') as f:
        match_data = json.load(f)

    # Get team info
    path_parts = Path(team_path).parts
    team_info = {
        'club': path_parts[0],
        'category': path_parts[1],
        'name': path_parts[2]
    }

    teams = match_data.get('teams', [])
    local_team = teams[0] if len(teams) > 0 else {}
    visit_team = teams[1] if len(teams) > 1 else {}

    # Get final score
    scores = match_data.get('score', [])
    final_score = scores[-1] if scores else {'local': 0, 'visit': 0}

    return render_template('match.html',
                         match_data=match_data,
                         team_info=team_info,
                         team_path=team_path,
                         local_team=local_team,
                         visit_team=visit_team,
                         final_score=final_score,
                         title=f"{local_team.get('name', 'Team')} vs {visit_team.get('name', 'Team')}")


if __name__ == '__main__':
    host = config.web_host
    port = config.web_port
    print(f"Starting web dashboard at http://{host}:{port}")
    app.run(host=host, port=port, debug=True)

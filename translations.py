#!/usr/bin/env python3
"""
Translation strings for the Basketball Dashboard
Supports Catalan (ca) and English (en)
"""

translations = {
    'ca': {
        # Navigation
        'home': 'Inici',
        'teams': 'Equips',
        'rivals': 'Rivals',
        'statistics': 'Estadístiques',

        # Team page
        'team': 'Equip',
        'category': 'Categoria',
        'season': 'Temporada',
        'all_seasons': 'Totes les temporades',
        'current_season': 'Temporada actual',
        'matches': 'Partits',
        'players': 'Jugadors',
        'player': 'Jugador',
        'rivals': 'Rivals',
        'league_standings': 'Classificació de la lliga',
        'position': 'Posició',
        'team_name': 'Nom de l\'equip',
        'played': 'J',
        'wins': 'V',
        'losses': 'D',
        'points_for': 'PF',
        'points_against': 'PC',
        'points': 'Punts',
        'total_points': 'Punts totals',

        # Player stats
        'player_statistics': 'Estadístiques dels jugadors',
        'number': 'Núm.',
        'games': 'Partits',
        'ppg': 'PPP',  # Punts per partit
        'mpg': 'MPP',  # Minuts per partit
        'rpg': 'RPP',  # Rebots per partit
        'apg': 'APP',  # Assistències per partit
        'fouls': 'Faltes',
        'ft_percentage': '% TL',  # Tirs lliures
        'fg_percentage': '% TC',  # Tirs de camp
        'rating': 'Valoració',
        'total': 'Total',
        'average': 'Mitjana',
        'minutes': 'Minuts',
        'rebounds': 'Rebots',
        'assists': 'Assistències',

        # Match details
        'match_history': 'Historial de partits',
        'match_details': 'Detalls del partit',
        'date': 'Data',
        'local': 'Local',
        'visitor': 'Visitant',
        'final_score': 'Resultat final',
        'quarter': 'Quart',
        'period': 'Període',
        'we_won': 'Hem guanyat',
        'we_lost': 'Hem perdut',
        'vs': 'vs',

        # Rivals
        'rival_teams': 'Equips rivals',
        'scout_team': 'Analitzar equip',
        'matches_against_us': 'Partits contra nosaltres',
        'wins_against_us': 'Victòries contra nosaltres',
        'avg_points': 'Punts mitjans',
        'opponent_analysis': 'Anàlisi de l\'oponent',
        'rival_detail': 'Detall del rival',
        'players_tracked': 'Jugadors registrats',
        'total_points_scored': 'Punts totals anotats',

        # General
        'back': 'Enrere',
        'back_to_teams': 'Tornar als equips',
        'back_to_rivals': 'Tornar als rivals',
        'loading': 'Carregant...',
        'no_data': 'No hi ha dades disponibles',
        'updated': 'Actualitzat',
        'club': 'Club',
        'filter_by_season': 'Filtrar per temporada',
        'sort_by': 'Ordenar per',
        'search': 'Cercar',

        # Stats headers
        'team_statistics': 'Estadístiques de l\'equip',
        'player_performance': 'Rendiment dels jugadors',
        'match_summary': 'Resum del partit',
        'competition': 'Competició',

        # Messages
        'no_matches': 'No s\'han trobat partits',
        'no_players': 'No s\'han trobat jugadors',
        'no_rivals': 'No s\'han trobat rivals',
        'complete_data': 'Dades completes disponibles',
        'limited_data': 'Dades limitades',

        # Dashboard
        'dashboard_title': 'Tauler de Bàsquet CB Cabrera',
        'welcome': 'Benvingut',
        'select_team': 'Selecciona un equip',
        'select_category': 'Selecciona una categoria',
        'categories': 'Categories',
        'matches_tracked': 'Partits registrats',
        'quick_access': 'Accés ràpid',
        'calendar': 'Calendari',
        'view_all_matches': 'Veure tots els partits',
        'scout_opponents': 'Analitzar rivals',
        'club_statistics': 'Estadístiques del club',
        'overall_performance': 'Rendiment general',
        'current': 'Actual',
        'basketball_stats': 'Estadístiques de Bàsquet',

        # Time
        'last_updated': 'Última actualització',
        'today': 'Avui',
        'yesterday': 'Ahir',

        # Actions
        'view_details': 'Veure detalls',
        'view_match': 'Veure partit',
        'view_stats': 'Veure estadístiques',
        'download': 'Descarregar',
        'export': 'Exportar',

        # Stats abbreviations (full names)
        'ppg_full': 'Punts per partit',
        'mpg_full': 'Minuts per partit',
        'rpg_full': 'Rebots per partit',
        'apg_full': 'Assistències per partit',
        'ft_full': 'Tirs lliures',
        'fg_full': 'Tirs de camp',

        # Warnings
        'warning_limited_data': '⚠️ Dades limitades: Només es mostren partits contra CB Cabrera.',
        'warning_scrape_needed': 'Per veure estadístiques completes (tots els partits, classificació completa), executa:',

        # Footer
        'powered_by': 'Desenvolupat amb',
        'data_source': 'Font de dades',
        'federation': 'Federació Catalana de Bàsquet',
    },
    'en': {
        # Navigation
        'home': 'Home',
        'teams': 'Teams',
        'rivals': 'Rivals',
        'statistics': 'Statistics',

        # Team page
        'team': 'Team',
        'category': 'Category',
        'season': 'Season',
        'all_seasons': 'All seasons',
        'current_season': 'Current season',
        'matches': 'Matches',
        'players': 'Players',
        'player': 'Player',
        'rivals': 'Rivals',
        'league_standings': 'League standings',
        'position': 'Position',
        'team_name': 'Team name',
        'played': 'P',
        'wins': 'W',
        'losses': 'L',
        'points_for': 'PF',
        'points_against': 'PA',
        'points': 'Points',
        'total_points': 'Total points',

        # Player stats
        'player_statistics': 'Player statistics',
        'number': '#',
        'games': 'Games',
        'ppg': 'PPG',
        'mpg': 'MPG',
        'rpg': 'RPG',
        'apg': 'APG',
        'fouls': 'Fouls',
        'ft_percentage': 'FT%',
        'fg_percentage': 'FG%',
        'rating': 'Rating',
        'total': 'Total',
        'average': 'Average',
        'minutes': 'Minutes',
        'rebounds': 'Rebounds',
        'assists': 'Assists',

        # Match details
        'match_history': 'Match history',
        'match_details': 'Match details',
        'date': 'Date',
        'local': 'Home',
        'visitor': 'Away',
        'final_score': 'Final score',
        'quarter': 'Quarter',
        'period': 'Period',
        'we_won': 'We won',
        'we_lost': 'We lost',
        'vs': 'vs',

        # Rivals
        'rival_teams': 'Rival teams',
        'scout_team': 'Scout team',
        'matches_against_us': 'Matches against us',
        'wins_against_us': 'Wins against us',
        'avg_points': 'Avg points',
        'opponent_analysis': 'Opponent analysis',
        'rival_detail': 'Rival detail',
        'players_tracked': 'Players tracked',
        'total_points_scored': 'Total points scored',

        # General
        'back': 'Back',
        'back_to_teams': 'Back to teams',
        'back_to_rivals': 'Back to rivals',
        'loading': 'Loading...',
        'no_data': 'No data available',
        'updated': 'Updated',
        'club': 'Club',
        'filter_by_season': 'Filter by season',
        'sort_by': 'Sort by',
        'search': 'Search',

        # Stats headers
        'team_statistics': 'Team statistics',
        'player_performance': 'Player performance',
        'match_summary': 'Match summary',
        'competition': 'Competition',

        # Messages
        'no_matches': 'No matches found',
        'no_players': 'No players found',
        'no_rivals': 'No rivals found',
        'complete_data': 'Complete data available',
        'limited_data': 'Limited data',

        # Dashboard
        'dashboard_title': 'CB Cabrera Basketball Dashboard',
        'welcome': 'Welcome',
        'select_team': 'Select a team',
        'select_category': 'Select a category',
        'categories': 'Categories',
        'matches_tracked': 'Matches tracked',
        'quick_access': 'Quick access',
        'calendar': 'Calendar',
        'view_all_matches': 'View all matches',
        'scout_opponents': 'Scout opponents',
        'club_statistics': 'Club statistics',
        'overall_performance': 'Overall performance',
        'current': 'Current',
        'basketball_stats': 'Basketball Stats',

        # Time
        'last_updated': 'Last updated',
        'today': 'Today',
        'yesterday': 'Yesterday',

        # Actions
        'view_details': 'View details',
        'view_match': 'View match',
        'view_stats': 'View statistics',
        'download': 'Download',
        'export': 'Export',

        # Stats abbreviations (full names)
        'ppg_full': 'Points per game',
        'mpg_full': 'Minutes per game',
        'rpg_full': 'Rebounds per game',
        'apg_full': 'Assists per game',
        'ft_full': 'Free throws',
        'fg_full': 'Field goals',

        # Warnings
        'warning_limited_data': '⚠️ Limited data: Only showing matches against CB Cabrera.',
        'warning_scrape_needed': 'To see complete statistics (all matches, full league standings), run:',

        # Footer
        'powered_by': 'Powered by',
        'data_source': 'Data source',
        'federation': 'Catalan Basketball Federation',
    }
}

def get_translation(key, lang='ca'):
    """Get translation for a key in the specified language"""
    return translations.get(lang, translations['ca']).get(key, key)

def get_all_translations(lang='ca'):
    """Get all translations for a language"""
    return translations.get(lang, translations['ca'])

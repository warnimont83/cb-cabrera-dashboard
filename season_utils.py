"""
Season utility functions for basketball statistics
Handles season calculation and filtering (Sept-June)
"""

from datetime import datetime
from typing import List, Dict, Any


def get_season_from_date(date_str: str) -> str:
    """
    Get basketball season from date string.
    Season runs from September to June (e.g., 2025-26)

    Args:
        date_str: Date string like "Oct 5, 2024 4:00:00 PM" or "20241005"

    Returns:
        Season string like "2024-25" or "2025-26"
    """
    try:
        # Try parsing various date formats
        for fmt in ["%b %d, %Y %I:%M:%S %p", "%Y%m%d", "%Y-%m-%d"]:
            try:
                date = datetime.strptime(date_str.split('_')[0] if '_' in date_str else date_str, fmt)
                break
            except ValueError:
                continue
        else:
            # If parsing fails, try to extract year from string
            import re
            year_match = re.search(r'20\d{2}', date_str)
            if year_match:
                year = int(year_match.group())
                month = 9  # Default to September
            else:
                return "Unknown"

        year = date.year
        month = date.month

        # If month is Sept-Dec, season is current_year/next_year
        # If month is Jan-June, season is previous_year/current_year
        # If month is July-Aug, it's off-season (use previous season)

        if month >= 9:  # Sept-Dec
            return f"{year}-{str(year + 1)[-2:]}"
        elif month <= 6:  # Jan-June
            return f"{year - 1}-{str(year)[-2:]}"
        else:  # July-Aug (off-season)
            return f"{year - 1}-{str(year)[-2:]}"

    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return "Unknown"


def get_current_season() -> str:
    """
    Get current basketball season based on today's date.

    Returns:
        Season string like "2025-26"
    """
    today = datetime.now()
    return get_season_from_date(today.strftime("%b %d, %Y %I:%M:%S %p"))


def filter_matches_by_season(matches: List[Dict[str, Any]], season: str) -> List[Dict[str, Any]]:
    """
    Filter matches to only include those from specified season.

    Args:
        matches: List of match dictionaries
        season: Season string like "2025-26" or "all"

    Returns:
        Filtered list of matches
    """
    if season == "all":
        return matches

    filtered = []
    for match in matches:
        match_date = match.get('date', '')
        match_season = get_season_from_date(match_date)

        if match_season == season:
            filtered.append(match)

    return filtered


def get_available_seasons(matches: List[Dict[str, Any]]) -> List[str]:
    """
    Get list of unique seasons from match data.

    Args:
        matches: List of match dictionaries

    Returns:
        Sorted list of season strings (newest first)
    """
    seasons = set()

    for match in matches:
        match_date = match.get('date', '')
        season = get_season_from_date(match_date)
        if season != "Unknown":
            seasons.add(season)

    # Sort by season (newest first)
    return sorted(list(seasons), reverse=True)


if __name__ == "__main__":
    # Test the functions
    test_dates = [
        "Oct 5, 2024 4:00:00 PM",
        "Jan 15, 2025 6:00:00 PM",
        "Sep 1, 2025 5:00:00 PM",
        "June 30, 2026 7:00:00 PM",
    ]

    print("Current season:", get_current_season())
    print("\nTest dates:")
    for date in test_dates:
        season = get_season_from_date(date)
        print(f"  {date} → Season {season}")

#!/usr/bin/env python3
"""
Clean up duplicate team folders
Removes generic "TEAM_xxxxx" folders when a properly named folder exists for the same team ID
"""

import os
from pathlib import Path
import shutil

def find_duplicate_teams():
    """Find teams that have both generic and properly named folders"""
    club_dir = Path("CLUB_BASQUET_CABRERA")

    duplicates = []

    for category_dir in club_dir.iterdir():
        if not category_dir.is_dir():
            continue

        # Track team IDs in this category
        teams_by_id = {}

        for team_dir in category_dir.iterdir():
            if not team_dir.is_dir():
                continue

            team_name = team_dir.name

            # Extract team ID (first part before _)
            parts = team_name.split('_')
            if not parts[0].isdigit():
                continue

            team_id = parts[0]

            # Check if this is a generic name or proper name
            is_generic = '_TEAM_' in team_name

            if team_id not in teams_by_id:
                teams_by_id[team_id] = []

            teams_by_id[team_id].append({
                'path': team_dir,
                'name': team_name,
                'is_generic': is_generic
            })

        # Find duplicates (same team ID with both generic and proper names)
        for team_id, folders in teams_by_id.items():
            if len(folders) > 1:
                # Check if we have both generic and proper names
                generic_folders = [f for f in folders if f['is_generic']]
                proper_folders = [f for f in folders if not f['is_generic']]

                if generic_folders and proper_folders:
                    duplicates.append({
                        'team_id': team_id,
                        'category': category_dir.name,
                        'generic': generic_folders,
                        'proper': proper_folders
                    })

    return duplicates

def cleanup_duplicates(duplicates, dry_run=True):
    """Remove generic-named duplicates, keeping properly named folders"""

    print(f"\n{'='*60}")
    print(f"{'DRY RUN - No files will be deleted' if dry_run else 'LIVE RUN - Deleting files'}")
    print(f"{'='*60}\n")

    for dup in duplicates:
        print(f"\nTeam ID: {dup['team_id']}")
        print(f"Category: {dup['category']}")
        print(f"  Keeping: {dup['proper'][0]['name']}")

        for generic in dup['generic']:
            print(f"  Removing: {generic['name']}")

            if not dry_run:
                try:
                    shutil.rmtree(generic['path'])
                    print(f"    ✅ Deleted")
                except Exception as e:
                    print(f"    ❌ Error: {e}")

    print(f"\n{'='*60}")
    print(f"Total duplicates found: {len(duplicates)}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    import sys

    # Check for --confirm flag
    auto_confirm = '--confirm' in sys.argv

    print("🔍 Scanning for duplicate team folders...")
    duplicates = find_duplicate_teams()

    if not duplicates:
        print("✅ No duplicates found!")
        sys.exit(0)

    # Show what would be deleted (dry run)
    cleanup_duplicates(duplicates, dry_run=True)

    # Ask for confirmation (or auto-confirm)
    if auto_confirm:
        print("\n--confirm flag detected, proceeding with deletion...")
        cleanup_duplicates(duplicates, dry_run=False)
        print("\n✅ Cleanup complete!")
    else:
        response = input("\nProceed with deletion? (yes/no): ")

        if response.lower() == 'yes':
            cleanup_duplicates(duplicates, dry_run=False)
            print("\n✅ Cleanup complete!")
        else:
            print("\n❌ Cancelled")

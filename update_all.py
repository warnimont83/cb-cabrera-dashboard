#!/usr/bin/env python3
"""
Update all clubs configured in config.yaml
This script reads the configuration and runs the scraper for all configured clubs
"""

import subprocess
import sys
from config_loader import config


def main():
    """Main function to update all configured clubs"""
    clubs = config.clubs

    if not clubs:
        print("❌ No clubs configured in config.yaml")
        print("Please add clubs to your configuration file")
        return 1

    print(f"📋 Found {len(clubs)} club(s) in configuration")
    print()

    phase = config.default_phase
    failed_clubs = []

    for i, club in enumerate(clubs, 1):
        club_id = club.get("id")
        club_name = club.get("name", f"Club {club_id}")

        print(f"{'='*60}")
        print(f"[{i}/{len(clubs)}] Processing: {club_name} (ID: {club_id})")
        print(f"{'='*60}")

        try:
            # Run club_scraper.py for this club
            result = subprocess.run(
                ["python3", "club_scraper.py", str(club_id), phase],
                check=True
            )
            print(f"✅ {club_name} completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error processing {club_name}: {e}")
            failed_clubs.append(club_name)
        except Exception as e:
            print(f"❌ Unexpected error for {club_name}: {e}")
            failed_clubs.append(club_name)

        print()

    # Summary
    print(f"{'='*60}")
    print("📊 Summary")
    print(f"{'='*60}")
    print(f"Total clubs: {len(clubs)}")
    print(f"Successful: {len(clubs) - len(failed_clubs)}")
    print(f"Failed: {len(failed_clubs)}")

    if failed_clubs:
        print()
        print("Failed clubs:")
        for club in failed_clubs:
            print(f"  - {club}")
        return 1

    print()
    print("✅ All clubs updated successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

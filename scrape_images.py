#!/usr/bin/env python3
"""
Image scraper for club logos and team photos
Downloads images from basquetcatala.cat
"""

import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
from config_loader import config
import hashlib


def download_image(url, save_path):
    """Download an image from URL to save_path"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False


def get_club_logo(club_id, club_name):
    """Scrape and download club logo"""
    url = f"{config.base_url}/club/{club_id}"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find club logo - it's usually the image with the club name in alt text
        images = soup.find_all('img')
        for img in images:
            alt = img.get('alt', '')
            src = img.get('src', '')

            # Look for cloudfront images (club logos)
            if 'cloudfront' in src and club_name.upper() in alt.upper():
                return src

            # Alternative: look for images with club name in alt
            if club_name.upper() in alt.upper() and 'fcbq' not in src.lower():
                return src

        # If not found, try the first cloudfront image
        for img in images:
            src = img.get('src', '')
            if 'cloudfront' in src:
                return src

    except Exception as e:
        print(f"Error scraping club {club_id}: {e}")

    return None


def scrape_all_club_logos():
    """Scrape logos for all configured clubs"""
    # Create images directory
    images_dir = Path('static/images/clubs')
    images_dir.mkdir(parents=True, exist_ok=True)

    print("🎨 Scraping club logos...")
    print("=" * 60)

    clubs = config.clubs
    success_count = 0

    for club in clubs:
        club_id = club.get('id')
        club_name = club.get('name')

        print(f"\n📸 {club_name} (ID: {club_id})")

        # Get logo URL
        logo_url = get_club_logo(club_id, club_name)

        if logo_url:
            # Create filename from club ID
            extension = logo_url.split('.')[-1].split('?')[0]
            if extension not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                extension = 'jpg'

            filename = f"{club_id}.{extension}"
            save_path = images_dir / filename

            # Download image
            if download_image(logo_url, save_path):
                print(f"  ✅ Logo saved: {save_path}")
                success_count += 1
            else:
                print(f"  ❌ Failed to download: {logo_url}")
        else:
            print(f"  ⚠️  Logo not found")

    print("\n" + "=" * 60)
    print(f"✅ Downloaded {success_count}/{len(clubs)} club logos")
    print(f"📁 Images saved in: {images_dir}")


def scrape_team_photos():
    """
    Try to scrape team photos (if available)
    Note: Most teams don't have public player photos for privacy/youth protection
    """
    print("\n🔍 Checking for team photos...")
    print("⚠️  Note: Player photos are often not publicly available for youth teams")

    # This is a placeholder - team photos are generally not available
    # on the public website for privacy reasons

    clubs = config.clubs
    for club in clubs:
        for team in club.get('teams', []):
            team_id = team.get('id')
            team_url = f"{config.base_url}/equip/{team_id}"

            try:
                response = requests.get(team_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Look for player roster images
                player_images = soup.find_all('img', class_='player-photo')

                if player_images:
                    print(f"  Found {len(player_images)} player photos for team {team_id}")
                    # Could download these if needed

            except Exception as e:
                pass  # Silently fail - most teams won't have photos


if __name__ == "__main__":
    print("🏀 Basketball Image Scraper")
    print("=" * 60)

    # Scrape club logos
    scrape_all_club_logos()

    # Optional: try to scrape team photos
    # scrape_team_photos()

    print("\n✅ Image scraping complete!")
    print("💡 Tip: Run this script periodically to update club logos")

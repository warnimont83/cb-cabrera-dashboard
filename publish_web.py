#!/usr/bin/env python3
"""
Static site generator for basketball statistics
Generates static HTML files that can be deployed to GitHub Pages, Netlify, etc.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from config_loader import config
from web_dashboard import find_all_teams, load_team_data, aggregate_player_stats


def generate_static_site(output_dir="docs"):
    """Generate static HTML site for statistics"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Copy CSS
    css_dir = output_path / "css"
    css_dir.mkdir(exist_ok=True)

    # Copy static CSS file
    import shutil
    if Path("static/css/style.css").exists():
        shutil.copy("static/css/style.css", css_dir / "style.css")

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))

    # Get all teams
    teams = find_all_teams()

    # Generate index page
    template = env.get_template('index_static.html')
    html = template.render(
        teams=teams,
        title=config.web_title,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    with open(output_path / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Generated index.html")

    # Generate team pages
    team_template = env.get_template('team_static.html')

    for team in teams:
        matches = load_team_data(team['path'])
        players = aggregate_player_stats(matches)
        players.sort(key=lambda x: x['total_points'], reverse=True)

        path_parts = Path(team['path']).parts
        team_info = {
            'club': path_parts[-3] if len(path_parts) >= 3 else 'Unknown',
            'category': path_parts[-2] if len(path_parts) >= 2 else 'Unknown',
            'name': path_parts[-1] if len(path_parts) >= 1 else 'Unknown'
        }

        # Create team directory
        team_dir = output_path / team_info['club'] / team_info['category']
        team_dir.mkdir(parents=True, exist_ok=True)

        html = team_template.render(
            team_info=team_info,
            players=players,
            match_count=len(matches),
            title=f"{team_info['name']} - {config.web_title}",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        team_file = team_dir / f"{team_info['name']}.html"
        with open(team_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ Generated {team_file}")

    print(f"\n🎉 Static site generated in '{output_dir}/'")
    print(f"Total pages: {len(teams) + 1}")
    print(f"\nTo deploy:")
    print(f"  - GitHub Pages: Push '{output_dir}/' to gh-pages branch")
    print(f"  - Netlify: Deploy '{output_dir}/' directory")
    print(f"  - Local: Open '{output_dir}/index.html' in a browser")


if __name__ == "__main__":
    generate_static_site()

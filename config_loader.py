"""
Configuration loader for Basketball Statistics Scraper
Loads settings from config.yaml and .env files
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management class"""

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize configuration from YAML file"""
        self.config_path = Path(config_path)
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                "Please create config.yaml based on config.yaml.example"
            )

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    # Database configuration
    @property
    def db_config(self) -> Dict[str, str]:
        """Get database configuration from environment variables"""
        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "matches_db"),
            "port": int(os.getenv("DB_PORT", "3306"))
        }

    # General settings
    @property
    def default_phase(self) -> str:
        """Get default phase (fase1, fase2, or tot)"""
        return self._config.get("default_phase", "tot")

    # Clubs and teams
    @property
    def clubs(self) -> List[Dict[str, Any]]:
        """Get list of clubs and their teams"""
        return self._config.get("clubs", [])

    def get_club_by_id(self, club_id: int) -> Dict[str, Any]:
        """Get club configuration by ID"""
        for club in self.clubs:
            if club["id"] == club_id:
                return club
        return None

    def get_club_by_name(self, club_name: str) -> Dict[str, Any]:
        """Get club configuration by name"""
        for club in self.clubs:
            if club["name"].lower() == club_name.lower():
                return club
        return None

    # Scraping settings
    @property
    def base_url(self) -> str:
        """Get base URL for scraping"""
        return self._config.get("scraping", {}).get(
            "base_url",
            "https://www.basquetcatala.cat"
        )

    @property
    def api_url(self) -> str:
        """Get API URL for match statistics"""
        return self._config.get("scraping", {}).get(
            "api_url",
            "https://msstats.optimalwayconsulting.com/v1/fcbq"
        )

    @property
    def timeout(self) -> int:
        """Get HTTP request timeout in seconds"""
        return self._config.get("scraping", {}).get("timeout", 10)

    @property
    def skip_downloads(self) -> bool:
        """Check if downloads should be skipped"""
        return self._config.get("scraping", {}).get("skip_downloads", False)

    @property
    def skip_id_checks(self) -> bool:
        """Check if ID checks should be skipped"""
        return self._config.get("scraping", {}).get("skip_id_checks", False)

    # Excel settings
    @property
    def excel_decimal_places(self) -> int:
        """Get number of decimal places for Excel reports"""
        return self._config.get("excel", {}).get("decimal_places", 1)

    # Web dashboard settings
    @property
    def web_enabled(self) -> bool:
        """Check if web dashboard is enabled"""
        return self._config.get("web", {}).get("enabled", False)

    @property
    def web_host(self) -> str:
        """Get web dashboard host"""
        return self._config.get("web", {}).get("host", "0.0.0.0")

    @property
    def web_port(self) -> int:
        """Get web dashboard port"""
        return self._config.get("web", {}).get("port", 8080)

    @property
    def web_title(self) -> str:
        """Get web dashboard title"""
        return self._config.get("web", {}).get(
            "title",
            "Basketball Statistics Dashboard"
        )


# Global configuration instance
config = Config()


if __name__ == "__main__":
    # Test configuration loading
    print("Configuration loaded successfully!")
    print(f"Default phase: {config.default_phase}")
    print(f"Number of clubs configured: {len(config.clubs)}")
    print(f"Database host: {config.db_config['host']}")
    print(f"API URL: {config.api_url}")

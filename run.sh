#!/bin/bash
# Convenience script to run the scraper with automatic environment activation

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${RESET}"
    echo "Please run: make setup && make install"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if config exists
if [ ! -f "config.yaml" ]; then
    echo -e "${RED}Error: config.yaml not found!${RESET}"
    echo "Please create config.yaml based on the example in the file"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Warning: .env file not found!${RESET}"
    echo "Please copy .env.example to .env and configure your database credentials"
    exit 1
fi

# If no arguments provided, show usage
if [ $# -eq 0 ]; then
    echo -e "${BLUE}Basketball Statistics Scraper${RESET}"
    echo ""
    echo "Usage:"
    echo "  $0 all              - Update all clubs configured in config.yaml"
    echo "  $0 cabrera          - Update CB Cabrera (quick shortcut)"
    echo "  $0 club <id>        - Update specific club by ID"
    echo "  $0 team <club> <team> - Update specific team"
    echo ""
    echo "Examples:"
    echo "  $0 cabrera"
    echo "  $0 club 59"
    echo "  $0 team 59 79391"
    exit 0
fi

# Process command
case "$1" in
    all)
        echo -e "${BLUE}Updating all configured clubs...${RESET}"
        python update_all.py
        ;;
    cabrera)
        echo -e "${BLUE}Updating CB Cabrera (club 59)...${RESET}"
        python club_scraper.py 59 tot
        ;;
    club)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please specify club ID${RESET}"
            echo "Usage: $0 club <club_id>"
            exit 1
        fi
        echo -e "${BLUE}Updating club $2...${RESET}"
        python club_scraper.py "$2" tot
        ;;
    team)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}Error: Please specify both club ID and team ID${RESET}"
            echo "Usage: $0 team <club_id> <team_id>"
            exit 1
        fi
        echo -e "${BLUE}Updating team $3 from club $2...${RESET}"
        python team_scraper.py "$2" "$3" tot
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$1'${RESET}"
        echo "Run '$0' without arguments to see usage"
        exit 1
        ;;
esac

echo -e "${GREEN}Done!${RESET}"

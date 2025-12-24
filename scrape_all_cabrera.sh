#!/bin/bash
# Complete CB Cabrera scraping script
# Scrapes all teams and their rivals for comprehensive coach analysis

echo "========================================"
echo "CB CABRERA - COMPLETE SCRAPING SCRIPT"
echo "========================================"
echo ""

# Array of all CB Cabrera team IDs
TEAMS=(
    # Senior Teams
    "69563"   # 2A Territorial Senior Femení
    "79388"   # 2A Territorial Senior Femení
    "79392"   # 2A Territorial Senior Masculí B
    "69565"   # 3A Territorial Senior Masculí B

    # Competition Teams
    "71828"   # Júnior Masculí Nivell A
    "79386"   # Júnior Masculí Nivell A Vermell
    "79387"   # Primera Categoria Masculina A
    "69564"   # Segona Categoria Masculina A
    "71827"   # Sots-20 Masculí Nivell A-1
    "79390"   # Sots-20 Masculí Nivell A-1

    # Cadet Teams
    "71714"   # Cadet Masculí Promoció Negre
    "72157"   # Cadet Masculí Promoció Vermell
    "79394"   # Cadet Masculí Promoció

    # Infantil Teams
    "79391"   # Infantil Femení Promoció
    "79385"   # Infantil Masculí Promoció Vermell
    "79389"   # Infantil Masculí Promoció Negre

    # Júnior Promoció
    "79395"   # Júnior Masculí Promoció Negre

    # Mini Teams
    "73131"   # Mini Masculí
    "79393"   # Mini Masculí
    "81385"   # Mini Masculí 1r Any Vermell
    "81386"   # Mini Masculí 1r Any Negre

    # Pre-Infantil Teams
    "71713"   # Pre-Infantil Femení
    "71712"   # Pre-Infantil Masculí

    # Pre-Mini Teams
    "72155"   # Pre-Mini Masculí Vermell
    "72156"   # Pre-Mini Masculí Negre
    "81644"   # Pre-Mini Masculí 1r Any Vermell
    "81645"   # Pre-Mini Masculí 1r Any Negre

    # Escobol Teams
    "74516"   # Escobol A
    "74543"   # Escobol B
    "84804"   # Escobol (Lliga)
)

TOTAL=${#TEAMS[@]}
CURRENT=0

echo "📊 Found $TOTAL CB Cabrera teams to process"
echo ""
echo "This will:"
echo "  1. Scrape each team's match data"
echo "  2. Scrape all rival teams in each competition"
echo "  3. Calculate complete league standings"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "Starting complete scraping process..."
echo ""

for TEAM_ID in "${TEAMS[@]}"; do
    CURRENT=$((CURRENT + 1))
    echo ""
    echo "════════════════════════════════════════"
    echo "[$CURRENT/$TOTAL] Processing Team: $TEAM_ID"
    echo "════════════════════════════════════════"
    echo ""

    # Step 1: Scrape the team's matches
    echo "📥 Step 1/2: Scraping team matches..."
    python3 team_scraper.py "$TEAM_ID" tot

    if [ $? -eq 0 ]; then
        echo "✅ Team $TEAM_ID scraped successfully"
    else
        echo "⚠️  Warning: Issues scraping team $TEAM_ID"
    fi

    echo ""

    # Step 2: Scrape all rivals (with full data)
    echo "🎯 Step 2/2: Scraping rival teams..."
    python3 scrape_rivals.py "$TEAM_ID" tot

    if [ $? -eq 0 ]; then
        echo "✅ Rivals for team $TEAM_ID scraped successfully"
    else
        echo "⚠️  Warning: Issues scraping rivals for team $TEAM_ID"
    fi

    # Delay between teams to avoid rate limiting
    if [ $CURRENT -lt $TOTAL ]; then
        echo ""
        echo "⏳ Waiting 3 seconds before next team..."
        sleep 3
    fi
done

echo ""
echo "════════════════════════════════════════"
echo "✅ COMPLETE!"
echo "════════════════════════════════════════"
echo ""
echo "Processed $TOTAL CB Cabrera teams"
echo ""
echo "Next steps:"
echo "  1. Start the dashboard: python3 web_dashboard.py"
echo "  2. Visit: http://localhost:5001"
echo "  3. Explore all teams, rivals, and statistics"
echo ""

#!/bin/bash
# Calculate league standings for all CB Cabrera teams
# This runs the standings calculation without re-scraping rival teams

echo "========================================"
echo "CALCULATE STANDINGS FOR ALL CB CABRERA TEAMS"
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
SUCCESS=0
FAILED=0

echo "📊 Calculating standings for $TOTAL CB Cabrera teams"
echo "⚡ This is fast - only calculates standings, no scraping"
echo ""

for TEAM_ID in "${TEAMS[@]}"; do
    CURRENT=$((CURRENT + 1))
    echo -n "[$CURRENT/$TOTAL] Team $TEAM_ID... "

    # Run scrape_rivals.py with --no-scrape to just calculate standings
    python3 scrape_rivals.py "$TEAM_ID" tot --no-scrape > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "✅"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "⚠️"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "════════════════════════════════════════"
echo "✅ COMPLETE!"
echo "════════════════════════════════════════"
echo ""
echo "Processed: $TOTAL teams"
echo "Success: $SUCCESS teams"
echo "Failed: $FAILED teams"
echo ""
echo "All CB Cabrera teams now have league standings!"
echo ""

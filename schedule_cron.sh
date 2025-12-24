#!/bin/bash
# Cron job script for automated statistics updates
# Add to crontab with: crontab -e
# Example: Run every Sunday at 2 AM
# 0 2 * * 0 /path/to/schedule_cron.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Log file
LOG_FILE="$SCRIPT_DIR/logs/cron_$(date +\%Y\%m\%d_\%H\%M\%S).log"
mkdir -p "$SCRIPT_DIR/logs"

# Redirect output to log file
exec 1>> "$LOG_FILE" 2>&1

echo "=========================================="
echo "Starting automated update: $(date)"
echo "=========================================="

# Activate virtual environment
source venv/bin/activate

# Update all clubs
python3 update_all.py

# Generate web dashboard (optional)
# python3 publish_web.py

echo ""
echo "=========================================="
echo "Completed: $(date)"
echo "=========================================="

# Optional: Clean old logs (keep last 30 days)
find "$SCRIPT_DIR/logs" -name "cron_*.log" -mtime +30 -delete

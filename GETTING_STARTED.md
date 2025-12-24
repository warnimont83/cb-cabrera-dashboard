# Getting Started - Quick Guide

This is a simplified guide to get you up and running quickly!

## What Changed?

Your project has been modernized with:
- Configuration files (no more hardcoded IDs!)
- Automation scripts (no more manual venv activation!)
- Web dashboard (view stats in your browser!)
- Scheduling support (automated updates!)

## Backup

Your original files are safe in: `backup_20241223_164129/`

## First Time Setup (5 minutes)

### Step 1: Install Dependencies

The old `requeriments.txt` (typo) has been fixed to `requirements.txt` and updated with new dependencies.

```bash
# Make sure you're in the project directory
cd /Users/enric.sola/Documents/Basket

# Install new dependencies to your existing venv
source venv/bin/activate
pip install -r requirements.txt
```

Or recreate the environment:
```bash
make clean-all
make setup
make install
```

### Step 2: Configuration is Already Done!

Your CB Cabrera configuration is already set up in `config.yaml`:
```yaml
clubs:
  - name: "CB Cabrera"
    id: 59
    teams:
      - id: 79391  # Your first team
      - id: 81385  # Your second team
```

Your database password has been moved from the code to `.env` file (more secure!).

## How to Use (Much Easier Now!)

### Old Way ❌
```bash
source venv/bin/activate  # Had to remember this
python club_scraper.py 59 tot  # Had to remember club ID
```

### New Way ✅

**Option 1: Using Make (Recommended)**
```bash
make run-cabrera  # That's it! No venv activation needed!
```

**Option 2: Using the Shell Script**
```bash
./run.sh cabrera  # Even simpler!
```

**Option 3: Update All Configured Teams**
```bash
make update-all
# or
./run.sh all
```

## View Your Statistics

### Option 1: Interactive Web Dashboard 🎨

```bash
make serve
```
Then open: http://localhost:8080

Features:
- Interactive charts
- Player statistics
- Team comparisons
- Real-time data

### Option 2: Static Website 📊

```bash
python3 publish_web.py
```
This generates HTML files in `docs/` that you can:
- Open locally in a browser
- Deploy to GitHub Pages
- Upload to any web host

### Option 3: Excel Files (Still Works!) 📈

Excel files are still generated in the same place:
```
CLUB_BASQUET_CABRERA/estadistiques/*.xlsx
```

## Useful Commands

```bash
make help              # See all available commands
make run-cabrera       # Update CB Cabrera
make serve             # Start web dashboard
make backup            # Create backup
make clean             # Clean temporary files
make test-config       # Test your configuration
```

## Automation (Optional)

### Set Up Weekly Updates

Add to cron (runs every Sunday at 2 AM):
```bash
crontab -e
# Add this line:
0 2 * * 0 /Users/enric.sola/Documents/Basket/schedule_cron.sh
```

## Adding More Teams

Just edit `config.yaml`:

```yaml
clubs:
  - name: "CB Cabrera"
    id: 59
    teams:
      - id: 79391
        name: "Team 1"
      - id: 81385
        name: "Team 2"
      - id: 99999  # Add new team here!
        name: "Team 3"

  - name: "Another Club"  # Add entire new clubs!
    id: 123
    teams:
      - id: 456
        name: "Some Team"
```

Then run:
```bash
make update-all
```

## What If Something Breaks?

### Restore Original Version
```bash
cp backup_20241223_164129/*.py .
```

### Check Configuration
```bash
make test-config
```

### View Full Documentation
```bash
cat README.md
```

## Quick Comparison

| Task | Old Way | New Way |
|------|---------|---------|
| Activate environment | `source venv/bin/activate` | Not needed (scripts do it) |
| Remember club ID | "Was it 59?" | Configured in config.yaml |
| Remember team IDs | "79391 and 81385?" | Configured in config.yaml |
| Run scraper | `python club_scraper.py 59 tot` | `make run-cabrera` |
| View statistics | Open Excel | Open browser + see charts! |
| Update all teams | Run multiple commands | `make update-all` |
| Schedule updates | Manual cron setup | Use provided script |
| Web publishing | Not possible | `make serve` or `make publish` |

## Next Steps

1. ✅ Run `make run-cabrera` to test everything works
2. ✅ Run `make serve` to see your new web dashboard
3. ✅ Bookmark http://localhost:8080 for easy access
4. ✅ (Optional) Set up cron for automatic updates

## Need Help?

- Full documentation: `README.md`
- Test configuration: `make test-config`
- Available commands: `make help`
- Restore backup: Files in `backup_20241223_164129/`

---

**You're all set! Try running: `make run-cabrera`**

# Image Features Guide

## What's New? 🎨

Your basketball dashboard now includes:
- **Club Logos** displayed throughout the interface
- **Federation-style design** matching basquetcatala.cat
- **Automatic image scraping** from the official website

## Features Added:

### 1. Club Logos Display
- ✅ Home page shows club logos next to club names
- ✅ Club detail pages show large logos in header
- ✅ Professional, clean design matching the federation website
- ✅ Logos automatically fetched from official website

### 2. Image Scraper Script
A new `scrape_images.py` script that:
- Downloads club logos from basquetcatala.cat
- Saves them in `static/images/clubs/`
- Automatically finds the correct logo for each club
- Creates backup if image already exists

### 3. Improved Visual Design
- Modern card-based layout
- Hover effects and shadows
- Better spacing and typography
- Professional color scheme
- Responsive design for mobile

## How to Use:

### Download Club Logos

```bash
# Run the image scraper
python3 scrape_images.py
```

This will:
- Download logos for all clubs in your `config.yaml`
- Save them as `static/images/clubs/{club_id}.jpg`
- Show progress and success/failure for each club

### Update Logos Periodically

```bash
# Clubs sometimes update their logos
# Run this monthly to keep logos fresh
python3 scrape_images.py
```

### Add New Clubs

When you add a new club to `config.yaml`:
1. Add the club configuration
2. Run `python3 scrape_images.py`
3. The new club's logo will be downloaded automatically

## What About Player Photos? 📸

**Current Status:**
- ❌ Player photos are NOT publicly available on basquetcatala.cat
- This is intentional for privacy/youth protection
- Most youth teams don't publish player photos online

**Alternatives:**
1. **Manual Upload**: You can manually add player photos if you have them
   - Create folder: `static/images/players/`
   - Name files: `{team_id}_{player_dorsal}.jpg`
   - Update templates to display them

2. **Team Photos**: You could add team group photos manually
   - Add to `static/images/teams/`
   - Display on team pages

3. **Default Avatars**: Use generic player silhouettes
   - Create default player icon
   - Show for all players without photos

## File Structure:

```
static/
  images/
    clubs/           # Club logos (auto-downloaded)
      59.jpg         # CB Cabrera logo
      123.jpg        # Another club logo
    players/         # Player photos (manual - optional)
      79391_8.jpg    # Jana's photo (team 79391, dorsal 8)
    teams/           # Team photos (manual - optional)
      79391.jpg      # Team group photo
```

## Customization:

### Change Logo Size

Edit `static/css/style.css`:

```css
.club-logo {
    width: 80px;     /* Change this */
    height: 80px;    /* And this */
}

.club-logo-large {
    width: 120px;    /* For large logos */
    height: 120px;
}
```

### Add Fallback Image

If a logo is missing, you can show a default:

```html
<img src="{{ url_for('static', filename='images/clubs/' ~ club_id ~ '.jpg') }}"
     onerror="this.src='{{ url_for('static', filename='images/default-club.png') }}'">
```

## Comparison: Before vs After

### Before:
- Plain text club names
- Simple list layout
- No visual identity
- Generic appearance

### After:
- Club logos displayed
- Professional card layout
- Visual club identity
- Federation-style design
- Hover effects and shadows

## Technical Details:

### Image Scraping Process:
1. Fetch club page HTML
2. Parse with BeautifulSoup
3. Find logo image (usually on CloudFront CDN)
4. Download and save locally
5. Serve from Flask static files

### Why Local Storage?
- ✅ Faster loading (no external requests)
- ✅ Works offline
- ✅ Reduces load on federation servers
- ✅ Consistent even if federation site changes

### Image Formats Supported:
- JPG/JPEG (most common)
- PNG (with transparency)
- GIF (static)
- WEBP (modern format)

## Troubleshooting:

### Logo Not Showing?

1. **Check if image was downloaded:**
   ```bash
   ls -la static/images/clubs/
   ```

2. **Re-download:**
   ```bash
   python3 scrape_images.py
   ```

3. **Check club ID in config.yaml:**
   - Make sure club ID matches the one on basquetcatala.cat

### Image Too Large/Small?

Edit CSS (see Customization section above)

### Wrong Image Downloaded?

- Federation site might have multiple images
- Script tries to find the best match
- You can manually replace the image in `static/images/clubs/`

## Future Enhancements:

### Potential Additions:
- [ ] Team badge/crest (if available)
- [ ] Category icons
- [ ] Player avatars (with privacy controls)
- [ ] Match venue photos
- [ ] Trophy/achievement icons

### Player Photos (Privacy-Aware):
If you want to add player photos:
1. Get written permission from parents/guardians
2. Use only for private/family viewing
3. Don't publish publicly without consent
4. Consider watermarking with "Private Use Only"

## Commands Summary:

```bash
# Download all club logos
python3 scrape_images.py

# Start dashboard with logos
python3 web_dashboard.py

# View in browser
open http://localhost:8080
```

---

**Enjoy your enhanced, professional-looking basketball dashboard!** 🏀✨

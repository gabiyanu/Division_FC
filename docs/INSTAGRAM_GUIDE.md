# 📱 Instagram Posting Guide

Complete guide for posting Division FC visualizations to Instagram.

---

## Table of Contents

1. [Export for Instagram](#export-for-instagram)
2. [Manual Posting](#manual-posting)
3. [Automated Posting](#automated-posting)
4. [Best Practices](#best-practices)
5. [Hashtags & Captions](#hashtags--captions)

---

## Export for Instagram

### Image Formats

| Format | Dimensions | Use Case |
|--------|------------|----------|
| Square Post | 1080 × 1080 | Standard feed post |
| Portrait Post | 1080 × 1350 | Taller visualizations |
| Story | 1080 × 1920 | Stories & temporary content |
| Reel | 1080 × 1920 | Animated content |

### Using the Instagram Exporter

```python
from src.export.instagram import InstagramExporter

# Initialize exporter
exporter = InstagramExporter(output_dir='output')

# Export as square post (1080x1080)
exporter.export_post(
    fig=fig,
    filename='messi_shots_ig.png',
    format='square',                    # 'square' or 'portrait'
    add_watermark=True,
    watermark_text='@divisionfc',
    background_color='#0D1117'          # Match brand background
)

# Export as story (1080x1920)
exporter.export_story(
    fig=fig,
    filename='messi_shots_story.png',
    add_watermark=True,
    watermark_text='@divisionfc'
)

# Export animation as reel
exporter.export_reel(
    anim=animation,
    filename='goal_sequence.mp4',
    fps=30,
    add_watermark=True,
    watermark_text='@divisionfc'
)

# Export as GIF (for carousels or external use)
exporter.export_gif(
    anim=animation,
    filename='passes.gif',
    fps=15,
    optimize=True
)
```

### Quick Export Functions

```python
from src.export.instagram import create_instagram_post

# One-liner for quick exports
filepath = create_instagram_post(
    fig=fig,
    filename='shot_map.png',
    watermark='@divisionfc'
)
print(f"Ready to post: {filepath}")
```

### Complete Workflow Example

```python
from src.data.loader import StatsBombLoader, get_top_players_by_stat
from src.export.instagram import InstagramExporter
import matplotlib.pyplot as plt

# 1. Load data (dynamically sourced)
loader = StatsBombLoader()
events, match_info = loader.load_match_by_criteria(
    competition_name="World Cup",
    stage="Final"
)

# 2. Create visualization
fig, ax = plt.subplots(figsize=(10, 10), facecolor='#0D1117')
# ... your visualization code ...

# 3. Export for Instagram
exporter = InstagramExporter()

# Square post for feed
post_path = exporter.export_post(
    fig, 
    'worldcup_final_post.png',
    format='square',
    add_watermark=True,
    watermark_text='@divisionfc'
)

# Story version
story_path = exporter.export_story(
    fig,
    'worldcup_final_story.png',
    add_watermark=True,
    watermark_text='@divisionfc'
)

print(f"📱 Post ready: {post_path}")
print(f"📱 Story ready: {story_path}")
```

---

## Manual Posting

### Option 1: Instagram Mobile App (Recommended)

1. **Transfer files to your phone:**
   - AirDrop (iOS)
   - Google Drive / Dropbox
   - Email to yourself
   - USB transfer

2. **Open Instagram app**

3. **Create new post:**
   - Tap **+** button
   - Select your exported image
   - Apply filters (optional - our images are already styled)
   - Add caption and hashtags
   - Tag location (optional)
   - Post!

### Option 2: Instagram Web (Desktop)

1. Go to [instagram.com](https://instagram.com)
2. Click **+** (Create) in the top menu
3. Drag and drop your exported image
4. Add caption and hashtags
5. Click **Share**

### Option 3: Meta Business Suite (Best for Scheduling)

1. Go to [business.facebook.com](https://business.facebook.com)
2. Select your Instagram account
3. Click **Create Post**
4. Upload your image
5. Write caption
6. **Schedule** for optimal time or post immediately

---

## Automated Posting

### Option 1: Meta Business Suite API

For business accounts, you can use the official Instagram Graph API.

```python
"""
Instagram Graph API Posting (requires Business Account)

Prerequisites:
1. Facebook Business Page linked to Instagram
2. Meta Developer App with Instagram Graph API access
3. Access Token with instagram_content_publish permission
"""

import requests

def post_to_instagram(image_url, caption, access_token, ig_user_id):
    """
    Post image to Instagram using Graph API.
    
    Args:
        image_url: Public URL of the image (must be accessible)
        caption: Post caption with hashtags
        access_token: Meta API access token
        ig_user_id: Instagram Business Account ID
    
    Returns:
        dict: API response
    """
    # Step 1: Create media container
    container_url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media"
    container_params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }
    
    container_response = requests.post(container_url, params=container_params)
    container_id = container_response.json().get('id')
    
    if not container_id:
        return {'error': 'Failed to create container', 'response': container_response.json()}
    
    # Step 2: Publish the container
    publish_url = f"https://graph.facebook.com/v18.0/{ig_user_id}/media_publish"
    publish_params = {
        'creation_id': container_id,
        'access_token': access_token
    }
    
    publish_response = requests.post(publish_url, params=publish_params)
    return publish_response.json()


# Example usage (requires your credentials)
# response = post_to_instagram(
#     image_url='https://your-server.com/images/shot_map.png',
#     caption='🎯 Messi Shot Map - World Cup Final\n\n#football #soccer #messi',
#     access_token='YOUR_ACCESS_TOKEN',
#     ig_user_id='YOUR_IG_USER_ID'
# )
```

### Option 2: Third-Party Tools

| Tool | Features | Pricing |
|------|----------|---------|
| **Buffer** | Scheduling, analytics | Free tier available |
| **Later** | Visual planner, scheduling | Free tier available |
| **Hootsuite** | Multi-platform, team features | Paid |
| **Sprout Social** | Enterprise features | Paid |

### Option 3: Instabot (Unofficial - Use Carefully)

```bash
pip install instabot
```

```python
from instabot import Bot

# ⚠️ WARNING: Unofficial API - may violate Instagram ToS
# Use at your own risk - account may be flagged

bot = Bot()
bot.login(username="your_username", password="your_password")
bot.upload_photo(
    "output/images/shot_map.png",
    caption="🎯 Shot Map Analysis\n\n#football #soccer #analytics"
)
```

---

## Best Practices

### Image Quality

```python
# Always export at high DPI for crisp images
fig.savefig('output.png', dpi=300, bbox_inches='tight')

# For Instagram, 150 DPI is sufficient and keeps file size down
exporter.export_post(fig, 'post.png')  # Uses 150 DPI internally
```

### Color Optimization

```python
# Our Midnight Aurora palette is optimized for mobile screens
COLORS = {
    'background': '#0D1117',   # Dark but not pure black
    'cyan': '#00FFCC',         # Vibrant, visible on mobile
    'magenta': '#FF66B2',      # Pops on dark background
    'gold': '#FFD700',         # High contrast highlight
}
```

### File Size Guidelines

| Content Type | Max Size | Recommendation |
|--------------|----------|----------------|
| Photo | 30 MB | < 5 MB for fast loading |
| Video/Reel | 650 MB | < 100 MB recommended |
| Story | 30 MB | < 5 MB |

### Optimal Posting Times

Based on general engagement data (adjust for your audience):

| Day | Best Times (EST) |
|-----|------------------|
| Monday | 11am, 5pm |
| Tuesday | 9am, 6pm |
| Wednesday | 11am, 3pm |
| Thursday | 12pm, 7pm |
| Friday | 10am, 5pm |
| Saturday | 9am, 11am |
| Sunday | 10am, 2pm |

---

## Hashtags & Captions

### Caption Template

```
[EMOJI] [TITLE]

[Brief description - 1-2 sentences]

[Key stat or insight]

📊 Data: StatsBomb
🎨 Viz: Division FC

#football #soccer #analytics #dataviz #socceranalytics
#[competition] #[team] #[player]
```

### Example Caption

```
🎯 MESSI SHOT MAP

7 shots, 2 goals, 1.78 xG - Messi delivered when it mattered most.

His positioning and finishing were clinical in the World Cup Final.

📊 Data: StatsBomb
🎨 Viz: Division FC

#worldcup #messi #argentina #football #soccer #dataviz
#shotmap #xg #socceranalytics #footballanalytics #qatar2022
```

### Recommended Hashtags

**General Football:**
```
#football #soccer #futbol #calcio #fussball
```

**Analytics:**
```
#footballanalytics #socceranalytics #dataviz #datavisualization
#xg #expectedgoals #shotmap #passmap #heatmap
```

**Competitions:**
```
#worldcup #ucl #championsleague #premierleague #laliga
#seriea #bundesliga #ligue1 #euro2024 #copamerica
```

**Engagement:**
```
#footballdata #tacticalanalysis #matchanalysis #footballstats
#soccerstats #footballtactics #soccertactics
```

### Hashtag Strategy

```python
# Save hashtag sets for easy reuse
HASHTAGS = {
    'base': '#football #soccer #dataviz #socceranalytics #divisionfc',
    
    'worldcup': '#worldcup #qatar2022 #fifaworldcup',
    'ucl': '#ucl #championsleague #uefachampionsleague',
    'premierleague': '#premierleague #epl #pl',
    
    'shotmap': '#shotmap #xg #expectedgoals #finishing',
    'passmap': '#passmap #passing #buildup #possession',
    'heatmap': '#heatmap #touches #movement #positioning',
}

def get_hashtags(viz_type, competition):
    """Generate hashtags for a post."""
    tags = [
        HASHTAGS['base'],
        HASHTAGS.get(viz_type, ''),
        HASHTAGS.get(competition, ''),
    ]
    return '\n\n' + ' '.join(tags)

# Usage
caption = f"🎯 Messi Shot Map{get_hashtags('shotmap', 'worldcup')}"
```

---

## Complete Posting Workflow

```python
#!/usr/bin/env python3
"""
Complete Instagram posting workflow.
"""

from src.data.loader import StatsBombLoader, get_top_players_by_stat, get_goals
from src.export.instagram import InstagramExporter
from pathlib import Path

def create_and_export_for_instagram():
    """Generate visualizations and prepare for Instagram."""
    
    # 1. Load data dynamically
    loader = StatsBombLoader()
    events, match_info = loader.load_match_by_criteria(
        competition_name="World Cup",
        stage="Final"
    )
    
    # Extract info from data
    home_team = match_info['home_team']
    away_team = match_info['away_team']
    competition = match_info.get('competition', 'Match')
    
    # 2. Create visualization (example: shot map)
    from examples.world_cup_analysis import create_shot_map, IMAGES_DIR
    
    # Get top shooter from data
    top_shooters = get_top_players_by_stat(events, home_team, stat='shots', n=1)
    if top_shooters:
        player = top_shooters[0]
        create_shot_map(events, player, 'shot_map_raw.png')
    
    # 3. Export for Instagram
    exporter = InstagramExporter()
    
    # Load the raw image and re-export for Instagram
    from PIL import Image
    import matplotlib.pyplot as plt
    
    raw_path = IMAGES_DIR / 'shot_map_raw.png'
    
    # Create Instagram-ready versions
    img = Image.open(raw_path)
    
    # Square post
    post_img = exporter._resize_with_padding(img, (1080, 1080), '#0D1117')
    post_img = exporter._add_watermark(post_img, '@divisionfc')
    post_path = IMAGES_DIR / 'shot_map_instagram.png'
    post_img.save(post_path, 'PNG', quality=95)
    
    # Story version
    story_img = exporter._resize_with_padding(img, (1080, 1920), '#0D1117')
    story_img = exporter._add_watermark(story_img, '@divisionfc', position='bottom')
    story_path = IMAGES_DIR / 'shot_map_story.png'
    story_img.save(story_path, 'PNG', quality=95)
    
    # 4. Generate caption
    player_short = player.split()[-1] if top_shooters else 'Player'
    goals = get_goals(events)
    player_goals = len(goals[goals['player_name'] == player]) if top_shooters else 0
    
    caption = f"""🎯 {player_short.upper()} SHOT MAP

{competition} Final - {home_team} vs {away_team}

{player_goals} goals from {player_short} in the biggest game of his career.

📊 Data: StatsBomb
🎨 Viz: Division FC

#football #soccer #dataviz #socceranalytics #shotmap
#worldcup #messi #argentina #{player_short.lower()}"""
    
    # 5. Print instructions
    print("=" * 50)
    print("📱 INSTAGRAM READY!")
    print("=" * 50)
    print(f"\n📸 Post image: {post_path}")
    print(f"📸 Story image: {story_path}")
    print(f"\n📝 Suggested caption:\n")
    print(caption)
    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. Transfer images to your phone")
    print("2. Open Instagram")
    print("3. Create new post/story")
    print("4. Paste the caption above")
    print("5. Post! 🚀")
    print("=" * 50)
    
    return {
        'post_path': str(post_path),
        'story_path': str(story_path),
        'caption': caption
    }


if __name__ == "__main__":
    create_and_export_for_instagram()
```

---

## Quick Reference

```bash
# Generate Instagram-ready content
python examples/world_cup_analysis.py

# Files will be in:
# - output/images/*_instagram.png (posts)
# - output/images/*_story.png (stories)
# - output/gifs/*.gif (carousel/external)
# - output/videos/*.mp4 (reels)
```

### File Checklist Before Posting

- [ ] Image is 1080×1080 (square) or 1080×1350 (portrait)
- [ ] File size < 5 MB
- [ ] Watermark added (@divisionfc)
- [ ] Colors are vibrant on mobile preview
- [ ] Text is readable on small screens
- [ ] Caption written with hashtags
- [ ] Credit given to data source (StatsBomb)

---

## Need Help?

- **Instagram Help Center:** https://help.instagram.com/
- **Meta Business Help:** https://www.facebook.com/business/help
- **Graph API Docs:** https://developers.facebook.com/docs/instagram-api

---

*Division FC - Soccer Analytics for the Social Age* ⚽📱

# ⚽ Division FC Soccer Analytics

<p align="center">
  <img src="assets/division_fc_logo_v3.svg" alt="Division FC Logo" width="200"/>
</p>

<p align="center">
  <strong>Professional soccer visualizations with the "Midnight Aurora" brand identity</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#jupyter-notebook-quick-start">Quick Start</a> •
  <a href="#visualizations">Visualizations</a> •
  <a href="#animations">Animations</a> •
  <a href="#instagram-export">Instagram Export</a>
</p>

---

## 🎯 Overview

Division FC Soccer Analytics is a Python toolkit for creating stunning, Instagram-ready soccer visualizations. Built with a custom "Midnight Aurora" brand identity.

**Demo Data:** FIFA World Cup 2022 Final (Argentina vs France)

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/division-fc-analytics.git
cd division-fc-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Notebook
jupyter notebook
```

---

## 🚀 Jupyter Notebook Quick Start

### Cell 1: Setup

```python
import sys
sys.path.insert(0, '.')

from src.data.loader import StatsBombLoader, get_top_players_by_stat, get_goals, get_shots, calculate_xg
from src.export.instagram import InstagramExporter

print("✅ Setup complete!")
```

### Cell 2: Load World Cup Final Data

```python
# Initialize loader
loader = StatsBombLoader()

# Load World Cup Final (all IDs sourced dynamically)
events, match_info = loader.load_match_by_criteria(
    competition_name="World Cup",
    stage="Final"
)

# Display match info
print(f"🏆 {match_info['home_team']} vs {match_info['away_team']}")
print(f"📊 Score: {int(match_info['home_score'])} - {int(match_info['away_score'])}")
print(f"📅 Date: {match_info['match_date']}")
print(f"✅ Loaded {len(events)} events")
```

### Cell 3: View Goals

```python
# Get all goals (from data)
goals = get_goals(events)

print(f"⚽ Goals ({len(goals)} total):")
for _, goal in goals.iterrows():
    player = goal['player_name'].split()[-1]
    print(f"   {int(goal['minute'])}' - {player} ({goal['team_name']})")
```

### Cell 4: Run Full Analysis

```python
# Run complete World Cup analysis
%run examples/world_cup_analysis.py
```

**Output files saved to:**
- `output/images/` - All visualization PNGs
- `output/gifs/` - Goal animations

---

## 📊 Visualizations

### Shot Map

```python
%run examples/world_cup_analysis.py

# Or create individually:
from examples.world_cup_analysis import create_shot_map, load_world_cup_final

events, match_info, _ = load_world_cup_final()
top_shooter = get_top_players_by_stat(events, match_info['home_team'], stat='shots', n=1)[0]
create_shot_map(events, top_shooter, 'my_shot_map.png')
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `player_name` | str | Full player name (sourced from data) |
| `filename` | str | Output filename |

---

### Touch Heatmap

```python
from examples.world_cup_analysis import create_touch_heatmap

create_touch_heatmap(events, player_name, 'heatmap.png')
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `player_name` | str | Player to analyze |
| `filename` | str | Output filename |

---

### Pass Network

```python
from examples.world_cup_analysis import create_pass_network

create_pass_network(events, team_name, 'pass_network.png')
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `team_name` | str | Team name (from `match_info['home_team']`) |
| `filename` | str | Output filename |

---

### Zone Control

```python
from examples.world_cup_analysis import create_zone_control

create_zone_control(events, home_team, away_team, 'zone_control.png')
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `home_team` | str | Home team name |
| `away_team` | str | Away team name |
| `filename` | str | Output filename |

---

### Match Summary

```python
from examples.world_cup_analysis import create_match_summary

create_match_summary(events, match_info, 'summary.png')
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `match_info` | Series | Match metadata |
| `filename` | str | Output filename |

---

## 🎬 Animations

### Goal Buildup Animation

```python
from examples.world_cup_analysis import create_goal_animation

# Get goals from data
goals = get_goals(events)
goal_minute = int(goals.iloc[0]['minute'])
team = goals.iloc[0]['team_name']

create_goal_animation(events, goal_minute, team, 'goal.gif')
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `goal_minute` | int | Minute of the goal (from data) |
| `team_name` | str | Scoring team |
| `filename` | str | Output filename |

---

### Using MatchAnimator Directly

```python
from src.animations.match_animation import MatchAnimator

animator = MatchAnimator(events, fps=10)
anim = animator.create_event_sequence_animation(
    team_name=match_info['home_team'],
    time_range=(20, 25),
    show_trails=True
)
animator.save_gif("sequence.gif", fps=8)
```

---

## 📱 Instagram Export

### Quick Export

```python
%run examples/instagram_export.py
```

**Output:**
- `output/images/instagram_post.png` (1080×1080)
- `output/images/instagram_story.png` (1080×1920)
- Caption printed to console

### Manual Export

```python
from src.export.instagram import InstagramExporter

exporter = InstagramExporter()

# Square post (1080x1080)
exporter.export_post(fig, 'post.png', format='square', add_watermark=True, watermark_text='@divisionfc')

# Story (1080x1920)
exporter.export_story(fig, 'story.png', add_watermark=True)

# Reel from animation
exporter.export_reel(anim, 'reel.mp4', fps=30)
```

### Export Formats

| Format | Dimensions | Method |
|--------|------------|--------|
| Square Post | 1080 × 1080 | `export_post(format='square')` |
| Portrait Post | 1080 × 1350 | `export_post(format='portrait')` |
| Story/Reel | 1080 × 1920 | `export_story()` / `export_reel()` |

---

## 🎨 Brand Colors

```python
from src.branding.style import ColorPalette

colors = ColorPalette()
colors.CYAN      # #00FFCC
colors.MAGENTA   # #FF66B2
colors.PURPLE    # #AA66FF
colors.GOLD      # #FFD700
```

---

## 📁 Output Files

After running `%run examples/world_cup_analysis.py`:

```
output/
├── images/
│   ├── messi_shot_map.png
│   ├── mbappe_shot_map.png
│   ├── messi_heatmap.png
│   ├── argentina_pass_network.png
│   ├── france_pass_network.png
│   ├── zone_control.png
│   └── match_summary.png
└── gifs/
    ├── argentina_goal_1.gif
    └── france_goal_1.gif
```

---

## 📓 Example Notebook Session

```python
# Cell 1: Setup
import sys
sys.path.insert(0, '.')
from src.data.loader import StatsBombLoader, get_goals, get_top_players_by_stat

# Cell 2: Load data
loader = StatsBombLoader()
events, match_info = loader.load_match_by_criteria(competition_name="World Cup", stage="Final")
print(f"✅ {match_info['home_team']} vs {match_info['away_team']}")

# Cell 3: Show goals
goals = get_goals(events)
for _, g in goals.iterrows():
    print(f"{int(g['minute'])}' - {g['player_name'].split()[-1]}")

# Cell 4: Generate all visualizations
%run examples/world_cup_analysis.py

# Cell 5: Export for Instagram
%run examples/instagram_export.py
```

---

## 🙏 Credits

| Source | Type | License |
|--------|------|---------|
| **StatsBomb** | Data | CC BY 4.0 |
| **mplsoccer** | Library | MIT |
| **Son of a Corner** | Inspiration | - |

---

## 📖 Additional Documentation

- [API Reference](docs/API_REFERENCE.md)
- [Brand Guide](docs/BRAND_GUIDE.md)
- [Instagram Guide](docs/INSTAGRAM_GUIDE.md)
- [Project Pipeline](docs/PROJECT_PIPELINE.md)

---

<p align="center">
  Made with ⚽ by Division FC
</p>

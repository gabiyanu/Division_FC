# ⚽ Division FC Soccer Analytics

<p align="center">
  <img src="assets/division_fc_logo_v3.svg" alt="Division FC Logo" width="200"/>
</p>

<p align="center">
  <strong>Professional soccer analytics visualizations with the "Midnight Aurora" brand identity</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#visualizations">Visualizations</a> •
  <a href="#animations">Animations</a> •
  <a href="#credits">Credits</a>
</p>

---

## 🎯 Overview

Division FC Soccer Analytics is a Python toolkit for creating stunning, Instagram-ready soccer visualizations. Built with a custom "Midnight Aurora" brand identity featuring dark backgrounds with vibrant cyan, magenta, purple, and gold accents.

**Demo Data:** FIFA World Cup 2022 Final (Argentina vs France)

---

## ✨ Features

- **5 Pitch Visualization Types:**
  - Progressive Passes Grid
  - Crossing Zones Heatmap
  - Contested Zones / Territorial Control
  - Player Shot Maps
  - Touch Heatmaps

- **Animated Visualizations:**
  - Event sequence animations
  - Pass flow animations
  - Goal buildup replays

- **Brand Identity System:**
  - Midnight Aurora color palette
  - Consistent typography
  - Watermark integration
  - Instagram-optimized exports

---

## 📦 Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/division-fc-analytics.git
cd division-fc-analytics

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### Load World Cup Final Data (All IDs Sourced Dynamically)

```python
from src.data.loader import StatsBombLoader

# Initialize loader
loader = StatsBombLoader()

# Find competition by name - NO hardcoded IDs
comp_id, season_id = loader.find_competition("World Cup", season="2022")

# Find final match dynamically
final = loader.find_final(comp_id, season_id)
print(f"Found: {final['home_team']} vs {final['away_team']}")

# Or use the convenience method - fully dynamic
events, match_info = loader.load_match_by_criteria(
    competition_name="World Cup",
    stage="Final"
)

# All values extracted from data
home_team = match_info['home_team']  # Sourced from API
away_team = match_info['away_team']  # Sourced from API
print(f"Loaded {len(events)} events for {home_team} vs {away_team}")
```

### Key Principle: Nothing Hardcoded

```python
# ❌ DON'T hardcode IDs
match_id = 3869685  # Bad - hardcoded

# ✅ DO discover from data
loader = StatsBombLoader()
events, info = loader.load_match_by_criteria(
    competition_name="World Cup",  # Search by name
    stage="Final"                   # Find dynamically
)
match_id = info['match_id']  # Good - sourced from data
```

### Create a Visualization (Data-Sourced)

```python
from src.data.loader import StatsBombLoader, get_top_players_by_stat, get_shots
from src.visualizations.shot_map import ShotMap

# Load data dynamically
loader = StatsBombLoader()
events, match_info = loader.load_match_by_criteria(
    competition_name="World Cup",
    stage="Final"
)

# Get team names from data (not hardcoded)
home_team = match_info['home_team']
away_team = match_info['away_team']

# Find top shooter dynamically
top_shooters = get_top_players_by_stat(events, home_team, stat='shots', n=1)
player_name = top_shooters[0]  # Sourced from data

# Get shots for that player
player_shots = get_shots(events, home_team)
player_shots = player_shots[player_shots['player_name'] == player_name]

# Create shot map
shot_map = ShotMap()
fig, ax = shot_map.create(
    shots=player_shots,
    title=f"{player_name.split()[-1]} - Shot Map",  # Name from data
    subtitle=f"{match_info['competition']} Final"    # Competition from data
)

fig.savefig('output/images/shot_map.png', dpi=300, bbox_inches='tight')
```

---

## 📊 Visualizations

### 1. Progressive Passes Grid

Shows improvement/deterioration in progressive passing by pitch zone.

```python
from src.visualizations.progressive_passes import ProgressivePassesGrid

grid = ProgressivePassesGrid()
fig = grid.create(
    events=events,
    team_name="Argentina",           # Team to analyze
    compare_to="season_average",     # Comparison baseline
    title="Progressive Passing Zones"
)
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data with pass locations |
| `team_name` | str | Team to analyze |
| `compare_to` | str | "season_average" or "opponent" |
| `title` | str | Chart title |

---

### 2. Crossing Zones Heatmap

Displays where crosses originate from on the pitch.

```python
from src.visualizations.crossing_zones import CrossingZonesMap

crossing_map = CrossingZonesMap()
fig = crossing_map.create(
    events=events,
    team_name="France",
    show_success_rate=True,
    title="Crossing Origins"
)
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `team_name` | str | Team to analyze |
| `show_success_rate` | bool | Overlay success percentages |
| `title` | str | Chart title |

---

### 3. Contested Zones / Territorial Control

Shows which team dominates different pitch areas.

```python
from src.visualizations.zone_control import ZoneControlMap

zone_map = ZoneControlMap()
fig = zone_map.create(
    events=events,
    home_team="Argentina",
    away_team="France",
    metric="touches",      # or "passes", "duels"
    title="Territorial Control"
)
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `home_team` | str | Home team name |
| `away_team` | str | Away team name |
| `metric` | str | "touches", "passes", or "duels" |
| `title` | str | Chart title |

---

### 4. Player Shot Map

Individual player shot locations with xG coloring.

```python
from src.visualizations.shot_map import ShotMap

shot_map = ShotMap()
fig = shot_map.create(
    shots=player_shots,         # DataFrame of shots
    player_name="Kylian Mbappé",
    show_xg=True,               # Color by xG value
    show_goals=True,            # Highlight goals
    title="Shot Map"
)
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `shots` | DataFrame | Shot event data |
| `player_name` | str | Player name for title |
| `show_xg` | bool | Color shots by xG |
| `show_goals` | bool | Highlight goals differently |
| `title` | str | Chart title |

---

### 5. Touch Heatmap

Player activity zones across the pitch.

```python
from src.visualizations.touch_heatmap import TouchHeatmap

heatmap = TouchHeatmap()
fig = heatmap.create(
    events=events,
    player_name="Lionel Andrés Messi Cuccittini",
    cmap="aurora",              # Brand colormap
    title="Touch Heatmap"
)
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `player_name` | str | Player to analyze |
| `cmap` | str | Colormap ("aurora", "cyan", "magenta") |
| `title` | str | Chart title |

---

## 🎬 Animations

### Event Sequence Animation

```python
from src.animations.match_animation import MatchAnimator

animator = MatchAnimator(events, fps=10)

# Animate a time range
anim = animator.create_event_sequence_animation(
    team_name="Argentina",
    time_range=(118, 122),      # Minutes (Messi's goal in ET)
    event_types=['Pass', 'Carry', 'Shot'],
    show_trails=True,
    trail_length=5,
    title="Argentina Goal Build-up"
)

# Save as GIF
animator.save_gif("argentina_goal.gif", fps=8, dpi=150)
```

**Inputs:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `events` | DataFrame | Match event data |
| `fps` | int | Frames per second |
| `team_name` | str | Filter by team |
| `time_range` | tuple | (start_minute, end_minute) |
| `event_types` | list | Event types to include |
| `show_trails` | bool | Show previous positions |
| `trail_length` | int | Number of trailing events |
| `title` | str | Animation title |

---

### Pass Flow Animation

```python
animator = MatchAnimator(events, fps=5)

anim = animator.create_pass_flow_animation(
    team_name="France",
    time_range=(0, 45),         # First half
    title="France First Half Passing"
)

animator.save_gif("france_passes.gif", fps=3)
```

---

### Goal Sequence Animation

```python
from src.animations.match_animation import GoalSequenceAnimator

goal_animator = GoalSequenceAnimator(events)

# Get all goals
goals = goal_animator.get_goals()
print(goals[['minute', 'player', 'shot_outcome']])

# Animate specific goal buildup
anim = goal_animator.animate_goal(
    goal_index=goals.index[0],   # First goal
    num_buildup_events=10,       # Events before goal
    fps=5
)
```

---

## 📱 Instagram Export & Posting

### Quick Export

```python
from src.export.instagram import InstagramExporter

exporter = InstagramExporter()

# Export as square post (1080x1080)
exporter.export_post(fig, 'shot_map.png', format='square', add_watermark=True, watermark_text='@divisionfc')

# Export as story (1080x1920)  
exporter.export_story(fig, 'shot_map_story.png', add_watermark=True)

# Export animation as reel
exporter.export_reel(anim, 'goal_sequence.mp4', fps=30)
```

### Posting Options

| Method | Best For |
|--------|----------|
| **Instagram App** | Quick manual posts |
| **Meta Business Suite** | Scheduling, analytics |
| **Graph API** | Automated posting (business accounts) |

### Export Formats

| Format | Dimensions | Use Case |
|--------|------------|----------|
| Square Post | 1080 × 1080 | Feed posts |
| Portrait Post | 1080 × 1350 | Taller visualizations |
| Story/Reel | 1080 × 1920 | Stories & Reels |

📖 **Full guide:** [docs/INSTAGRAM_GUIDE.md](docs/INSTAGRAM_GUIDE.md)

---

## 🎨 Brand Identity

### Midnight Aurora Color Palette

```python
from src.branding.style import ColorPalette

colors = ColorPalette()

# Background colors
colors.DEEP_SPACE      # #0D1117 - Primary background
colors.CHARCOAL        # #161B22 - Secondary background
colors.SLATE           # #21262D - Tertiary

# Aurora accent colors
colors.CYAN            # #00FFCC - Primary accent
colors.MAGENTA         # #FF66B2 - Secondary accent
colors.PURPLE          # #AA66FF - Tertiary accent
colors.GOLD            # #FFD700 - Highlight accent

# Functional colors
colors.SUCCESS         # #3FB950 - Positive outcomes
colors.DANGER          # #F85149 - Negative outcomes
```

### Apply Brand Styling

```python
from src.branding.style import apply_brand_style, BrandElements

# Apply to any matplotlib figure
apply_brand_style(fig, ax)

# Add watermark
BrandElements.add_watermark(ax, "DIVISION FC")

# Add signature accent bar
BrandElements.add_accent_bar(ax, position='bottom-left')
```

---

## 📁 Project Structure

```
division-fc-analytics/
├── assets/
│   └── division_fc_logo_v3.svg    # Brand logo
├── config/
│   └── settings.py                 # Configuration
├── data/                           # Data storage
├── docs/
│   ├── BRAND_GUIDE.md             # Brand guidelines
│   └── API_REFERENCE.md           # Full API docs
├── examples/
│   ├── quick_start.py             # Basic usage
│   ├── world_cup_analysis.py      # Full demo
│   └── create_animations.py       # Animation examples
├── notebooks/
│   └── exploration.ipynb          # Jupyter notebook
├── output/                         # Generated files
│   ├── images/
│   ├── gifs/
│   └── videos/
├── src/
│   ├── animations/
│   │   └── match_animation.py     # Animation classes
│   ├── branding/
│   │   ├── style.py               # Brand styling
│   │   └── chart_templates.py     # Branded charts
│   ├── data/
│   │   └── statsbomb_loader.py    # Data loading
│   └── visualizations/
│       ├── shot_map.py
│       ├── touch_heatmap.py
│       ├── zone_control.py
│       └── ...
├── tests/                          # Unit tests
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 🙏 Credits & Acknowledgments

### Data Sources

- **[StatsBomb Open Data](https://github.com/statsbomb/open-data)**  
  Free football event data including FIFA World Cup 2022.  
  Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
  
  > StatsBomb are quite simply the best in the business. Thank you for making this data freely available.

### Libraries & Tools

- **[mplsoccer](https://mplsoccer.readthedocs.io/)** - Football pitch plotting library  
  Created by Andrew Rowlinson. MIT License.
  
- **[matplotlib](https://matplotlib.org/)** - Visualization library  
  BSD License.
  
- **[pandas](https://pandas.pydata.org/)** - Data manipulation  
  BSD 3-Clause License.
  
- **[NumPy](https://numpy.org/)** - Numerical computing  
  BSD License.

### Inspiration

- **[Son of a Corner](https://github.com/sonofacorner/soc-viz-of-the-week)**  
  Visualization styles and techniques inspired by the "Viz of the Week" series.  
  Created by [@sonofacorner](https://twitter.com/sonofacorner).

### Brand Identity

- **Division FC** brand identity created with the "Midnight Aurora" theme
- Logo designed with dual-eye division symbol concept

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Data License

StatsBomb data is provided under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You must give appropriate credit when using this data.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📬 Contact

**Division FC** - Soccer Analytics

- GitHub: [@yourusername](https://github.com/yourusername)
- Twitter: [@divisionfc](https://twitter.com/divisionfc)
- Instagram: [@divisionfc](https://instagram.com/divisionfc)

---

<p align="center">
  Made with ⚽ by Division FC
</p>

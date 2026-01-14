# Division FC Soccer Analytics - Complete Project Pipeline

## 🎯 Project Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DIVISION FC SOCCER ANALYTICS                         │
│                                                                             │
│     Professional soccer visualizations with "Midnight Aurora" branding      │
│                                                                             │
│  Data Source: StatsBomb Open Data (CC BY 4.0)                              │
│  Demo Match: FIFA World Cup 2022 Final - Argentina vs France               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Complete Pipeline

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              PIPELINE OVERVIEW                                │
└──────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │   STAGE 1   │───▶│   STAGE 2   │───▶│   STAGE 3   │───▶│   STAGE 4   │
  │    DATA     │    │  ANALYSIS   │    │VISUALIZATION│    │   EXPORT    │
  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
        │                  │                  │                  │
        ▼                  ▼                  ▼                  ▼
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │ • StatsBomb │    │ • Shots     │    │ • Shot Maps │    │ • Instagram │
  │ • Dynamic   │    │ • Passes    │    │ • Heatmaps  │    │ • PNG/MP4   │
  │   Loading   │    │ • Goals     │    │ • Networks  │    │ • Captions  │
  │ • No IDs    │    │ • xG        │    │ • Animations│    │ • Hashtags  │
  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 🔧 Stage 1: Data Loading (Dynamic)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         STAGE 1: DATA LOADING                                 │
│                     All IDs sourced from API - Nothing hardcoded              │
└──────────────────────────────────────────────────────────────────────────────┘

                          ┌─────────────────────┐
                          │   StatsBomb API     │
                          │  (Open Data - Free) │
                          └──────────┬──────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
           ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
           │ Competitions │  │   Matches    │  │   Events     │
           │              │  │              │  │              │
           │ • World Cup  │  │ • Finals     │  │ • Shots      │
           │ • UCL        │  │ • Semis      │  │ • Passes     │
           │ • La Liga    │  │ • Group      │  │ • Carries    │
           │ • etc...     │  │ • etc...     │  │ • etc...     │
           └──────────────┘  └──────────────┘  └──────────────┘
                    │                │                │
                    └────────────────┼────────────────┘
                                     ▼
                          ┌─────────────────────┐
                          │  StatsBombLoader    │
                          │                     │
                          │ find_competition()  │
                          │ find_final()        │
                          │ load_events()       │
                          └─────────────────────┘
```

### Code Example

```python
from src.data.loader import StatsBombLoader

loader = StatsBombLoader()

# ❌ OLD WAY (hardcoded)
# match_id = 3869685  # Don't do this!

# ✅ NEW WAY (dynamic)
events, match_info = loader.load_match_by_criteria(
    competition_name="World Cup",    # Search by name
    stage="Final"                     # Find dynamically
)

# All values extracted FROM data
home_team = match_info['home_team']   # "Argentina"
away_team = match_info['away_team']   # "France"  
match_id = match_info['match_id']     # 3869685 (sourced, not hardcoded)
```

---

## 📈 Stage 2: Data Analysis

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         STAGE 2: DATA ANALYSIS                                │
│                      Extract insights from event data                         │
└──────────────────────────────────────────────────────────────────────────────┘

                          ┌─────────────────────┐
                          │    Events Data      │
                          │   (~3000 events)    │
                          └──────────┬──────────┘
                                     │
         ┌───────────────┬───────────┼───────────┬───────────────┐
         ▼               ▼           ▼           ▼               ▼
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │   Shots     │ │   Passes    │ │   Goals     │ │  Touches    │ │   Stats     │
  │             │ │             │ │             │ │             │ │             │
  │ get_shots() │ │ get_passes()│ │ get_goals() │ │ by player   │ │ xG, poss.   │
  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
         │               │           │           │               │
         └───────────────┴───────────┼───────────┴───────────────┘
                                     ▼
                    ┌────────────────────────────────┐
                    │     get_top_players_by_stat()  │
                    │                                │
                    │  • Top shooters                │
                    │  • Top passers                 │
                    │  • Most touches                │
                    │  • Goal scorers                │
                    └────────────────────────────────┘
```

### Utility Functions

```python
from src.data.loader import (
    get_teams,              # Extract team names
    get_players,            # Get all players
    get_goals,              # Extract goals
    get_shots,              # Get shot events
    get_passes,             # Get pass events
    calculate_xg,           # Sum expected goals
    calculate_possession,   # Possession %
    get_top_players_by_stat,# Find top performers
    get_match_stats         # Complete match stats
)

# Example: Get top shooter (from data)
top_shooters = get_top_players_by_stat(events, home_team, stat='shots', n=1)
player_name = top_shooters[0]  # Sourced from data!
```

---

## 🎨 Stage 3: Visualization

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        STAGE 3: VISUALIZATION                                 │
│                    5 Visualization Types + Animations                         │
└──────────────────────────────────────────────────────────────────────────────┘

                     ┌─────────────────────────────────┐
                     │      "Midnight Aurora" Theme    │
                     │                                 │
                     │  Background: #0D1117            │
                     │  Cyan:       #00FFCC            │
                     │  Magenta:    #FF66B2            │
                     │  Purple:     #AA66FF            │
                     │  Gold:       #FFD700            │
                     └────────────────┬────────────────┘
                                      │
        ┌──────────────┬──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼
 ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
 │  Shot Map  │ │  Heatmap   │ │Pass Network│ │Zone Control│ │  Summary   │
 │            │ │            │ │            │ │            │ │            │
 │ Half-pitch │ │ Full-pitch │ │ Nodes+Lines│ │ Grid zones │ │ Instagram  │
 │ xG colored │ │ Gaussian   │ │ Avg pos.   │ │ Dominance  │ │ Square     │
 └────────────┘ └────────────┘ └────────────┘ └────────────┘ └────────────┘
        │              │              │              │              │
        └──────────────┴──────────────┼──────────────┴──────────────┘
                                      ▼
                           ┌─────────────────────┐
                           │     ANIMATIONS      │
                           │                     │
                           │ • Event sequences   │
                           │ • Pass flows        │
                           │ • Goal buildups     │
                           └─────────────────────┘
```

### Visualization Functions

```python
# All visualizations in world_cup_analysis.py

create_shot_map(events, player_name, filename)
# Inputs: events (DataFrame), player_name (str), filename (str)
# Output: Half-pitch shot locations with xG coloring

create_touch_heatmap(events, player_name, filename)
# Inputs: events (DataFrame), player_name (str), filename (str)
# Output: Full-pitch Gaussian smoothed heatmap

create_pass_network(events, team_name, filename)
# Inputs: events (DataFrame), team_name (str), filename (str)
# Output: Network diagram with nodes and weighted edges

create_zone_control(events, home_team, away_team, filename)
# Inputs: events (DataFrame), home_team (str), away_team (str), filename (str)
# Output: 3x3 grid showing territorial dominance

create_match_summary(events, match_info, filename)
# Inputs: events (DataFrame), match_info (Series), filename (str)
# Output: Instagram-ready square summary graphic
```

### Animation Functions

```python
from src.animations.match_animation import MatchAnimator, GoalSequenceAnimator

# Event sequence animation
animator = MatchAnimator(events, fps=10)
anim = animator.create_event_sequence_animation(
    team_name="Argentina",
    time_range=(118, 122),
    event_types=['Pass', 'Carry', 'Shot'],
    show_trails=True
)
animator.save_gif("goal_buildup.gif", fps=8)

# Goal buildup animation
goal_animator = GoalSequenceAnimator(events)
goals = goal_animator.get_goals()  # From data
anim = goal_animator.animate_goal(goal_index=goals.index[0], num_buildup_events=10)
```

---

## 📱 Stage 4: Export & Instagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        STAGE 4: EXPORT & INSTAGRAM                            │
│                     Multiple formats for different platforms                   │
└──────────────────────────────────────────────────────────────────────────────┘

                     ┌─────────────────────────────────┐
                     │     InstagramExporter           │
                     └────────────────┬────────────────┘
                                      │
        ┌──────────────┬──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼
 ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
 │Square Post │ │Portrait    │ │   Story    │ │    Reel    │ │    GIF     │
 │            │ │   Post     │ │            │ │            │ │            │
 │ 1080x1080  │ │ 1080x1350  │ │ 1080x1920  │ │ 1080x1920  │ │  540x540   │
 │    .png    │ │    .png    │ │    .png    │ │    .mp4    │ │    .gif    │
 └────────────┘ └────────────┘ └────────────┘ └────────────┘ └────────────┘
        │              │              │              │              │
        └──────────────┴──────────────┼──────────────┴──────────────┘
                                      ▼
                     ┌─────────────────────────────────┐
                     │      Caption Generator          │
                     │                                 │
                     │  • Title from player data       │
                     │  • Stats from events            │
                     │  • Hashtags library             │
                     │  • Data credit (StatsBomb)      │
                     └─────────────────────────────────┘
                                      │
                                      ▼
                     ┌─────────────────────────────────┐
                     │      POSTING OPTIONS            │
                     │                                 │
                     │  • Instagram App (manual)       │
                     │  • Meta Business Suite          │
                     │  • Graph API (automated)        │
                     └─────────────────────────────────┘
```

### Export Code

```python
from src.export.instagram import InstagramExporter

exporter = InstagramExporter(output_dir='output')

# Square post (1080x1080)
exporter.export_post(fig, 'post.png', format='square', 
                     add_watermark=True, watermark_text='@divisionfc')

# Story (1080x1920)
exporter.export_story(fig, 'story.png', add_watermark=True)

# Reel from animation (1080x1920)
exporter.export_reel(anim, 'reel.mp4', fps=30)

# GIF for carousel
exporter.export_gif(anim, 'animation.gif', fps=15)
```

---

## 📁 Project Structure

```
soccer-analytics-viz/
│
├── 📂 assets/                          # Brand assets
│   └── division_fc_logo_v3.svg         # Division FC logo (gold prestige)
│
├── 📂 config/                          # Configuration
│   ├── settings.ini                    # Project settings
│   └── pitchpulse.mplstyle            # Matplotlib style
│
├── 📂 data/                            # Data storage (git-ignored)
│   └── .gitkeep
│
├── 📂 docs/                            # Documentation
│   ├── API_REFERENCE.md               # Full API documentation
│   ├── BRAND_GUIDE.md                 # Brand guidelines
│   └── INSTAGRAM_GUIDE.md             # Instagram posting guide
│
├── 📂 examples/                        # Example scripts
│   ├── quick_start.py                 # Minimal test script
│   ├── world_cup_analysis.py          # Full analysis demo
│   └── instagram_export.py            # Instagram export workflow
│
├── 📂 notebooks/                       # Jupyter notebooks
│   └── 01_getting_started.ipynb
│
├── 📂 output/                          # Generated files
│   ├── images/                        # PNG exports
│   ├── gifs/                          # GIF animations
│   └── videos/                        # MP4 reels
│
├── 📂 src/                             # Source code
│   ├── 📂 animations/
│   │   └── match_animation.py         # MatchAnimator, GoalSequenceAnimator
│   │
│   ├── 📂 branding/
│   │   ├── style.py                   # ColorPalette, Typography
│   │   └── chart_templates.py         # Branded chart templates
│   │
│   ├── 📂 data/
│   │   └── loader.py                  # StatsBombLoader (dynamic)
│   │
│   ├── 📂 export/
│   │   └── instagram.py               # InstagramExporter
│   │
│   └── 📂 visualizations/
│       └── pitch.py                   # Pitch visualization utilities
│
├── 📂 tests/                           # Unit tests
│
├── CREDITS.md                          # Formal attributions
├── LICENSE                             # MIT License
├── README.md                           # Main documentation
└── requirements.txt                    # Python dependencies
```

---

## 🚀 Quick Start Commands

```bash
# 1. Setup
unzip soccer-analytics-viz.zip
cd soccer-analytics-viz
pip install -r requirements.txt

# 2. Quick test (verify data loading)
python examples/quick_start.py

# 3. Generate all visualizations
python examples/world_cup_analysis.py

# 4. Instagram-ready export with caption
python examples/instagram_export.py
```

---

## 📊 Output Files

```
After running world_cup_analysis.py:

output/
├── images/
│   ├── messi_shot_map.png           # Messi shots
│   ├── mbappe_shot_map.png          # Mbappé shots
│   ├── messi_heatmap.png            # Messi touches
│   ├── mbappe_heatmap.png           # Mbappé touches
│   ├── argentina_pass_network.png   # Argentina passing
│   ├── france_pass_network.png      # France passing
│   ├── zone_control.png             # Territorial control
│   └── match_summary.png            # Instagram summary
│
└── gifs/
    ├── argentina_goal_1.gif         # First Argentina goal
    └── france_goal_1.gif            # First France goal

After running instagram_export.py:

output/images/
├── instagram_post.png               # 1080x1080 with watermark
└── instagram_story.png              # 1080x1920 with watermark
```

---

## 🙏 Credits & Attributions

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              CREDITS                                          │
└──────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┬────────────────────────────────┬───────────────────────────┐
│     Source      │          Description           │          License          │
├─────────────────┼────────────────────────────────┼───────────────────────────┤
│ StatsBomb       │ Event data (World Cup 2022)    │ CC BY 4.0                 │
│ mplsoccer       │ Pitch plotting library         │ MIT                       │
│ Son of a Corner │ Visualization inspiration      │ -                         │
│ matplotlib      │ Plotting library               │ BSD                       │
│ pandas          │ Data manipulation              │ BSD 3-Clause              │
│ NumPy           │ Numerical computing            │ BSD                       │
│ Pillow          │ Image processing               │ HPND                      │
└─────────────────┴────────────────────────────────┴───────────────────────────┘
```

---

## 🔄 Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐  │
│   │StatsBomb│────▶│ Loader  │────▶│ Events  │────▶│  Viz    │────▶│ Export  │  │
│   │   API   │     │(dynamic)│     │DataFrame│     │Functions│     │Instagram│  │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘  │
│        │               │               │               │               │        │
│        ▼               ▼               ▼               ▼               ▼        │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐  │
│   │ • Comps │     │ • find_ │     │ • Shots │     │ • Shot  │     │ • Post  │  │
│   │ • Matchs│     │   comp  │     │ • Passes│     │   Maps  │     │ • Story │  │
│   │ • Events│     │ • find_ │     │ • Goals │     │ • Heat  │     │ • Reel  │  │
│   │         │     │   final │     │ • xG    │     │   maps  │     │ • GIF   │  │
│   │         │     │ • load_ │     │ • Stats │     │ • Pass  │     │ • Captns│  │
│   │         │     │   match │     │         │     │   Nets  │     │         │  │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘  │
│                                                                                 │
│   ════════════════════════════════════════════════════════════════════════════ │
│                                                                                 │
│   🎨 BRAND: Midnight Aurora     📊 DATA: All Dynamic     📱 OUTPUT: IG Ready   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## ✅ Key Principles

| Principle | Implementation |
|-----------|----------------|
| **No Hardcoded IDs** | `find_competition()`, `find_final()` |
| **Data-Sourced Values** | Team names, players, stats from API |
| **Consistent Branding** | Midnight Aurora palette throughout |
| **Instagram-Ready** | Multiple export formats with watermarks |
| **Proper Attribution** | StatsBomb, mplsoccer, Son of a Corner |
| **Clean Code** | Modular, documented, testable |

---

*Division FC - Professional Soccer Analytics* ⚽

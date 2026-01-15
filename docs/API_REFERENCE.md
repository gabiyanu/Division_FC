# API Reference

## Division FC Soccer Analytics

Complete reference for all visualization and animation functions.

---

## Table of Contents

1. [Data Loading](#data-loading)
2. [Visualizations](#visualizations)
3. [Animations](#animations)
4. [Branding](#branding)

---

## Data Loading

### StatsBomb Data

```python
from mplsoccer import Sbopen

parser = Sbopen()

# Load match events
events, related, freeze, tactics = parser.event(match_id)

# Load competition matches
matches = parser.match(competition_id, season_id)
```

### Key StatsBomb IDs

| Competition | competition_id | season_id | Notes |
|-------------|----------------|-----------|-------|
| World Cup 2022 | 43 | 106 | Full tournament |
| La Liga | 11 | varies | Multiple seasons |
| Premier League | 2 | varies | Multiple seasons |

### World Cup 2022 Final Match ID

```python
MATCH_ID = 3869685  # Argentina vs France
```

---

## Visualizations

### Shot Map

Creates a half-pitch view showing shot locations.

```python
def create_shot_map(
    shots: pd.DataFrame,       # Shot events
    player_name: str,          # Player name for title
    show_xg: bool = True,      # Color by xG value
    show_goals: bool = True,   # Highlight goals
    title: str = "Shot Map"    # Chart title
) -> tuple[Figure, Axes]
```

**Required DataFrame columns:**
- `x`, `y` - Shot location coordinates
- `outcome_name` - Shot outcome (Goal, Saved, etc.)
- `shot_statsbomb_xg` - Expected goals value

**Example:**
```python
shots = events[events['type_name'] == 'Shot']
fig, ax = create_shot_map(shots, "Messi")
fig.savefig('messi_shots.png', dpi=300)
```

---

### Touch Heatmap

Creates a full-pitch heatmap showing player activity zones.

```python
def create_touch_heatmap(
    events: pd.DataFrame,      # All match events
    player_name: str,          # Player to analyze
    cmap: str = "aurora",      # Colormap name
    sigma: float = 1.5,        # Gaussian smoothing
    title: str = "Touch Heatmap"
) -> tuple[Figure, Axes]
```

**Required DataFrame columns:**
- `player_name` - Player identifier
- `x`, `y` - Event location coordinates

**Available colormaps:**
- `"aurora"` - Cyan to magenta gradient
- `"cyan"` - Dark to bright cyan
- `"magenta"` - Dark to bright magenta

---

### Pass Network

Creates a network diagram showing passing connections.

```python
def create_pass_network(
    events: pd.DataFrame,      # Match events
    team_name: str,            # Team to analyze
    min_passes: int = 3,       # Minimum passes to show line
    node_scale: float = 3,     # Node size multiplier
    title: str = "Pass Network"
) -> tuple[Figure, Axes]
```

**Required DataFrame columns:**
- `type_name` - Event type ("Pass")
- `team_name` - Team identifier
- `player_name` - Passer name
- `pass_recipient_name` - Receiver name
- `x`, `y` - Pass origin coordinates
- `outcome_name` - Pass outcome (null = successful)

---

### Zone Control Map

Creates a grid showing territorial dominance.

```python
def create_zone_control(
    events: pd.DataFrame,      # Match events
    home_team: str,            # Home team name
    away_team: str,            # Away team name
    x_zones: int = 3,          # Horizontal divisions
    y_zones: int = 3,          # Vertical divisions
    metric: str = "touches",   # "touches", "passes", "duels"
    title: str = "Zone Control"
) -> tuple[Figure, Axes]
```

**Zone Control Interpretation:**
- **Cyan zones**: Home team dominant (>55%)
- **Magenta zones**: Away team dominant (<45%)
- **Purple zones**: Contested (45-55%)

---

### Match Summary

Creates an Instagram-ready match summary graphic.

```python
def create_match_summary(
    events: pd.DataFrame,      # Match events
    match_info: pd.Series,     # Match metadata
    format: str = "square",    # "square", "story", "wide"
    title: str = "Match Summary"
) -> tuple[Figure, Axes]
```

**Format dimensions:**
- `"square"`: 1080x1080px (Instagram post)
- `"story"`: 1080x1920px (Instagram story)
- `"wide"`: 1920x1080px (YouTube thumbnail)

---

## Animations

### MatchAnimator

Main class for creating event sequence animations.

```python
from src.animations.match_animation import MatchAnimator

animator = MatchAnimator(
    events: pd.DataFrame,      # Match events
    fps: int = 25,             # Frames per second
    figsize: tuple = (12, 8)   # Figure size
)
```

#### create_event_sequence_animation()

```python
anim = animator.create_event_sequence_animation(
    event_indices: list = None,        # Specific event indices
    event_types: list = None,          # Filter by event types
    team_name: str = None,             # Filter by team
    time_range: tuple = None,          # (start_min, end_min)
    title: str = None,                 # Animation title
    show_trails: bool = True,          # Show trailing positions
    trail_length: int = 5              # Number of trailing events
) -> FuncAnimation
```

**Event types to filter:**
- `"Pass"` - Passes
- `"Shot"` - Shots
- `"Carry"` - Ball carries
- `"Duel"` - Duels/tackles
- `"Pressure"` - Pressing events

#### create_pass_flow_animation()

```python
anim = animator.create_pass_flow_animation(
    team_name: str,                    # Team to show
    time_range: tuple = None,          # (start_min, end_min)
    title: str = None                  # Animation title
) -> FuncAnimation
```

#### save_gif()

```python
filepath = animator.save_gif(
    filename: str,                     # Output filename
    output_dir: str = "output/gifs",   # Output directory
    fps: int = None,                   # Override fps
    dpi: int = 100                     # Image resolution
) -> str                               # Returns filepath
```

#### save_video()

```python
filepath = animator.save_video(
    filename: str,                     # Output filename (*.mp4)
    output_dir: str = "output/videos", # Output directory
    fps: int = None,                   # Override fps
    dpi: int = 150,                    # Video resolution
    codec: str = "libx264"             # Video codec
) -> str                               # Returns filepath
```

> **Note:** Video export requires ffmpeg installed on your system.

---

### GoalSequenceAnimator

Specialized animator for goal buildup sequences.

```python
from src.animations.match_animation import GoalSequenceAnimator

goal_animator = GoalSequenceAnimator(events: pd.DataFrame)
```

#### get_goals()

```python
goals_df = goal_animator.get_goals()
# Returns DataFrame of all goals in match
```

#### get_buildup_events()

```python
buildup_df = goal_animator.get_buildup_events(
    goal_index: int,           # Index of goal in events
    num_events: int = 10       # Events before goal
) -> pd.DataFrame
```

#### animate_goal()

```python
anim = goal_animator.animate_goal(
    goal_index: int,           # Index of goal in events
    num_buildup_events: int = 10,
    fps: int = 5,
    figsize: tuple = (12, 8)
) -> FuncAnimation
```

---

## Branding

### ColorPalette

```python
from src.branding.style import ColorPalette

colors = ColorPalette()

# Background colors
colors.DEEP_SPACE           # #0D1117
colors.CHARCOAL             # #161B22
colors.SLATE                # #21262D

# Aurora accent colors
colors.CYAN                 # #00FFCC
colors.MAGENTA              # #FF66B2
colors.PURPLE               # #AA66FF
colors.GOLD                 # #FFD700

# Text colors
colors.TEXT_PRIMARY         # #F0F6FC
colors.TEXT_SECONDARY       # #8B949E

# Functional colors
colors.SUCCESS              # #3FB950
colors.DANGER               # #F85149
```

### apply_brand_style()

```python
from src.branding.style import apply_brand_style

fig, ax = plt.subplots()
# ... create visualization ...
apply_brand_style(fig, ax)
```

### BrandElements

```python
from src.branding.style import BrandElements

# Add watermark
BrandElements.add_watermark(ax, text="DIVISION FC")

# Add accent bar
BrandElements.add_accent_bar(ax, position='bottom-left', color='cyan')
```

### get_brand_cmap()

```python
from src.branding.style import get_brand_cmap

cmap = get_brand_cmap('aurora')    # Full aurora gradient
cmap = get_brand_cmap('cyan')      # Cyan gradient
cmap = get_brand_cmap('magenta')   # Magenta gradient
```

---

## Common Patterns

### Filtering Events

```python
# Shots by player
player_shots = events[
    (events['type_name'] == 'Shot') &
    (events['player_name'] == 'Lionel Andrés Messi Cuccittini')
]

# Successful passes by team
team_passes = events[
    (events['type_name'] == 'Pass') &
    (events['team_name'] == 'Argentina') &
    (events['outcome_name'].isna())  # Successful passes have no outcome
]

# Events in time range
first_half = events[
    (events['minute'] >= 0) &
    (events['minute'] < 45)
]
```

### Saving Figures

```python
# High quality PNG for print
fig.savefig('output.png', dpi=300, bbox_inches='tight', facecolor='#0D1117')

# Instagram optimized
fig.savefig('output.png', dpi=150, bbox_inches='tight', facecolor='#0D1117')

# Transparent background
fig.savefig('output.png', dpi=300, transparent=True)
```

---

## Credits

- **Data**: StatsBomb Open Data (CC BY 4.0)
- **Pitch Plotting**: mplsoccer by Andrew Rowlinson
- **Visualization Inspiration**: Son of a Corner (@sonofacorner)
- **Brand**: Division FC "Midnight Aurora" theme

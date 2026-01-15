"""
Division FC - Match Configuration

THIS IS THE SINGLE SOURCE OF TRUTH FOR MATCH SELECTION.
Change settings here to analyze a different match.
All visualizations and animations will use this config.

Author: Division FC
"""

# =============================================================================
# MATCH CONFIGURATION - CHANGE THESE TO ANALYZE A DIFFERENT MATCH
# =============================================================================

MATCH_CONFIG = {
    # Competition settings
    "competition_name": "FIFA World Cup",  # Search string for competition
    "season": "2022",                       # Season year
    "stage": "Final",                       # Match stage (Final, Semi-final, etc.)
    
    # Alternative: specify teams directly (leave stage empty)
    "home_team": None,                      # e.g., "Argentina"
    "away_team": None,                      # e.g., "France"
    
    # Filter options
    "exclude_youth": True,                  # Exclude U20/U17/Women competitions
}

# =============================================================================
# VISUALIZATION SETTINGS
# =============================================================================

VIZ_CONFIG = {
    # Goal filtering
    "regulation_only": False,               # Include extra time goals
    
    # Player name display
    "use_display_names": False,             # Use full names (not shortened)
    
    # Output settings
    "save_images": True,
    "show_plots": True,
    "dpi": 300,
}

# =============================================================================
# BRAND COLORS - Midnight Aurora Theme
# =============================================================================

COLORS = {
    'background': '#0D1117',
    'cyan': '#00FFCC',
    'magenta': '#FF66B2',
    'purple': '#AA66FF',
    'gold': '#FFD700',
    'text': '#F0F6FC',
    'text_secondary': '#8B949E',
    'pitch_line': '#8B949E',
}

# =============================================================================
# INSTAGRAM SETTINGS
# =============================================================================

INSTAGRAM_CONFIG = {
    "handle": "@divisionfc",
    "add_watermark": True,
    "post_size": (1080, 1080),
    "story_size": (1080, 1920),
}

# =============================================================================
# OUTPUT DIRECTORIES
# =============================================================================

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
GIFS_DIR = OUTPUT_DIR / "gifs"
VIDEOS_DIR = OUTPUT_DIR / "videos"

# Create directories
for dir_path in [IMAGES_DIR, GIFS_DIR, VIDEOS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


# =============================================================================
# LOAD MATCH DATA (cached)
# =============================================================================

_cached_data = {}

def get_match_data():
    """
    Load match data based on MATCH_CONFIG.
    Cached so it only loads once.
    
    Returns:
        tuple: (events DataFrame, match_info Series)
    """
    if 'events' not in _cached_data:
        from src.data.loader import StatsBombLoader
        
        loader = StatsBombLoader()
        events, match_info = loader.load_match_by_criteria(
            competition_name=MATCH_CONFIG['competition_name'],
            season=MATCH_CONFIG['season'],
            stage=MATCH_CONFIG['stage'],
            home_team=MATCH_CONFIG['home_team'],
            away_team=MATCH_CONFIG['away_team'],
        )
        
        _cached_data['events'] = events
        _cached_data['match_info'] = match_info
        _cached_data['home_team'] = match_info['home_team']
        _cached_data['away_team'] = match_info['away_team']
        
        print(f"✅ Loaded: {match_info['home_team']} vs {match_info['away_team']}")
        print(f"   Score: {int(match_info['home_score'])} - {int(match_info['away_score'])}")
        print(f"   Date: {match_info['match_date']}")
    
    return _cached_data['events'], _cached_data['match_info']


def get_home_team():
    """Get home team name."""
    if 'home_team' not in _cached_data:
        get_match_data()
    return _cached_data['home_team']


def get_away_team():
    """Get away team name."""
    if 'away_team' not in _cached_data:
        get_match_data()
    return _cached_data['away_team']

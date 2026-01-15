"""
=============================================================================
                        PITCH PULSE - BRAND IDENTITY
=============================================================================

Your unique soccer analytics brand with a distinctive dark mode aesthetic,
neon accents, and gradient-based visualizations.

Brand Philosophy:
- Dark, cinematic backgrounds that make data "pop"
- Electric/neon accent colors for energy and impact
- Clean, modern typography
- Signature visual elements that are instantly recognizable

This file defines your brand constants - colors, fonts, and styling rules
that will be used across all visualizations.
"""

# =============================================================================
# COLOR PALETTE
# =============================================================================

# Primary Background Colors (Dark Mode)
BACKGROUND_PRIMARY = "#0d1117"      # Deep space black
BACKGROUND_SECONDARY = "#161b22"    # Elevated surface
BACKGROUND_PITCH = "#1a2332"        # Pitch background (dark blue-gray)

# Accent Colors (Neon/Electric)
ACCENT_CYAN = "#00f5ff"             # Electric cyan (primary accent)
ACCENT_MAGENTA = "#ff00aa"          # Hot magenta (secondary accent)
ACCENT_GOLD = "#ffd700"             # Championship gold (highlights)
ACCENT_LIME = "#39ff14"             # Neon lime (goals/success)

# Gradient Pairs (for creating striking visual effects)
GRADIENT_OCEAN = ("#00f5ff", "#0066ff")     # Cyan to blue
GRADIENT_FIRE = ("#ff00aa", "#ff6b35")      # Magenta to orange
GRADIENT_AURORA = ("#00f5ff", "#ff00aa")    # Cyan to magenta (signature!)
GRADIENT_GOLD = ("#ffd700", "#ff8c00")      # Gold to orange

# Text Colors
TEXT_PRIMARY = "#ffffff"            # White for headers
TEXT_SECONDARY = "#8b949e"          # Muted gray for labels
TEXT_ACCENT = "#00f5ff"             # Cyan for highlighted text

# Data Visualization Colors
VIZ_POSITIVE = "#39ff14"            # Goals, successful actions
VIZ_NEGATIVE = "#ff4444"            # Missed, unsuccessful
VIZ_NEUTRAL = "#8b949e"             # Neutral data points
VIZ_HOME_TEAM = "#00f5ff"           # Home team (cyan)
VIZ_AWAY_TEAM = "#ff00aa"           # Away team (magenta)

# Heat Map Colors (custom colormap endpoints)
HEATMAP_COLD = "#0d1117"            # No activity
HEATMAP_WARM = "#00f5ff"            # Medium activity
HEATMAP_HOT = "#ff00aa"             # High activity

# Pitch Colors
PITCH_GRASS = "#1a2332"             # Dark pitch surface
PITCH_LINES = "#3d4f5f"             # Subtle pitch lines
PITCH_LINES_ACCENT = "#00f5ff"      # Highlighted zones

# =============================================================================
# TYPOGRAPHY
# =============================================================================

# Font Stack (use these in order of preference)
FONT_TITLE = "Orbitron"             # Futuristic, bold titles
FONT_HEADING = "Rajdhani"           # Clean, modern headings
FONT_BODY = "Inter"                 # Highly readable body text
FONT_MONO = "JetBrains Mono"        # Stats and numbers

# Fallback fonts (system fonts)
FONT_FALLBACK = "DejaVu Sans"

# Font Sizes
SIZE_TITLE = 28
SIZE_SUBTITLE = 18
SIZE_HEADING = 14
SIZE_BODY = 11
SIZE_CAPTION = 9
SIZE_STATS = 24                     # Large stats numbers

# Font Weights
WEIGHT_BOLD = "bold"
WEIGHT_SEMIBOLD = "semibold"
WEIGHT_REGULAR = "regular"
WEIGHT_LIGHT = "light"

# =============================================================================
# SIGNATURE VISUAL ELEMENTS
# =============================================================================

# Glow Effect Parameters
GLOW_RADIUS = 15
GLOW_ALPHA = 0.3

# Gradient Mesh Density
MESH_DENSITY = 50

# Ring/Pulse Animation
PULSE_RINGS = 3
PULSE_DURATION = 2.0  # seconds

# Border/Frame
FRAME_CORNER_RADIUS = 12
FRAME_BORDER_WIDTH = 2
FRAME_BORDER_COLOR = "#00f5ff"

# Watermark
WATERMARK_TEXT = "@pitchpulse"      # Your Instagram handle
WATERMARK_OPACITY = 0.6
WATERMARK_POSITION = "bottom_right"

# =============================================================================
# BRAND VARIATIONS (for different content types)
# =============================================================================

# Standard Post (1080x1080)
POST_STYLE = {
    "background": BACKGROUND_PRIMARY,
    "accent": ACCENT_CYAN,
    "title_size": SIZE_TITLE,
}

# Story/Reel (1080x1920)
STORY_STYLE = {
    "background": BACKGROUND_PRIMARY,
    "accent": GRADIENT_AURORA,
    "title_size": SIZE_TITLE + 4,
}

# Match Report
MATCH_STYLE = {
    "home_color": VIZ_HOME_TEAM,
    "away_color": VIZ_AWAY_TEAM,
    "background": BACKGROUND_PRIMARY,
}

# Player Spotlight
PLAYER_STYLE = {
    "highlight_color": ACCENT_GOLD,
    "background": BACKGROUND_SECONDARY,
}

# =============================================================================
# EXPORTABLE CONSTANTS
# =============================================================================

# Complete color palette as dict
COLORS = {
    "bg_primary": BACKGROUND_PRIMARY,
    "bg_secondary": BACKGROUND_SECONDARY,
    "bg_pitch": BACKGROUND_PITCH,
    "accent_cyan": ACCENT_CYAN,
    "accent_magenta": ACCENT_MAGENTA,
    "accent_gold": ACCENT_GOLD,
    "accent_lime": ACCENT_LIME,
    "text_primary": TEXT_PRIMARY,
    "text_secondary": TEXT_SECONDARY,
    "positive": VIZ_POSITIVE,
    "negative": VIZ_NEGATIVE,
    "home": VIZ_HOME_TEAM,
    "away": VIZ_AWAY_TEAM,
}

# Font configuration
FONTS = {
    "title": FONT_TITLE,
    "heading": FONT_HEADING,
    "body": FONT_BODY,
    "mono": FONT_MONO,
    "fallback": FONT_FALLBACK,
}

# Sizes configuration
SIZES = {
    "title": SIZE_TITLE,
    "subtitle": SIZE_SUBTITLE,
    "heading": SIZE_HEADING,
    "body": SIZE_BODY,
    "caption": SIZE_CAPTION,
    "stats": SIZE_STATS,
}

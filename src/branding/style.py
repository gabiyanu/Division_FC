"""
🎨 CUSTOM BRANDING & STYLING SYSTEM
====================================
Unique visual identity for your soccer analytics content.

Brand Name: [YOUR BRAND NAME HERE]
Style: Modern Minimalist with Bold Accents

This module defines your exclusive visual identity that makes
your Instagram content instantly recognizable.
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass


# =============================================================================
# 🎨 COLOR PALETTE - "MIDNIGHT AURORA"
# =============================================================================
# A distinctive palette inspired by northern lights over a night sky.
# Dark, sophisticated backgrounds with vibrant accent colors.

@dataclass
class ColorPalette:
    """Your exclusive color palette - Midnight Aurora theme."""
    
    # Primary Background Colors
    BACKGROUND_DARK: str = "#0D1117"      # Deep space black
    BACKGROUND_MEDIUM: str = "#161B22"    # Charcoal
    BACKGROUND_LIGHT: str = "#21262D"     # Slate gray
    
    # Primary Accent Colors (The Aurora)
    AURORA_CYAN: str = "#58D9C4"          # Primary accent - Teal/Cyan
    AURORA_MAGENTA: str = "#E056A0"       # Secondary accent - Magenta pink
    AURORA_PURPLE: str = "#A371F7"        # Tertiary accent - Soft purple
    AURORA_GOLD: str = "#F5C344"          # Highlight - Warm gold
    
    # Functional Colors
    SUCCESS: str = "#3FB950"              # Positive metrics (green)
    DANGER: str = "#F85149"               # Negative metrics (red)
    WARNING: str = "#D29922"              # Caution (amber)
    NEUTRAL: str = "#8B949E"              # Neutral/secondary text
    
    # Text Colors
    TEXT_PRIMARY: str = "#F0F6FC"         # Primary text (almost white)
    TEXT_SECONDARY: str = "#8B949E"       # Secondary text (gray)
    TEXT_MUTED: str = "#484F58"           # Muted text (dark gray)
    
    # Pitch Colors
    PITCH_GREEN: str = "#1B4D3E"          # Dark grass green
    PITCH_LINES: str = "#FFFFFF"          # White lines
    PITCH_ACCENT: str = "#2E7D5B"         # Lighter pitch area
    
    # Gradient definitions
    @property
    def gradient_aurora(self) -> List[str]:
        """Main aurora gradient - cyan to purple to magenta."""
        return [self.AURORA_CYAN, self.AURORA_PURPLE, self.AURORA_MAGENTA]
    
    @property
    def gradient_heat(self) -> List[str]:
        """Heat map gradient - dark to gold."""
        return [self.BACKGROUND_DARK, self.WARNING, self.AURORA_GOLD]
    
    @property
    def gradient_performance(self) -> List[str]:
        """Performance gradient - red to gold to green."""
        return [self.DANGER, self.AURORA_GOLD, self.SUCCESS]


# Instantiate the palette
COLORS = ColorPalette()


# =============================================================================
# 🔤 TYPOGRAPHY
# =============================================================================

@dataclass
class Typography:
    """Your brand typography settings."""
    
    # Font families (fallbacks for different systems)
    FONT_TITLE: str = "Inter"             # Clean, modern titles
    FONT_BODY: str = "Inter"              # Body text
    FONT_MONO: str = "JetBrains Mono"     # Stats/numbers
    FONT_FALLBACK: str = "DejaVu Sans"    # System fallback
    
    # Font sizes (in points)
    SIZE_HERO: int = 32                   # Main title
    SIZE_TITLE: int = 24                  # Section titles
    SIZE_SUBTITLE: int = 18               # Subtitles
    SIZE_BODY: int = 14                   # Body text
    SIZE_CAPTION: int = 11                # Captions/labels
    SIZE_MICRO: int = 9                   # Small annotations
    
    # Font weights
    WEIGHT_BOLD: str = "bold"
    WEIGHT_SEMIBOLD: str = "semibold"
    WEIGHT_REGULAR: str = "regular"
    WEIGHT_LIGHT: str = "light"


TYPOGRAPHY = Typography()


# =============================================================================
# 📐 LAYOUT & SPACING
# =============================================================================

@dataclass
class Layout:
    """Layout and spacing constants."""
    
    # Instagram dimensions
    POST_SQUARE: Tuple[int, int] = (1080, 1080)
    POST_PORTRAIT: Tuple[int, int] = (1080, 1350)
    STORY: Tuple[int, int] = (1080, 1920)
    
    # Figure sizes (inches) for different outputs
    FIG_SQUARE: Tuple[float, float] = (10.8, 10.8)
    FIG_PORTRAIT: Tuple[float, float] = (10.8, 13.5)
    FIG_WIDE: Tuple[float, float] = (14.4, 10.8)
    
    # Padding and margins (as fraction of figure)
    MARGIN_TOP: float = 0.12              # Space for title
    MARGIN_BOTTOM: float = 0.08           # Space for watermark
    MARGIN_SIDES: float = 0.06            # Side margins
    
    # Grid spacing
    GRID_GAP: float = 0.02                # Gap between grid items


LAYOUT = Layout()


# =============================================================================
# 🎯 BRAND ELEMENTS
# =============================================================================

class BrandElements:
    """Signature visual elements for brand recognition."""
    
    # Watermark/Logo text
    BRAND_NAME: str = "@YOUR_HANDLE"      # Change this!
    TAGLINE: str = "Soccer Analytics"
    
    # Signature corner accent (a small colored bar)
    ACCENT_BAR_WIDTH: float = 0.15        # 15% of figure width
    ACCENT_BAR_HEIGHT: float = 0.008      # Thin bar
    
    # Title underline style
    TITLE_UNDERLINE_WIDTH: float = 0.3
    TITLE_UNDERLINE_HEIGHT: float = 0.004
    
    @staticmethod
    def get_signature_gradient():
        """Returns the signature aurora gradient for matplotlib."""
        return LinearSegmentedColormap.from_list(
            "aurora",
            [COLORS.AURORA_CYAN, COLORS.AURORA_PURPLE, COLORS.AURORA_MAGENTA],
            N=256
        )
    
    @staticmethod
    def get_heat_cmap():
        """Returns custom heat colormap."""
        return LinearSegmentedColormap.from_list(
            "custom_heat",
            [COLORS.BACKGROUND_DARK, COLORS.AURORA_PURPLE, COLORS.AURORA_MAGENTA, COLORS.AURORA_GOLD],
            N=256
        )
    
    @staticmethod
    def get_diverging_cmap():
        """Returns diverging colormap for comparison charts."""
        return LinearSegmentedColormap.from_list(
            "diverging",
            [COLORS.DANGER, COLORS.BACKGROUND_MEDIUM, COLORS.SUCCESS],
            N=256
        )


BRAND = BrandElements()


# =============================================================================
# 🖼️ MATPLOTLIB STYLE CONFIGURATION
# =============================================================================

def apply_brand_style():
    """
    Apply the complete brand style to matplotlib.
    Call this at the start of your visualization scripts.
    """
    
    # Reset to default first
    plt.style.use('default')
    
    # Background colors
    rcParams['figure.facecolor'] = COLORS.BACKGROUND_DARK
    rcParams['axes.facecolor'] = COLORS.BACKGROUND_MEDIUM
    rcParams['savefig.facecolor'] = COLORS.BACKGROUND_DARK
    
    # Text colors
    rcParams['text.color'] = COLORS.TEXT_PRIMARY
    rcParams['axes.labelcolor'] = COLORS.TEXT_PRIMARY
    rcParams['xtick.color'] = COLORS.TEXT_SECONDARY
    rcParams['ytick.color'] = COLORS.TEXT_SECONDARY
    
    # Font settings
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = [
        TYPOGRAPHY.FONT_TITLE, 
        TYPOGRAPHY.FONT_FALLBACK, 
        'Arial', 
        'Helvetica'
    ]
    rcParams['font.size'] = TYPOGRAPHY.SIZE_BODY
    
    # Axes styling
    rcParams['axes.edgecolor'] = COLORS.BACKGROUND_LIGHT
    rcParams['axes.linewidth'] = 0.8
    rcParams['axes.grid'] = True
    rcParams['grid.color'] = COLORS.BACKGROUND_LIGHT
    rcParams['grid.alpha'] = 0.3
    rcParams['grid.linewidth'] = 0.5
    
    # Legend styling
    rcParams['legend.facecolor'] = COLORS.BACKGROUND_MEDIUM
    rcParams['legend.edgecolor'] = COLORS.BACKGROUND_LIGHT
    rcParams['legend.fontsize'] = TYPOGRAPHY.SIZE_CAPTION
    
    # Tick styling
    rcParams['xtick.major.size'] = 0
    rcParams['ytick.major.size'] = 0
    rcParams['xtick.labelsize'] = TYPOGRAPHY.SIZE_CAPTION
    rcParams['ytick.labelsize'] = TYPOGRAPHY.SIZE_CAPTION
    
    # Figure settings
    rcParams['figure.dpi'] = 100
    rcParams['savefig.dpi'] = 150
    rcParams['savefig.bbox'] = 'tight'
    rcParams['savefig.pad_inches'] = 0.1


# =============================================================================
# 🎨 CHART-SPECIFIC STYLING FUNCTIONS
# =============================================================================

class ChartStyler:
    """
    Styling functions for each of the 7 chart types.
    Each returns a styled figure with your brand identity.
    """
    
    def __init__(self):
        apply_brand_style()
    
    def style_title(
        self,
        ax: plt.Axes,
        title: str,
        subtitle: Optional[str] = None,
        add_underline: bool = True
    ):
        """Add branded title with optional underline accent."""
        # Main title
        ax.text(
            0.5, 1.08, title,
            transform=ax.transAxes,
            fontsize=TYPOGRAPHY.SIZE_TITLE,
            fontweight=TYPOGRAPHY.WEIGHT_BOLD,
            color=COLORS.TEXT_PRIMARY,
            ha='center', va='bottom'
        )
        
        # Subtitle
        if subtitle:
            ax.text(
                0.5, 1.02, subtitle,
                transform=ax.transAxes,
                fontsize=TYPOGRAPHY.SIZE_CAPTION,
                fontweight=TYPOGRAPHY.WEIGHT_REGULAR,
                color=COLORS.TEXT_SECONDARY,
                ha='center', va='bottom'
            )
        
        # Signature underline with gradient effect
        if add_underline:
            underline_width = BRAND.TITLE_UNDERLINE_WIDTH
            ax.axhline(
                y=1.05, 
                xmin=0.5 - underline_width/2, 
                xmax=0.5 + underline_width/2,
                color=COLORS.AURORA_CYAN,
                linewidth=3,
                transform=ax.transAxes,
                clip_on=False
            )
    
    def add_watermark(self, fig: plt.Figure):
        """Add branded watermark to bottom of figure."""
        fig.text(
            0.98, 0.02,
            BRAND.BRAND_NAME,
            fontsize=TYPOGRAPHY.SIZE_CAPTION,
            fontweight=TYPOGRAPHY.WEIGHT_SEMIBOLD,
            color=COLORS.AURORA_CYAN,
            ha='right', va='bottom',
            alpha=0.8
        )
        
        # Add small accent bar
        fig.patches.append(plt.Rectangle(
            (0.02, 0.015),
            BRAND.ACCENT_BAR_WIDTH,
            BRAND.ACCENT_BAR_HEIGHT,
            transform=fig.transFigure,
            facecolor=COLORS.AURORA_MAGENTA,
            clip_on=False
        ))
    
    def add_data_source(self, fig: plt.Figure, source: str = "Data: StatsBomb"):
        """Add data source attribution."""
        fig.text(
            0.02, 0.02,
            source,
            fontsize=TYPOGRAPHY.SIZE_MICRO,
            color=COLORS.TEXT_MUTED,
            ha='left', va='bottom'
        )
    
    # =========================================================================
    # CHART TYPE 1: Progressive Passes Grid
    # =========================================================================
    def style_progress_grid(
        self,
        fig: plt.Figure,
        axes: np.ndarray,
        title: str = "Team Progress Analysis"
    ):
        """
        Style for mini-pitch grid showing team improvements.
        Uses aurora gradient for improvement levels.
        """
        fig.patch.set_facecolor(COLORS.BACKGROUND_DARK)
        
        for ax in axes.flat:
            ax.set_facecolor(COLORS.BACKGROUND_MEDIUM)
            for spine in ax.spines.values():
                spine.set_color(COLORS.BACKGROUND_LIGHT)
                spine.set_linewidth(0.5)
        
        # Add title
        fig.suptitle(
            title,
            fontsize=TYPOGRAPHY.SIZE_TITLE,
            fontweight=TYPOGRAPHY.WEIGHT_BOLD,
            color=COLORS.TEXT_PRIMARY,
            y=0.98
        )
        
        self.add_watermark(fig)
        return fig
    
    # =========================================================================
    # CHART TYPE 2: Player Stats Table
    # =========================================================================
    def get_table_colors(self) -> Dict:
        """Get colors for styled tables."""
        return {
            'header_bg': COLORS.AURORA_CYAN,
            'header_text': COLORS.BACKGROUND_DARK,
            'row_bg_odd': COLORS.BACKGROUND_MEDIUM,
            'row_bg_even': COLORS.BACKGROUND_LIGHT,
            'row_text': COLORS.TEXT_PRIMARY,
            'bar_fill': COLORS.AURORA_MAGENTA,
            'bar_bg': COLORS.BACKGROUND_LIGHT,
            'highlight': COLORS.AURORA_GOLD
        }
    
    # =========================================================================
    # CHART TYPE 3: Crossing Zones / Heatmap Grid
    # =========================================================================
    def get_zone_cmap(self):
        """Custom colormap for zone heatmaps."""
        return LinearSegmentedColormap.from_list(
            "zone_heat",
            [
                COLORS.BACKGROUND_MEDIUM,
                COLORS.AURORA_PURPLE,
                COLORS.AURORA_MAGENTA,
                COLORS.AURORA_GOLD
            ],
            N=256
        )
    
    # =========================================================================
    # CHART TYPE 4: Scatter Plot
    # =========================================================================
    def style_scatter(
        self,
        ax: plt.Axes,
        highlight_color: str = None
    ):
        """Style scatter plots with brand colors."""
        ax.set_facecolor(COLORS.BACKGROUND_MEDIUM)
        
        # Grid styling
        ax.grid(True, alpha=0.2, color=COLORS.TEXT_MUTED, linestyle='--')
        
        # Spine styling
        for spine in ax.spines.values():
            spine.set_color(COLORS.BACKGROUND_LIGHT)
            spine.set_linewidth(0.5)
        
        return highlight_color or COLORS.AURORA_CYAN
    
    # =========================================================================
    # CHART TYPE 5: Histogram/Distribution
    # =========================================================================
    def style_histogram(
        self,
        ax: plt.Axes,
        primary_color: str = None,
        highlight_color: str = None
    ):
        """Style histograms with brand colors."""
        ax.set_facecolor(COLORS.BACKGROUND_DARK)
        
        return {
            'primary': primary_color or COLORS.AURORA_CYAN,
            'highlight': highlight_color or COLORS.AURORA_GOLD,
            'edge': COLORS.BACKGROUND_DARK,
            'grid': COLORS.BACKGROUND_LIGHT
        }
    
    # =========================================================================
    # CHART TYPE 6: Zone Control Maps
    # =========================================================================
    def get_control_colors(self) -> Dict:
        """Colors for territorial control visualization."""
        return {
            'team_control': COLORS.SUCCESS,        # Team dominates
            'opponent_control': COLORS.DANGER,     # Opponent dominates
            'contested': COLORS.AURORA_PURPLE,     # Contested zones
            'neutral': COLORS.BACKGROUND_LIGHT     # Neutral zones
        }
    
    # =========================================================================
    # CHART TYPE 7: Shot Maps
    # =========================================================================
    def get_shot_colors(self) -> Dict:
        """Colors for shot map visualization."""
        return {
            'goal': COLORS.SUCCESS,
            'saved': COLORS.AURORA_CYAN,
            'blocked': COLORS.WARNING,
            'off_target': COLORS.DANGER,
            'post': COLORS.AURORA_GOLD,
            'hexbin_cmap': self.get_zone_cmap()
        }
    
    def style_shot_map(self, ax: plt.Axes):
        """Apply shot map specific styling."""
        ax.set_facecolor(COLORS.PITCH_GREEN)
        return ax


# =============================================================================
# 🏟️ PITCH STYLING
# =============================================================================

def get_pitch_config() -> Dict:
    """
    Return pitch configuration for mplsoccer.
    Creates a distinctive dark pitch style.
    """
    return {
        'pitch_type': 'statsbomb',
        'pitch_color': COLORS.PITCH_GREEN,
        'line_color': COLORS.PITCH_LINES,
        'linewidth': 1.5,
        'goal_type': 'box',
        'goal_alpha': 0.8,
        'stripe': True,
        'stripe_color': COLORS.PITCH_ACCENT,
        'pad_top': 2,
        'pad_bottom': 2,
        'pad_left': 2,
        'pad_right': 2
    }


# =============================================================================
# 📊 QUICK STYLE PRESETS
# =============================================================================

STYLE_PRESETS = {
    'default': {
        'background': COLORS.BACKGROUND_DARK,
        'accent': COLORS.AURORA_CYAN,
        'secondary': COLORS.AURORA_MAGENTA
    },
    'high_contrast': {
        'background': '#000000',
        'accent': COLORS.AURORA_GOLD,
        'secondary': COLORS.TEXT_PRIMARY
    },
    'soft': {
        'background': COLORS.BACKGROUND_MEDIUM,
        'accent': COLORS.AURORA_PURPLE,
        'secondary': COLORS.AURORA_CYAN
    }
}


# =============================================================================
# 🚀 INITIALIZATION
# =============================================================================

def init_brand():
    """Initialize the brand styling system."""
    apply_brand_style()
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🎨 BRAND STYLING SYSTEM LOADED                              ║
    ║                                                              ║
    ║  Theme: Midnight Aurora                                      ║
    ║  Brand: {BRAND.BRAND_NAME:<20}                            ║
    ║                                                              ║
    ║  Primary Accent:   {COLORS.AURORA_CYAN}                        ║
    ║  Secondary Accent: {COLORS.AURORA_MAGENTA}                        ║
    ║  Tertiary Accent:  {COLORS.AURORA_PURPLE}                        ║
    ║                                                              ║
    ║  Ready to create stunning visualizations! ⚽                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    return ChartStyler()


# Auto-initialize when imported
if __name__ == "__main__":
    styler = init_brand()

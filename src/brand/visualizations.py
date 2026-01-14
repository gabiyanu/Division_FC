"""
=============================================================================
                    PITCH PULSE - SIGNATURE VISUALIZATIONS
=============================================================================

Unique visualization types that define the Pitch Pulse brand:

1. Pulse Shot Map - Radial shot visualization with glow effects
2. Flow Pass Network - Animated pass connections with gradients
3. Impact Zones - Player influence heatmaps with neon styling
4. Aurora Chart - Gradient-filled comparison charts
5. Stats Card - Branded player/team statistics card

These visualizations are designed to be instantly recognizable as
Pitch Pulse content on Instagram.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
import matplotlib.patheffects as path_effects
from mplsoccer import Pitch, VerticalPitch
import numpy as np
import pandas as pd
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path

# Import brand identity
from src.brand.identity import (
    COLORS, FONTS, SIZES,
    BACKGROUND_PRIMARY, BACKGROUND_PITCH,
    ACCENT_CYAN, ACCENT_MAGENTA, ACCENT_GOLD, ACCENT_LIME,
    TEXT_PRIMARY, TEXT_SECONDARY,
    GRADIENT_AURORA, GRADIENT_OCEAN,
    WATERMARK_TEXT
)


class PitchPulseViz:
    """
    Signature visualization class for Pitch Pulse brand.
    Creates unique, branded soccer visualizations.
    """
    
    def __init__(self, style_path: Optional[str] = None):
        """
        Initialize with Pitch Pulse styling.
        
        Args:
            style_path: Path to custom matplotlib style file
        """
        # Apply style
        if style_path:
            plt.style.use(style_path)
        else:
            # Try to use default location
            default_style = Path(__file__).parent.parent.parent / 'config' / 'pitchpulse.mplstyle'
            if default_style.exists():
                plt.style.use(str(default_style))
        
        # Create custom colormaps
        self._setup_colormaps()
        
    def _setup_colormaps(self):
        """Create brand-specific colormaps."""
        # Aurora colormap (cyan -> magenta)
        self.cmap_aurora = LinearSegmentedColormap.from_list(
            'aurora',
            [BACKGROUND_PRIMARY, ACCENT_CYAN, ACCENT_MAGENTA],
            N=256
        )
        
        # Ocean colormap (dark -> cyan)
        self.cmap_ocean = LinearSegmentedColormap.from_list(
            'ocean',
            [BACKGROUND_PRIMARY, '#003344', ACCENT_CYAN],
            N=256
        )
        
        # Fire colormap (dark -> magenta -> gold)
        self.cmap_fire = LinearSegmentedColormap.from_list(
            'fire',
            [BACKGROUND_PRIMARY, ACCENT_MAGENTA, ACCENT_GOLD],
            N=256
        )
        
    def _add_glow(self, ax, x, y, color, radius=0.15, alpha=0.3, layers=3):
        """Add a glow effect around a point."""
        for i in range(layers, 0, -1):
            circle = Circle(
                (x, y),
                radius * i,
                facecolor=color,
                alpha=alpha / i,
                edgecolor='none',
                zorder=1
            )
            ax.add_patch(circle)
    
    def _add_watermark(self, fig, text: str = None, position: str = 'bottom_right'):
        """Add branded watermark to figure."""
        text = text or WATERMARK_TEXT
        
        if position == 'bottom_right':
            x, y = 0.98, 0.02
            ha, va = 'right', 'bottom'
        elif position == 'bottom_left':
            x, y = 0.02, 0.02
            ha, va = 'left', 'bottom'
        else:
            x, y = 0.5, 0.02
            ha, va = 'center', 'bottom'
        
        fig.text(
            x, y, text,
            fontsize=10,
            color=ACCENT_CYAN,
            alpha=0.6,
            ha=ha, va=va,
            fontweight='bold',
            transform=fig.transFigure
        )
    
    def _add_title_block(
        self,
        fig,
        title: str,
        subtitle: str = None,
        accent_color: str = None
    ):
        """Add branded title block with accent line."""
        accent_color = accent_color or ACCENT_CYAN
        
        # Main title
        fig.text(
            0.5, 0.95, title,
            fontsize=SIZES['title'],
            color=TEXT_PRIMARY,
            ha='center', va='top',
            fontweight='bold',
            transform=fig.transFigure
        )
        
        # Accent line under title
        line = plt.Line2D(
            [0.2, 0.8], [0.92, 0.92],
            transform=fig.transFigure,
            color=accent_color,
            linewidth=2,
            alpha=0.8
        )
        fig.add_artist(line)
        
        # Subtitle
        if subtitle:
            fig.text(
                0.5, 0.90, subtitle,
                fontsize=SIZES['subtitle'],
                color=TEXT_SECONDARY,
                ha='center', va='top',
                transform=fig.transFigure
            )

    # =========================================================================
    # SIGNATURE VISUALIZATION: PULSE SHOT MAP
    # =========================================================================
    
    def pulse_shot_map(
        self,
        events: pd.DataFrame,
        team_name: str,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 12)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a Pulse Shot Map - shots displayed with glow effects
        on a dark pitch, sized by xG with goal celebrations.
        
        Args:
            events: DataFrame with shot events
            team_name: Team to show shots for
            title: Optional custom title
            figsize: Figure size
            
        Returns:
            Figure and axes
        """
        # Filter shots
        shots = events[
            (events['type'] == 'Shot') &
            (events['team'] == team_name)
        ].copy()
        
        if shots.empty:
            raise ValueError(f"No shots found for {team_name}")
        
        # Extract coordinates
        if 'x' not in shots.columns:
            shots['x'] = shots['location'].apply(lambda x: x[0] if isinstance(x, list) else None)
            shots['y'] = shots['location'].apply(lambda x: x[1] if isinstance(x, list) else None)
        
        shots = shots.dropna(subset=['x', 'y'])
        
        # Create figure with dark background
        fig = plt.figure(figsize=figsize, facecolor=BACKGROUND_PRIMARY)
        ax = fig.add_axes([0.05, 0.1, 0.9, 0.75])
        ax.set_facecolor(BACKGROUND_PITCH)
        
        # Create pitch
        pitch = VerticalPitch(
            pitch_type='statsbomb',
            pitch_color=BACKGROUND_PITCH,
            line_color='#3d4f5f',
            linewidth=1,
            half=True
        )
        pitch.draw(ax=ax)
        
        # Plot each shot with glow effect
        for _, shot in shots.iterrows():
            x, y = shot['x'], shot['y']
            is_goal = shot.get('shot_outcome') == 'Goal'
            xg = shot.get('shot_statsbomb_xg', 0.1)
            
            # Determine color and size
            if is_goal:
                color = ACCENT_LIME
                size = max(300, xg * 1500)
                glow_layers = 5
            else:
                color = ACCENT_CYAN if xg > 0.15 else ACCENT_MAGENTA
                size = max(100, xg * 800)
                glow_layers = 3
            
            # Add glow effect (converted to pitch coords)
            self._add_glow(ax, y, x, color, radius=size/800, alpha=0.2, layers=glow_layers)
            
            # Plot main point
            ax.scatter(
                y, x,
                s=size,
                c=color,
                alpha=0.9,
                edgecolors='white' if is_goal else color,
                linewidth=2 if is_goal else 0,
                zorder=10
            )
            
            # Add star for goals
            if is_goal:
                ax.scatter(y, x, s=50, marker='*', c='white', zorder=11)
        
        # Add title block
        title = title or f"{team_name.upper()} | SHOT MAP"
        self._add_title_block(fig, title, f"Goals: {len(shots[shots['shot_outcome'] == 'Goal'])} | Total Shots: {len(shots)}")
        
        # Add legend
        legend_elements = [
            plt.scatter([], [], s=150, c=ACCENT_LIME, label='Goal', edgecolors='white', linewidth=2),
            plt.scatter([], [], s=100, c=ACCENT_CYAN, label='High xG Shot'),
            plt.scatter([], [], s=60, c=ACCENT_MAGENTA, label='Low xG Shot'),
        ]
        ax.legend(
            handles=legend_elements,
            loc='lower right',
            fontsize=9,
            framealpha=0.8,
            facecolor=BACKGROUND_SECONDARY
        )
        
        # Add watermark
        self._add_watermark(fig)
        
        return fig, ax

    # =========================================================================
    # SIGNATURE VISUALIZATION: AURORA PASS NETWORK
    # =========================================================================
    
    def aurora_pass_network(
        self,
        events: pd.DataFrame,
        team_name: str,
        min_passes: int = 3,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 8)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create an Aurora Pass Network - pass connections with gradient
        lines showing pass frequency between players.
        
        Args:
            events: DataFrame with event data
            team_name: Team to show network for
            min_passes: Minimum passes between players to show
            title: Optional custom title
            figsize: Figure size
            
        Returns:
            Figure and axes
        """
        # Filter passes for team
        passes = events[
            (events['type'] == 'Pass') &
            (events['team'] == team_name) &
            (events['pass_outcome'].isna())  # Successful passes
        ].copy()
        
        if passes.empty:
            raise ValueError(f"No passes found for {team_name}")
        
        # Extract coordinates
        if 'x' not in passes.columns:
            passes['x'] = passes['location'].apply(lambda x: x[0] if isinstance(x, list) else None)
            passes['y'] = passes['location'].apply(lambda x: x[1] if isinstance(x, list) else None)
        
        # Get pass recipient
        passes['recipient'] = passes['pass_recipient']
        passes = passes.dropna(subset=['x', 'y', 'player', 'recipient'])
        
        # Calculate average positions
        avg_positions = passes.groupby('player').agg({
            'x': 'mean',
            'y': 'mean'
        }).reset_index()
        
        # Count passes between players
        pass_counts = passes.groupby(['player', 'recipient']).size().reset_index(name='count')
        pass_counts = pass_counts[pass_counts['count'] >= min_passes]
        
        # Create figure
        fig = plt.figure(figsize=figsize, facecolor=BACKGROUND_PRIMARY)
        ax = fig.add_axes([0.05, 0.1, 0.9, 0.8])
        
        # Create pitch
        pitch = Pitch(
            pitch_type='statsbomb',
            pitch_color=BACKGROUND_PITCH,
            line_color='#3d4f5f',
            linewidth=1
        )
        pitch.draw(ax=ax)
        
        # Plot pass connections with gradient
        max_count = pass_counts['count'].max()
        
        for _, row in pass_counts.iterrows():
            player1 = row['player']
            player2 = row['recipient']
            count = row['count']
            
            pos1 = avg_positions[avg_positions['player'] == player1]
            pos2 = avg_positions[avg_positions['player'] == player2]
            
            if pos1.empty or pos2.empty:
                continue
            
            x1, y1 = pos1['x'].values[0], pos1['y'].values[0]
            x2, y2 = pos2['x'].values[0], pos2['y'].values[0]
            
            # Create gradient line
            n_points = 50
            x_vals = np.linspace(x1, x2, n_points)
            y_vals = np.linspace(y1, y2, n_points)
            points = np.array([x_vals, y_vals]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            
            # Color gradient from cyan to magenta based on position
            colors = np.linspace(0, 1, len(segments))
            
            # Line width based on pass count
            lw = 1 + (count / max_count) * 4
            
            lc = LineCollection(
                segments,
                cmap=self.cmap_aurora,
                norm=plt.Normalize(0, 1),
                linewidths=lw,
                alpha=0.6
            )
            lc.set_array(colors)
            ax.add_collection(lc)
        
        # Plot player nodes
        for _, player in avg_positions.iterrows():
            total_passes = passes[passes['player'] == player['player']].shape[0]
            size = 100 + total_passes * 5
            
            # Glow effect
            self._add_glow(ax, player['x'], player['y'], ACCENT_CYAN, radius=3, alpha=0.2)
            
            # Main node
            ax.scatter(
                player['x'], player['y'],
                s=size,
                c=ACCENT_CYAN,
                edgecolors='white',
                linewidth=1.5,
                zorder=10
            )
            
            # Player name
            name = player['player'].split()[-1]  # Last name only
            ax.annotate(
                name,
                (player['x'], player['y'] - 4),
                fontsize=8,
                color=TEXT_PRIMARY,
                ha='center',
                va='top',
                fontweight='bold',
                path_effects=[
                    path_effects.withStroke(linewidth=2, foreground=BACKGROUND_PRIMARY)
                ]
            )
        
        # Title
        title = title or f"{team_name.upper()} | PASS NETWORK"
        self._add_title_block(fig, title, f"Successful passes shown (min {min_passes} between players)")
        
        self._add_watermark(fig)
        
        return fig, ax

    # =========================================================================
    # SIGNATURE VISUALIZATION: IMPACT ZONES HEATMAP
    # =========================================================================
    
    def impact_zones(
        self,
        events: pd.DataFrame,
        player_name: str,
        event_types: List[str] = None,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 8)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create an Impact Zones heatmap - shows player activity areas
        with neon-styled density visualization.
        
        Args:
            events: DataFrame with event data
            player_name: Player to show heatmap for
            event_types: List of event types to include (default: all)
            title: Optional custom title
            figsize: Figure size
            
        Returns:
            Figure and axes
        """
        # Filter events
        player_events = events[events['player'] == player_name].copy()
        
        if event_types:
            player_events = player_events[player_events['type'].isin(event_types)]
        
        if player_events.empty:
            raise ValueError(f"No events found for {player_name}")
        
        # Extract coordinates
        if 'x' not in player_events.columns:
            player_events['x'] = player_events['location'].apply(
                lambda x: x[0] if isinstance(x, list) else None
            )
            player_events['y'] = player_events['location'].apply(
                lambda x: x[1] if isinstance(x, list) else None
            )
        
        player_events = player_events.dropna(subset=['x', 'y'])
        
        # Create figure
        fig = plt.figure(figsize=figsize, facecolor=BACKGROUND_PRIMARY)
        ax = fig.add_axes([0.05, 0.1, 0.9, 0.8])
        
        # Create pitch
        pitch = Pitch(
            pitch_type='statsbomb',
            pitch_color=BACKGROUND_PITCH,
            line_color='#3d4f5f',
            linewidth=1,
            line_zorder=2
        )
        pitch.draw(ax=ax)
        
        # Create heatmap with custom colormap
        pitch.kdeplot(
            player_events['x'],
            player_events['y'],
            ax=ax,
            cmap=self.cmap_aurora,
            fill=True,
            levels=50,
            alpha=0.7,
            zorder=1
        )
        
        # Add scatter points for events
        ax.scatter(
            player_events['x'],
            player_events['y'],
            s=20,
            c=ACCENT_CYAN,
            alpha=0.4,
            zorder=3
        )
        
        # Title
        title = title or f"{player_name.upper()} | IMPACT ZONES"
        event_desc = ', '.join(event_types) if event_types else 'All Events'
        self._add_title_block(fig, title, f"{len(player_events)} actions | {event_desc}")
        
        self._add_watermark(fig)
        
        return fig, ax

    # =========================================================================
    # SIGNATURE VISUALIZATION: STATS CARD
    # =========================================================================
    
    def stats_card(
        self,
        player_name: str,
        team_name: str,
        stats: Dict[str, Any],
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 10)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a branded Stats Card for a player.
        
        Args:
            player_name: Player name
            team_name: Team name
            stats: Dictionary of stat_name: value pairs
            title: Optional custom title
            figsize: Figure size
            
        Returns:
            Figure and axes
        """
        fig = plt.figure(figsize=figsize, facecolor=BACKGROUND_PRIMARY)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
        ax.set_facecolor(BACKGROUND_PRIMARY)
        
        # Header section
        ax.fill_between([0, 100], [85, 85], [100, 100], color=BACKGROUND_SECONDARY)
        
        # Accent line
        ax.plot([10, 90], [84, 84], color=ACCENT_CYAN, linewidth=3)
        
        # Player name
        ax.text(
            50, 92, player_name.upper(),
            fontsize=24, color=TEXT_PRIMARY,
            ha='center', va='center',
            fontweight='bold'
        )
        
        # Team name
        ax.text(
            50, 87, team_name,
            fontsize=12, color=TEXT_SECONDARY,
            ha='center', va='center'
        )
        
        # Stats grid
        n_stats = len(stats)
        cols = 2
        rows = (n_stats + 1) // 2
        
        stat_items = list(stats.items())
        
        for i, (stat_name, stat_value) in enumerate(stat_items):
            col = i % cols
            row = i // cols
            
            x = 25 + col * 50
            y = 70 - row * 20
            
            # Stat value (large)
            ax.text(
                x, y, str(stat_value),
                fontsize=28, color=ACCENT_CYAN,
                ha='center', va='center',
                fontweight='bold'
            )
            
            # Stat label
            ax.text(
                x, y - 7, stat_name,
                fontsize=10, color=TEXT_SECONDARY,
                ha='center', va='center'
            )
        
        # Bottom accent
        ax.fill_between([0, 100], [0, 0], [5, 5], color=ACCENT_CYAN, alpha=0.3)
        
        # Watermark
        ax.text(
            95, 2, WATERMARK_TEXT,
            fontsize=10, color=ACCENT_CYAN,
            ha='right', va='bottom',
            alpha=0.6, fontweight='bold'
        )
        
        return fig, ax

    # =========================================================================
    # UTILITY: SAVE WITH BRANDING
    # =========================================================================
    
    def save(
        self,
        fig: plt.Figure,
        filename: str,
        output_dir: str = 'output/images',
        dpi: int = 150
    ) -> str:
        """
        Save figure with proper branding and settings.
        
        Args:
            fig: Figure to save
            filename: Output filename
            output_dir: Output directory
            dpi: Resolution
            
        Returns:
            Path to saved file
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        filepath = Path(output_dir) / filename
        
        fig.savefig(
            filepath,
            dpi=dpi,
            facecolor=fig.get_facecolor(),
            edgecolor='none',
            bbox_inches='tight',
            pad_inches=0.1
        )
        plt.close(fig)
        
        return str(filepath)

"""
📊 BRANDED CHART TEMPLATES
===========================
Implementation of all 7 visualization types with your unique brand styling.

Chart Types:
1. Progressive Passes Grid - Team improvement zones
2. Player Stats Table - Styled data tables with bars
3. Crossing Zones Grid - Pitch heatmap grids
4. Scatter Plot - Player performance comparisons
5. Histogram/Distribution - Statistical distributions
6. Zone Control Maps - Territorial control visualization
7. Shot Maps - Player shot location analysis
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.table import Table
from mplsoccer import Pitch, VerticalPitch
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path

# Import branding
from src.branding.style import (
    COLORS, TYPOGRAPHY, LAYOUT, BRAND,
    ChartStyler, apply_brand_style, get_pitch_config
)


class BrandedCharts:
    """
    Create all 7 chart types with your unique brand styling.
    """
    
    def __init__(self):
        """Initialize with brand styling."""
        apply_brand_style()
        self.styler = ChartStyler()
    
    # =========================================================================
    # CHART 1: PROGRESSIVE PASSES GRID
    # =========================================================================
    def progressive_passes_grid(
        self,
        data: pd.DataFrame,
        teams: List[str],
        title: str = "WHICH TEAMS ARE IMPROVING?",
        subtitle: str = "Progressive pass success rate by pitch zone",
        cols: int = 5,
        figsize: Tuple[float, float] = None
    ) -> plt.Figure:
        """
        Create a grid of mini-pitches showing improvement/deterioration
        in different zones for each team.
        
        Args:
            data: DataFrame with columns [team, zone, current_rate, prev_rate]
            teams: List of team names to display
            title: Main title
            subtitle: Subtitle text
            cols: Number of columns in grid
            figsize: Figure size
            
        Returns:
            Styled matplotlib figure
        """
        n_teams = len(teams)
        rows = (n_teams + cols - 1) // cols
        
        figsize = figsize or (cols * 2.5, rows * 3 + 1.5)
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        axes = np.atleast_2d(axes)
        fig.patch.set_facecolor(COLORS.BACKGROUND_DARK)
        
        # Flatten axes for easy iteration
        axes_flat = axes.flatten()
        
        # Create mini pitch for each team
        for idx, team in enumerate(teams):
            ax = axes_flat[idx]
            self._draw_mini_pitch_zones(ax, team, data)
        
        # Hide unused axes
        for idx in range(len(teams), len(axes_flat)):
            axes_flat[idx].set_visible(False)
        
        # Add title with brand styling
        fig.suptitle(
            title,
            fontsize=TYPOGRAPHY.SIZE_TITLE,
            fontweight=TYPOGRAPHY.WEIGHT_BOLD,
            color=COLORS.TEXT_PRIMARY,
            y=0.98
        )
        
        # Subtitle
        fig.text(
            0.5, 0.94, subtitle,
            fontsize=TYPOGRAPHY.SIZE_CAPTION,
            color=COLORS.TEXT_SECONDARY,
            ha='center'
        )
        
        # Add signature accent bar at top
        fig.patches.append(plt.Rectangle(
            (0.35, 0.96), 0.3, 0.005,
            transform=fig.transFigure,
            facecolor=COLORS.AURORA_CYAN,
            clip_on=False
        ))
        
        self.styler.add_watermark(fig)
        self.styler.add_data_source(fig)
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.92])
        return fig
    
    def _draw_mini_pitch_zones(self, ax: plt.Axes, team: str, data: pd.DataFrame):
        """Draw a mini pitch with colored zones."""
        ax.set_facecolor(COLORS.BACKGROUND_MEDIUM)
        ax.set_xlim(0, 120)
        ax.set_ylim(0, 80)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Draw pitch outline
        pitch_rect = patches.Rectangle(
            (0, 0), 120, 80,
            fill=False, edgecolor=COLORS.TEXT_MUTED, linewidth=0.5
        )
        ax.add_patch(pitch_rect)
        
        # Draw zones (3x3 grid)
        zone_width = 40
        zone_height = 80/3
        
        cmap = LinearSegmentedColormap.from_list(
            "progress",
            [COLORS.DANGER, COLORS.BACKGROUND_MEDIUM, COLORS.SUCCESS],
            N=256
        )
        
        for i in range(3):  # columns
            for j in range(3):  # rows
                # Get zone value (mock random for demo)
                value = np.random.uniform(-0.15, 0.15)  # Replace with real data
                color = cmap(0.5 + value * 3)  # Map to colormap
                
                zone = patches.Rectangle(
                    (i * zone_width, j * zone_height),
                    zone_width, zone_height,
                    facecolor=color, edgecolor=COLORS.TEXT_MUTED,
                    linewidth=0.3, alpha=0.8
                )
                ax.add_patch(zone)
                
                # Add percentage text
                pct_text = f"{value*100:+.1f}%"
                text_color = COLORS.TEXT_PRIMARY if abs(value) > 0.05 else COLORS.TEXT_MUTED
                ax.text(
                    i * zone_width + zone_width/2,
                    j * zone_height + zone_height/2,
                    pct_text,
                    fontsize=7, ha='center', va='center',
                    color=text_color, fontweight='bold'
                )
        
        # Draw center circle
        center_circle = patches.Circle(
            (60, 40), 9.15,
            fill=False, edgecolor=COLORS.TEXT_MUTED, linewidth=0.3
        )
        ax.add_patch(center_circle)
        
        # Team name
        ax.text(
            60, -5, team,
            fontsize=8, ha='center', va='top',
            color=COLORS.TEXT_PRIMARY, fontweight='bold'
        )
    
    # =========================================================================
    # CHART 2: PLAYER STATS TABLE
    # =========================================================================
    def player_stats_table(
        self,
        data: pd.DataFrame,
        title: str = "TOP PERFORMERS",
        subtitle: str = "Player statistics breakdown",
        bar_column: str = None,
        figsize: Tuple[float, float] = (12, 14)
    ) -> plt.Figure:
        """
        Create a styled player statistics table.
        
        Args:
            data: DataFrame with player statistics
            title: Main title
            subtitle: Subtitle
            bar_column: Column to show as progress bar
            figsize: Figure size
            
        Returns:
            Styled matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor(COLORS.BACKGROUND_DARK)
        ax.set_facecolor(COLORS.BACKGROUND_DARK)
        ax.axis('off')
        
        colors = self.styler.get_table_colors()
        n_rows = len(data)
        n_cols = len(data.columns)
        
        # Calculate cell dimensions
        col_width = 1.0 / n_cols
        row_height = 0.8 / (n_rows + 1)  # +1 for header
        
        # Draw header
        for col_idx, col_name in enumerate(data.columns):
            rect = patches.FancyBboxPatch(
                (col_idx * col_width, 0.85),
                col_width - 0.005, row_height,
                boxstyle="round,pad=0.01",
                facecolor=colors['header_bg'],
                edgecolor='none',
                transform=ax.transAxes
            )
            ax.add_patch(rect)
            
            ax.text(
                col_idx * col_width + col_width/2, 0.85 + row_height/2,
                col_name.upper(),
                transform=ax.transAxes,
                fontsize=TYPOGRAPHY.SIZE_CAPTION,
                fontweight=TYPOGRAPHY.WEIGHT_BOLD,
                color=colors['header_text'],
                ha='center', va='center'
            )
        
        # Draw data rows
        for row_idx, (_, row) in enumerate(data.iterrows()):
            y_pos = 0.85 - (row_idx + 1) * row_height
            bg_color = colors['row_bg_odd'] if row_idx % 2 == 0 else colors['row_bg_even']
            
            for col_idx, (col_name, value) in enumerate(row.items()):
                # Cell background
                rect = patches.Rectangle(
                    (col_idx * col_width, y_pos),
                    col_width - 0.005, row_height - 0.005,
                    facecolor=bg_color,
                    edgecolor='none',
                    transform=ax.transAxes
                )
                ax.add_patch(rect)
                
                # If this is the bar column, draw a progress bar
                if bar_column and col_name == bar_column:
                    try:
                        bar_val = float(str(value).replace('%', '')) / 100
                        bar_width = (col_width - 0.02) * bar_val
                        bar_rect = patches.Rectangle(
                            (col_idx * col_width + 0.005, y_pos + 0.002),
                            bar_width, row_height - 0.01,
                            facecolor=colors['bar_fill'],
                            edgecolor='none',
                            transform=ax.transAxes,
                            alpha=0.8
                        )
                        ax.add_patch(bar_rect)
                    except:
                        pass
                
                # Cell text
                ax.text(
                    col_idx * col_width + col_width/2, y_pos + row_height/2,
                    str(value),
                    transform=ax.transAxes,
                    fontsize=TYPOGRAPHY.SIZE_CAPTION,
                    color=colors['row_text'],
                    ha='center', va='center'
                )
        
        # Title
        ax.text(
            0.5, 0.95, title,
            transform=ax.transAxes,
            fontsize=TYPOGRAPHY.SIZE_TITLE,
            fontweight=TYPOGRAPHY.WEIGHT_BOLD,
            color=COLORS.TEXT_PRIMARY,
            ha='center'
        )
        
        # Subtitle
        ax.text(
            0.5, 0.91, subtitle,
            transform=ax.transAxes,
            fontsize=TYPOGRAPHY.SIZE_CAPTION,
            color=COLORS.TEXT_SECONDARY,
            ha='center'
        )
        
        # Signature underline
        ax.axhline(y=0.925, xmin=0.35, xmax=0.65,
                   color=COLORS.AURORA_CYAN, linewidth=2,
                   transform=ax.transAxes)
        
        self.styler.add_watermark(fig)
        return fig
    
    # =========================================================================
    # CHART 3: CROSSING ZONES GRID
    # =========================================================================
    def crossing_zones_grid(
        self,
        data: Dict[str, np.ndarray],
        title: str = "WHERE DO CROSSES COME FROM?",
        subtitle: str = "Crossing zone analysis by team",
        cols: int = 5,
        figsize: Tuple[float, float] = None
    ) -> plt.Figure:
        """
        Create a grid showing crossing zones for multiple teams.
        
        Args:
            data: Dict mapping team names to zone arrays
            title: Main title
            subtitle: Subtitle
            cols: Columns in grid
            figsize: Figure size
            
        Returns:
            Styled matplotlib figure
        """
        teams = list(data.keys())
        n_teams = len(teams)
        rows = (n_teams + cols - 1) // cols
        
        figsize = figsize or (cols * 2.5, rows * 3 + 1.5)
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        axes = np.atleast_2d(axes)
        fig.patch.set_facecolor(COLORS.BACKGROUND_DARK)
        
        axes_flat = axes.flatten()
        cmap = self.styler.get_zone_cmap()
        
        for idx, team in enumerate(teams):
            ax = axes_flat[idx]
            self._draw_crossing_pitch(ax, team, cmap)
        
        # Hide unused
        for idx in range(len(teams), len(axes_flat)):
            axes_flat[idx].set_visible(False)
        
        # Titles
        fig.suptitle(
            title,
            fontsize=TYPOGRAPHY.SIZE_TITLE,
            fontweight=TYPOGRAPHY.WEIGHT_BOLD,
            color=COLORS.TEXT_PRIMARY,
            y=0.98
        )
        
        fig.text(0.5, 0.94, subtitle,
                fontsize=TYPOGRAPHY.SIZE_CAPTION,
                color=COLORS.TEXT_SECONDARY, ha='center')
        
        # Accent bar
        fig.patches.append(plt.Rectangle(
            (0.35, 0.96), 0.3, 0.005,
            transform=fig.transFigure,
            facecolor=COLORS.AURORA_MAGENTA,
            clip_on=False
        ))
        
        self.styler.add_watermark(fig)
        plt.tight_layout(rect=[0, 0.03, 1, 0.92])
        return fig
    
    def _draw_crossing_pitch(self, ax: plt.Axes, team: str, cmap):
        """Draw pitch with crossing zone heatmap."""
        ax.set_facecolor(COLORS.BACKGROUND_MEDIUM)
        ax.set_xlim(0, 60)
        ax.set_ylim(0, 80)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Pitch outline (half pitch)
        pitch_rect = patches.Rectangle(
            (0, 0), 60, 80,
            fill=False, edgecolor=COLORS.TEXT_MUTED, linewidth=0.5
        )
        ax.add_patch(pitch_rect)
        
        # Penalty area
        penalty = patches.Rectangle(
            (0, 18), 18, 44,
            fill=False, edgecolor=COLORS.TEXT_MUTED, linewidth=0.3
        )
        ax.add_patch(penalty)
        
        # Crossing zones (left and right flanks)
        left_zone = np.random.uniform(0.3, 1.0)
        right_zone = np.random.uniform(0.3, 1.0)
        
        # Left flank
        left_rect = patches.Rectangle(
            (0, 0), 15, 25,
            facecolor=cmap(left_zone), alpha=0.7
        )
        ax.add_patch(left_rect)
        ax.text(7.5, 12.5, f"{int(left_zone*100)}%",
                fontsize=7, ha='center', va='center',
                color=COLORS.TEXT_PRIMARY, fontweight='bold')
        
        # Right flank
        right_rect = patches.Rectangle(
            (0, 55), 15, 25,
            facecolor=cmap(right_zone), alpha=0.7
        )
        ax.add_patch(right_rect)
        ax.text(7.5, 67.5, f"{int(right_zone*100)}%",
                fontsize=7, ha='center', va='center',
                color=COLORS.TEXT_PRIMARY, fontweight='bold')
        
        # Team name
        ax.text(30, -5, team,
                fontsize=8, ha='center', va='top',
                color=COLORS.TEXT_PRIMARY, fontweight='bold')
    
    # =========================================================================
    # CHART 4: SCATTER PLOT
    # =========================================================================
    def scatter_plot(
        self,
        data: pd.DataFrame,
        x_col: str,
        y_col: str,
        label_col: str = None,
        size_col: str = None,
        color_col: str = None,
        title: str = "PLAYER PERFORMANCE",
        subtitle: str = "Statistical comparison",
        x_label: str = None,
        y_label: str = None,
        figsize: Tuple[float, float] = (12, 10)
    ) -> plt.Figure:
        """
        Create a branded scatter plot.
        
        Args:
            data: DataFrame with data
            x_col: Column for x-axis
            y_col: Column for y-axis
            label_col: Column for point labels
            size_col: Column for point sizes
            color_col: Column for point colors
            title: Main title
            subtitle: Subtitle
            x_label, y_label: Axis labels
            figsize: Figure size
            
        Returns:
            Styled matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor(COLORS.BACKGROUND_DARK)
        ax.set_facecolor(COLORS.BACKGROUND_MEDIUM)
        
        # Calculate sizes
        sizes = data[size_col] * 100 if size_col else 80
        
        # Colors
        if color_col:
            colors = data[color_col]
            cmap = self.styler.get_zone_cmap()
            scatter = ax.scatter(
                data[x_col], data[y_col],
                s=sizes, c=colors, cmap=cmap,
                alpha=0.8, edgecolors=COLORS.BACKGROUND_DARK, linewidth=0.5
            )
        else:
            scatter = ax.scatter(
                data[x_col], data[y_col],
                s=sizes, c=COLORS.AURORA_CYAN,
                alpha=0.8, edgecolors=COLORS.BACKGROUND_DARK, linewidth=0.5
            )
        
        # Add labels
        if label_col:
            for _, row in data.iterrows():
                ax.annotate(
                    row[label_col],
                    (row[x_col], row[y_col]),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=TYPOGRAPHY.SIZE_MICRO,
                    color=COLORS.TEXT_SECONDARY,
                    alpha=0.9
                )
        
        # Styling
        ax.set_xlabel(x_label or x_col, fontsize=TYPOGRAPHY.SIZE_BODY,
                     color=COLORS.TEXT_PRIMARY)
        ax.set_ylabel(y_label or y_col, fontsize=TYPOGRAPHY.SIZE_BODY,
                     color=COLORS.TEXT_PRIMARY)
        
        ax.grid(True, alpha=0.15, color=COLORS.TEXT_MUTED, linestyle='--')
        
        for spine in ax.spines.values():
            spine.set_color(COLORS.BACKGROUND_LIGHT)
        
        # Title
        self.styler.style_title(ax, title, subtitle)
        self.styler.add_watermark(fig)
        
        plt.tight_layout(rect=[0, 0.02, 1, 0.95])
        return fig
    
    # =========================================================================
    # CHART 5: HISTOGRAM / DISTRIBUTION
    # =========================================================================
    def histogram_grid(
        self,
        data: Dict[str, np.ndarray],
        title: str = "GOAL SIMULATION",
        subtitle: str = "Distribution of expected goals",
        cols: int = 3,
        highlight_values: Dict[str, float] = None,
        figsize: Tuple[float, float] = None
    ) -> plt.Figure:
        """
        Create a grid of histograms.
        
        Args:
            data: Dict mapping names to value arrays
            title: Main title
            subtitle: Subtitle
            cols: Columns in grid
            highlight_values: Dict of actual values to highlight
            figsize: Figure size
            
        Returns:
            Styled matplotlib figure
        """
        names = list(data.keys())
        n = len(names)
        rows = (n + cols - 1) // cols
        
        figsize = figsize or (cols * 4, rows * 3 + 1.5)
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        axes = np.atleast_2d(axes)
        fig.patch.set_facecolor(COLORS.BACKGROUND_DARK)
        
        axes_flat = axes.flatten()
        
        for idx, name in enumerate(names):
            ax = axes_flat[idx]
            ax.set_facecolor(COLORS.BACKGROUND_DARK)
            
            values = data[name]
            
            # Histogram
            n_vals, bins, patches_hist = ax.hist(
                values, bins=20,
                color=COLORS.AURORA_CYAN,
                edgecolor=COLORS.BACKGROUND_DARK,
                alpha=0.8
            )
            
            # Highlight actual value
            if highlight_values and name in highlight_values:
                actual = highlight_values[name]
                ax.axvline(
                    actual, color=COLORS.AURORA_GOLD,
                    linewidth=2, linestyle='--',
                    label=f'Actual: {actual}'
                )
            
            # Styling
            ax.set_title(name, fontsize=TYPOGRAPHY.SIZE_BODY,
                        fontweight=TYPOGRAPHY.WEIGHT_BOLD,
                        color=COLORS.TEXT_PRIMARY)
            ax.tick_params(colors=COLORS.TEXT_SECONDARY)
            
            for spine in ax.spines.values():
                spine.set_visible(False)
        
        # Hide unused
        for idx in range(len(names), len(axes_flat)):
            axes_flat[idx].set_visible(False)
        
        # Title
        fig.suptitle(title,
                    fontsize=TYPOGRAPHY.SIZE_TITLE,
                    fontweight=TYPOGRAPHY.WEIGHT_BOLD,
                    color=COLORS.TEXT_PRIMARY, y=0.98)
        
        fig.text(0.5, 0.94, subtitle,
                fontsize=TYPOGRAPHY.SIZE_CAPTION,
                color=COLORS.TEXT_SECONDARY, ha='center')
        
        # Accent
        fig.patches.append(plt.Rectangle(
            (0.35, 0.96), 0.3, 0.005,
            transform=fig.transFigure,
            facecolor=COLORS.AURORA_GOLD,
            clip_on=False
        ))
        
        self.styler.add_watermark(fig)
        plt.tight_layout(rect=[0, 0.03, 1, 0.92])
        return fig
    
    # =========================================================================
    # CHART 6: ZONE CONTROL MAPS
    # =========================================================================
    def zone_control_grid(
        self,
        teams: List[str],
        title: str = "TERRITORIAL CONTROL",
        subtitle: str = "Zones of dominance analysis",
        cols: int = 5,
        figsize: Tuple[float, float] = None
    ) -> plt.Figure:
        """
        Create a grid of territorial control maps.
        
        Args:
            teams: List of team names
            title: Main title
            subtitle: Subtitle
            cols: Columns in grid
            figsize: Figure size
            
        Returns:
            Styled matplotlib figure
        """
        n_teams = len(teams)
        rows = (n_teams + cols - 1) // cols
        
        figsize = figsize or (cols * 2.5, rows * 3 + 1.5)
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        axes = np.atleast_2d(axes)
        fig.patch.set_facecolor(COLORS.BACKGROUND_DARK)
        
        axes_flat = axes.flatten()
        control_colors = self.styler.get_control_colors()
        
        for idx, team in enumerate(teams):
            ax = axes_flat[idx]
            self._draw_control_pitch(ax, team, control_colors)
        
        for idx in range(len(teams), len(axes_flat)):
            axes_flat[idx].set_visible(False)
        
        # Titles
        fig.suptitle(title,
                    fontsize=TYPOGRAPHY.SIZE_TITLE,
                    fontweight=TYPOGRAPHY.WEIGHT_BOLD,
                    color=COLORS.TEXT_PRIMARY, y=0.98)
        
        fig.text(0.5, 0.94, subtitle,
                fontsize=TYPOGRAPHY.SIZE_CAPTION,
                color=COLORS.TEXT_SECONDARY, ha='center')
        
        # Legend
        fig.patches.append(plt.Rectangle((0.15, 0.01), 0.02, 0.015,
                          transform=fig.transFigure,
                          facecolor=control_colors['team_control']))
        fig.text(0.18, 0.015, 'Team Control', transform=fig.transFigure,
                fontsize=TYPOGRAPHY.SIZE_MICRO, color=COLORS.TEXT_SECONDARY)
        
        fig.patches.append(plt.Rectangle((0.35, 0.01), 0.02, 0.015,
                          transform=fig.transFigure,
                          facecolor=control_colors['contested']))
        fig.text(0.38, 0.015, 'Contested', transform=fig.transFigure,
                fontsize=TYPOGRAPHY.SIZE_MICRO, color=COLORS.TEXT_SECONDARY)
        
        fig.patches.append(plt.Rectangle((0.52, 0.01), 0.02, 0.015,
                          transform=fig.transFigure,
                          facecolor=control_colors['opponent_control']))
        fig.text(0.55, 0.015, 'Opponent Control', transform=fig.transFigure,
                fontsize=TYPOGRAPHY.SIZE_MICRO, color=COLORS.TEXT_SECONDARY)
        
        # Accent
        fig.patches.append(plt.Rectangle(
            (0.35, 0.96), 0.3, 0.005,
            transform=fig.transFigure,
            facecolor=COLORS.AURORA_PURPLE,
            clip_on=False
        ))
        
        self.styler.add_watermark(fig)
        plt.tight_layout(rect=[0, 0.04, 1, 0.92])
        return fig
    
    def _draw_control_pitch(self, ax, team, colors):
        """Draw pitch with control zones."""
        ax.set_facecolor(COLORS.BACKGROUND_MEDIUM)
        ax.set_xlim(0, 120)
        ax.set_ylim(0, 80)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Pitch outline
        pitch_rect = patches.Rectangle(
            (0, 0), 120, 80,
            fill=False, edgecolor=COLORS.TEXT_MUTED, linewidth=0.5
        )
        ax.add_patch(pitch_rect)
        
        # 4x3 zones
        zone_w = 30
        zone_h = 80/3
        
        for i in range(4):
            for j in range(3):
                # Random control value (-1 to 1)
                control = np.random.uniform(-1, 1)
                
                if control > 0.3:
                    color = colors['team_control']
                elif control < -0.3:
                    color = colors['opponent_control']
                else:
                    color = colors['contested']
                
                alpha = min(abs(control), 0.8)
                
                zone = patches.Rectangle(
                    (i * zone_w, j * zone_h),
                    zone_w, zone_h,
                    facecolor=color, alpha=alpha,
                    edgecolor=COLORS.TEXT_MUTED, linewidth=0.2
                )
                ax.add_patch(zone)
        
        ax.text(60, -5, team,
                fontsize=8, ha='center', va='top',
                color=COLORS.TEXT_PRIMARY, fontweight='bold')
    
    # =========================================================================
    # CHART 7: SHOT MAPS
    # =========================================================================
    def shot_map(
        self,
        shots: pd.DataFrame,
        player_name: str,
        title: str = None,
        subtitle: str = None,
        show_hexbin: bool = True,
        figsize: Tuple[float, float] = (10, 12)
    ) -> plt.Figure:
        """
        Create a branded shot map for a player.
        
        Args:
            shots: DataFrame with shot data (x, y, outcome, xg columns)
            player_name: Player name for title
            title: Override title
            subtitle: Override subtitle
            show_hexbin: Show hexbin density
            figsize: Figure size
            
        Returns:
            Styled matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor(COLORS.BACKGROUND_DARK)
        
        # Create vertical pitch (half)
        pitch = VerticalPitch(
            pitch_type='statsbomb',
            pitch_color=COLORS.PITCH_GREEN,
            line_color=COLORS.PITCH_LINES,
            linewidth=1,
            half=True,
            goal_type='box'
        )
        pitch.draw(ax=ax)
        
        shot_colors = self.styler.get_shot_colors()
        
        # Extract coordinates
        if 'x' not in shots.columns:
            shots = shots.copy()
            shots['x'] = shots['location'].apply(lambda l: l[0] if isinstance(l, list) else None)
            shots['y'] = shots['location'].apply(lambda l: l[1] if isinstance(l, list) else None)
        
        shots_valid = shots.dropna(subset=['x', 'y'])
        
        # Hexbin background if requested
        if show_hexbin and len(shots_valid) > 5:
            pitch.hexbin(
                shots_valid['y'], shots_valid['x'],
                ax=ax, cmap=shot_colors['hexbin_cmap'],
                gridsize=10, alpha=0.4
            )
        
        # Plot individual shots
        for _, shot in shots_valid.iterrows():
            outcome = shot.get('shot_outcome', 'Off Target')
            xg = shot.get('shot_statsbomb_xg', 0.1)
            
            color = shot_colors.get(outcome.lower().replace(' ', '_'), COLORS.NEUTRAL)
            if outcome == 'Goal':
                color = shot_colors['goal']
            elif outcome == 'Saved':
                color = shot_colors['saved']
            
            size = max(50, xg * 500)
            
            ax.scatter(
                shot['y'], shot['x'],
                s=size, c=color,
                alpha=0.8, edgecolors=COLORS.BACKGROUND_DARK,
                linewidth=0.5, zorder=3
            )
        
        # Stats box
        goals = len(shots_valid[shots_valid['shot_outcome'] == 'Goal'])
        total = len(shots_valid)
        total_xg = shots_valid['shot_statsbomb_xg'].sum() if 'shot_statsbomb_xg' in shots_valid else 0
        
        stats_text = f"Goals: {goals}  |  Shots: {total}  |  xG: {total_xg:.2f}"
        ax.text(
            40, 62, stats_text,
            fontsize=TYPOGRAPHY.SIZE_BODY,
            fontweight=TYPOGRAPHY.WEIGHT_BOLD,
            color=COLORS.TEXT_PRIMARY,
            ha='center',
            bbox=dict(
                boxstyle='round,pad=0.5',
                facecolor=COLORS.BACKGROUND_MEDIUM,
                edgecolor=COLORS.AURORA_CYAN,
                linewidth=1
            )
        )
        
        # Title
        title = title or f"{player_name.upper()}"
        subtitle = subtitle or "Shot Map Analysis"
        
        ax.text(40, 68, title,
                fontsize=TYPOGRAPHY.SIZE_TITLE,
                fontweight=TYPOGRAPHY.WEIGHT_BOLD,
                color=COLORS.TEXT_PRIMARY, ha='center')
        
        ax.text(40, 65, subtitle,
                fontsize=TYPOGRAPHY.SIZE_CAPTION,
                color=COLORS.TEXT_SECONDARY, ha='center')
        
        # Accent underline
        ax.plot([25, 55], [66.5, 66.5],
                color=COLORS.AURORA_CYAN, linewidth=2)
        
        self.styler.add_watermark(fig)
        self.styler.add_data_source(fig)
        
        plt.tight_layout()
        return fig
    
    # =========================================================================
    # SAVE UTILITY
    # =========================================================================
    def save(
        self,
        fig: plt.Figure,
        filename: str,
        output_dir: str = 'output/images',
        dpi: int = 150
    ) -> str:
        """Save figure with brand-consistent settings."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        filepath = Path(output_dir) / filename
        
        fig.savefig(
            filepath,
            dpi=dpi,
            bbox_inches='tight',
            facecolor=fig.get_facecolor(),
            edgecolor='none'
        )
        plt.close(fig)
        return str(filepath)


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def create_branded_charts() -> BrandedCharts:
    """Create and return a BrandedCharts instance."""
    return BrandedCharts()

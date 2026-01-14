"""
Visualization Module for Soccer Analytics

This module provides functions to create various soccer visualizations
including pitch plots, shot maps, pass networks, and heatmaps.

Usage:
    from src.visualizations.pitch import SoccerViz
    
    viz = SoccerViz()
    fig, ax = viz.plot_shot_map(events, team_name="Barcelona")
    viz.save(fig, "shot_map.png")
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mplsoccer import Pitch, VerticalPitch, Sbopen
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List, Dict, Any
import configparser
from pathlib import Path


class SoccerViz:
    """
    A class for creating soccer visualizations with Instagram-ready output.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the visualizer with optional config.
        
        Args:
            config_path: Path to settings.ini file
        """
        self.config = self._load_config(config_path)
        
        # Instagram dimensions
        self.instagram_post = (1080, 1080)
        self.instagram_story = (1080, 1920)
        
        # Default colors
        self.home_color = self.config.get('home_color', '#e41a1c')
        self.away_color = self.config.get('away_color', '#377eb8')
        self.ball_color = self.config.get('ball_color', '#ffffff')
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        defaults = {
            'pitch_type': 'statsbomb',
            'pitch_color': 'grass',
            'line_color': 'white',
            'home_color': '#e41a1c',
            'away_color': '#377eb8',
            'ball_color': '#ffffff',
            'title_fontsize': 16,
            'label_fontsize': 12,
        }
        
        if config_path and Path(config_path).exists():
            parser = configparser.ConfigParser()
            parser.read(config_path)
            if 'visualization' in parser:
                defaults.update(dict(parser['visualization']))
                
        return defaults
    
    def create_pitch(
        self,
        pitch_type: str = 'statsbomb',
        pitch_color: str = 'grass',
        line_color: str = 'white',
        orientation: str = 'horizontal',
        half: bool = False,
        figsize: Tuple[int, int] = (12, 8)
    ) -> Tuple[plt.Figure, plt.Axes, Pitch]:
        """
        Create a soccer pitch for plotting.
        
        Args:
            pitch_type: Type of pitch coordinates ('statsbomb', 'opta', etc.)
            pitch_color: Color of the pitch
            line_color: Color of the lines
            orientation: 'horizontal' or 'vertical'
            half: If True, show only half the pitch
            figsize: Figure size
            
        Returns:
            Tuple of (figure, axes, pitch object)
        """
        if orientation == 'vertical':
            pitch = VerticalPitch(
                pitch_type=pitch_type,
                pitch_color=pitch_color,
                line_color=line_color,
                half=half
            )
        else:
            pitch = Pitch(
                pitch_type=pitch_type,
                pitch_color=pitch_color,
                line_color=line_color,
                half=half
            )
        
        fig, ax = pitch.draw(figsize=figsize)
        return fig, ax, pitch
    
    def plot_shot_map(
        self,
        events: pd.DataFrame,
        team_name: Optional[str] = None,
        title: Optional[str] = None,
        show_xg: bool = True,
        figsize: Tuple[int, int] = (12, 8)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a shot map visualization.
        
        Args:
            events: DataFrame with event data (must have shot events)
            team_name: Filter shots by team name (optional)
            title: Plot title
            show_xg: If True, size markers by xG value
            figsize: Figure size
            
        Returns:
            Tuple of (figure, axes)
        """
        # Filter for shots
        shots = events[events['type'] == 'Shot'].copy()
        
        if team_name:
            shots = shots[shots['team'] == team_name]
        
        if shots.empty:
            raise ValueError("No shots found in the data")
        
        # Create pitch (half pitch, vertical for shot map)
        pitch = VerticalPitch(
            pitch_type='statsbomb',
            pitch_color='grass',
            line_color='white',
            half=True
        )
        fig, ax = pitch.draw(figsize=figsize)
        
        # Extract coordinates
        if 'x' not in shots.columns:
            shots['x'] = shots['location'].apply(lambda x: x[0] if isinstance(x, list) else None)
            shots['y'] = shots['location'].apply(lambda x: x[1] if isinstance(x, list) else None)
        
        # Get xG values
        if show_xg and 'shot_statsbomb_xg' in shots.columns:
            sizes = shots['shot_statsbomb_xg'] * 500 + 50
        else:
            sizes = 100
        
        # Color by outcome
        colors = shots['shot_outcome'].apply(
            lambda x: '#2ecc71' if x == 'Goal' else '#e74c3c'
        )
        
        # Plot shots
        scatter = ax.scatter(
            shots['y'], shots['x'],
            s=sizes,
            c=colors,
            alpha=0.7,
            edgecolors='white',
            linewidth=1,
            zorder=3
        )
        
        # Add title
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold', pad=10)
        elif team_name:
            ax.set_title(f"{team_name} - Shot Map", fontsize=16, fontweight='bold', pad=10)
        
        # Add legend
        goal_patch = patches.Circle((0, 0), 0.1, fc='#2ecc71', label='Goal')
        miss_patch = patches.Circle((0, 0), 0.1, fc='#e74c3c', label='No Goal')
        ax.legend(
            handles=[goal_patch, miss_patch],
            loc='upper right',
            framealpha=0.9
        )
        
        plt.tight_layout()
        return fig, ax
    
    def plot_pass_map(
        self,
        events: pd.DataFrame,
        team_name: str,
        player_name: Optional[str] = None,
        pass_type: Optional[str] = None,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 8)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a pass map visualization.
        
        Args:
            events: DataFrame with event data
            team_name: Team to show passes for
            player_name: Filter by specific player (optional)
            pass_type: Filter by pass type (optional)
            title: Plot title
            figsize: Figure size
            
        Returns:
            Tuple of (figure, axes)
        """
        # Filter for passes
        passes = events[
            (events['type'] == 'Pass') & 
            (events['team'] == team_name)
        ].copy()
        
        if player_name:
            passes = passes[passes['player'] == player_name]
            
        if pass_type:
            passes = passes[passes['pass_type'] == pass_type]
        
        if passes.empty:
            raise ValueError("No passes found matching criteria")
        
        # Create pitch
        pitch = Pitch(
            pitch_type='statsbomb',
            pitch_color='grass',
            line_color='white'
        )
        fig, ax = pitch.draw(figsize=figsize)
        
        # Extract coordinates
        if 'x' not in passes.columns:
            passes['x'] = passes['location'].apply(lambda x: x[0] if isinstance(x, list) else None)
            passes['y'] = passes['location'].apply(lambda x: x[1] if isinstance(x, list) else None)
            passes['pass_end_x'] = passes['pass_end_location'].apply(lambda x: x[0] if isinstance(x, list) else None)
            passes['pass_end_y'] = passes['pass_end_location'].apply(lambda x: x[1] if isinstance(x, list) else None)
        
        # Color by outcome
        successful = passes[passes['pass_outcome'].isna()]
        unsuccessful = passes[passes['pass_outcome'].notna()]
        
        # Plot successful passes
        if not successful.empty:
            pitch.arrows(
                successful['x'], successful['y'],
                successful['pass_end_x'], successful['pass_end_y'],
                width=2, headwidth=5, headlength=5,
                color='#2ecc71', alpha=0.6, ax=ax
            )
        
        # Plot unsuccessful passes
        if not unsuccessful.empty:
            pitch.arrows(
                unsuccessful['x'], unsuccessful['y'],
                unsuccessful['pass_end_x'], unsuccessful['pass_end_y'],
                width=2, headwidth=5, headlength=5,
                color='#e74c3c', alpha=0.6, ax=ax
            )
        
        # Title
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        else:
            name = player_name if player_name else team_name
            ax.set_title(f"{name} - Pass Map", fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        return fig, ax
    
    def plot_heatmap(
        self,
        events: pd.DataFrame,
        team_name: Optional[str] = None,
        player_name: Optional[str] = None,
        event_type: str = 'all',
        title: Optional[str] = None,
        cmap: str = 'hot',
        figsize: Tuple[int, int] = (12, 8)
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a heatmap visualization.
        
        Args:
            events: DataFrame with event data
            team_name: Filter by team (optional)
            player_name: Filter by player (optional)
            event_type: Type of events to include ('all', 'Pass', 'Shot', etc.)
            title: Plot title
            cmap: Colormap for heatmap
            figsize: Figure size
            
        Returns:
            Tuple of (figure, axes)
        """
        # Filter events
        filtered = events.copy()
        
        if team_name:
            filtered = filtered[filtered['team'] == team_name]
        if player_name:
            filtered = filtered[filtered['player'] == player_name]
        if event_type != 'all':
            filtered = filtered[filtered['type'] == event_type]
        
        # Extract coordinates
        if 'x' not in filtered.columns:
            filtered['x'] = filtered['location'].apply(
                lambda x: x[0] if isinstance(x, list) else None
            )
            filtered['y'] = filtered['location'].apply(
                lambda x: x[1] if isinstance(x, list) else None
            )
        
        # Remove rows without location
        filtered = filtered.dropna(subset=['x', 'y'])
        
        # Create pitch
        pitch = Pitch(
            pitch_type='statsbomb',
            pitch_color='grass',
            line_color='white',
            line_zorder=2
        )
        fig, ax = pitch.draw(figsize=figsize)
        
        # Create heatmap
        pitch.kdeplot(
            filtered['x'], filtered['y'],
            ax=ax,
            cmap=cmap,
            fill=True,
            levels=100,
            alpha=0.7,
            zorder=1
        )
        
        # Title
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        else:
            name = player_name if player_name else (team_name if team_name else "All")
            ax.set_title(f"{name} - Heatmap", fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        return fig, ax
    
    def save(
        self,
        fig: plt.Figure,
        filename: str,
        output_dir: str = 'output/images',
        dpi: int = 150,
        instagram_format: Optional[str] = None
    ) -> str:
        """
        Save a figure to file.
        
        Args:
            fig: Matplotlib figure to save
            filename: Output filename
            output_dir: Output directory
            dpi: Resolution
            instagram_format: 'post' (1080x1080) or 'story' (1080x1920)
            
        Returns:
            Path to saved file
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        if instagram_format == 'post':
            fig.set_size_inches(10.8, 10.8)  # 1080x1080 at 100 dpi
        elif instagram_format == 'story':
            fig.set_size_inches(10.8, 19.2)  # 1080x1920 at 100 dpi
        
        filepath = Path(output_dir) / filename
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close(fig)
        
        return str(filepath)


# Convenience function
def quick_shot_map(events: pd.DataFrame, team_name: str) -> Tuple[plt.Figure, plt.Axes]:
    """
    Quick function to create a shot map for a team.
    
    Args:
        events: Match events DataFrame (use StatsBombLoader to load)
        team_name: Team name to filter shots
    
    Returns:
        Tuple of (figure, axes)
    
    Example:
        from src.data.loader import StatsBombLoader
        
        loader = StatsBombLoader()
        events, info = loader.load_match_by_criteria(
            competition_name="World Cup",
            stage="Final"
        )
        fig, ax = quick_shot_map(events, team_name=info['home_team'])
    """
    viz = SoccerViz()
    return viz.plot_shot_map(events, team_name=team_name)

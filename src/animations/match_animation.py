"""
Animation Module for Soccer Analytics

This module provides functions to create animated visualizations
for match sequences, player movements, and tactical animations.

Usage:
    from src.animations.match_animation import MatchAnimator
    
    animator = MatchAnimator(events, match_id)
    animator.animate_sequence(start_frame=0, end_frame=100)
    animator.save_gif("goal_sequence.gif")
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mplsoccer import Pitch
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List, Dict, Any, Callable
from pathlib import Path
import imageio


class MatchAnimator:
    """
    A class for creating animated soccer visualizations.
    """
    
    def __init__(
        self,
        events: pd.DataFrame,
        fps: int = 25,
        figsize: Tuple[int, int] = (12, 8)
    ):
        """
        Initialize the animator.
        
        Args:
            events: DataFrame with event data
            fps: Frames per second for animation
            figsize: Figure size
        """
        self.events = events.copy()
        self.fps = fps
        self.figsize = figsize
        
        # Prepare location data
        self._prepare_locations()
        
        # Animation state
        self.fig = None
        self.ax = None
        self.pitch = None
        self.anim = None
        self.frames = []
        
    def _prepare_locations(self):
        """Extract and prepare location data from events."""
        if 'x' not in self.events.columns and 'location' in self.events.columns:
            self.events['x'] = self.events['location'].apply(
                lambda loc: loc[0] if isinstance(loc, list) and len(loc) >= 2 else None
            )
            self.events['y'] = self.events['location'].apply(
                lambda loc: loc[1] if isinstance(loc, list) and len(loc) >= 2 else None
            )
    
    def create_event_sequence_animation(
        self,
        event_indices: Optional[List[int]] = None,
        event_types: Optional[List[str]] = None,
        team_name: Optional[str] = None,
        time_range: Optional[Tuple[float, float]] = None,
        title: Optional[str] = None,
        show_trails: bool = True,
        trail_length: int = 5
    ) -> animation.FuncAnimation:
        """
        Create an animation showing a sequence of events.
        
        Args:
            event_indices: Specific event indices to animate
            event_types: Filter by event types (e.g., ['Pass', 'Shot'])
            team_name: Filter by team
            time_range: (start_minute, end_minute) to filter
            title: Animation title
            show_trails: Show trailing positions
            trail_length: Number of previous events to show as trail
            
        Returns:
            Matplotlib animation object
        """
        # Filter events
        filtered = self.events.copy()
        
        if event_types:
            filtered = filtered[filtered['type'].isin(event_types)]
        if team_name:
            filtered = filtered[filtered['team'] == team_name]
        if time_range:
            filtered = filtered[
                (filtered['minute'] >= time_range[0]) &
                (filtered['minute'] <= time_range[1])
            ]
        if event_indices:
            filtered = filtered.iloc[event_indices]
        
        # Remove events without location
        filtered = filtered.dropna(subset=['x', 'y']).reset_index(drop=True)
        
        if filtered.empty:
            raise ValueError("No events to animate after filtering")
        
        # Create pitch
        self.pitch = Pitch(
            pitch_type='statsbomb',
            pitch_color='grass',
            line_color='white'
        )
        self.fig, self.ax = self.pitch.draw(figsize=self.figsize)
        
        # Initialize plot elements
        ball_scatter = self.ax.scatter([], [], s=150, c='white', edgecolors='black', zorder=10)
        trail_scatter = self.ax.scatter([], [], s=50, c='white', alpha=0.3, zorder=5)
        event_text = self.ax.text(60, 2, '', fontsize=10, ha='center', color='white', 
                                  bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
        
        if title:
            self.ax.set_title(title, fontsize=14, fontweight='bold', color='white')
        
        def init():
            ball_scatter.set_offsets(np.empty((0, 2)))
            trail_scatter.set_offsets(np.empty((0, 2)))
            event_text.set_text('')
            return ball_scatter, trail_scatter, event_text
        
        def update(frame):
            if frame >= len(filtered):
                return ball_scatter, trail_scatter, event_text
            
            row = filtered.iloc[frame]
            
            # Update ball position
            ball_scatter.set_offsets([[row['x'], row['y']]])
            
            # Update trail
            if show_trails and frame > 0:
                start_idx = max(0, frame - trail_length)
                trail_data = filtered.iloc[start_idx:frame]
                trail_positions = trail_data[['x', 'y']].values
                trail_scatter.set_offsets(trail_positions)
            
            # Update event text
            minute = int(row.get('minute', 0))
            second = int(row.get('second', 0))
            event_type = row.get('type', 'Event')
            player = row.get('player', 'Unknown')
            event_text.set_text(f"{minute}:{second:02d} | {player} - {event_type}")
            
            return ball_scatter, trail_scatter, event_text
        
        self.anim = animation.FuncAnimation(
            self.fig, update, init_func=init,
            frames=len(filtered),
            interval=1000 / self.fps,
            blit=True
        )
        
        return self.anim
    
    def create_pass_flow_animation(
        self,
        team_name: str,
        time_range: Optional[Tuple[float, float]] = None,
        title: Optional[str] = None
    ) -> animation.FuncAnimation:
        """
        Create an animation showing passes flowing across the pitch.
        
        Args:
            team_name: Team to show passes for
            time_range: (start_minute, end_minute)
            title: Animation title
            
        Returns:
            Matplotlib animation object
        """
        # Filter for passes
        passes = self.events[
            (self.events['type'] == 'Pass') &
            (self.events['team'] == team_name)
        ].copy()
        
        if time_range:
            passes = passes[
                (passes['minute'] >= time_range[0]) &
                (passes['minute'] <= time_range[1])
            ]
        
        # Get end locations
        passes['pass_end_x'] = passes['pass_end_location'].apply(
            lambda x: x[0] if isinstance(x, list) else None
        )
        passes['pass_end_y'] = passes['pass_end_location'].apply(
            lambda x: x[1] if isinstance(x, list) else None
        )
        
        passes = passes.dropna(subset=['x', 'y', 'pass_end_x', 'pass_end_y']).reset_index(drop=True)
        
        # Create pitch
        self.pitch = Pitch(
            pitch_type='statsbomb',
            pitch_color='grass',
            line_color='white'
        )
        self.fig, self.ax = self.pitch.draw(figsize=self.figsize)
        
        if title:
            self.ax.set_title(title, fontsize=14, fontweight='bold')
        else:
            self.ax.set_title(f"{team_name} - Pass Flow", fontsize=14, fontweight='bold')
        
        # Store arrow artists
        arrows = []
        
        def init():
            return []
        
        def update(frame):
            if frame >= len(passes):
                return arrows
            
            row = passes.iloc[frame]
            
            # Determine color based on pass outcome
            color = '#2ecc71' if pd.isna(row.get('pass_outcome')) else '#e74c3c'
            
            # Add arrow
            arrow = self.ax.annotate(
                '',
                xy=(row['pass_end_x'], row['pass_end_y']),
                xytext=(row['x'], row['y']),
                arrowprops=dict(
                    arrowstyle='->', 
                    color=color, 
                    alpha=0.6,
                    lw=1.5
                ),
                zorder=5
            )
            arrows.append(arrow)
            
            return arrows
        
        self.anim = animation.FuncAnimation(
            self.fig, update, init_func=init,
            frames=len(passes),
            interval=200,  # 200ms between passes
            blit=False
        )
        
        return self.anim
    
    def save_gif(
        self,
        filename: str,
        output_dir: str = 'output/gifs',
        fps: Optional[int] = None,
        dpi: int = 100
    ) -> str:
        """
        Save the current animation as a GIF.
        
        Args:
            filename: Output filename
            output_dir: Output directory
            fps: Frames per second (uses instance fps if not specified)
            dpi: Resolution
            
        Returns:
            Path to saved file
        """
        if self.anim is None:
            raise ValueError("No animation created yet. Call an animation method first.")
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        filepath = Path(output_dir) / filename
        
        fps = fps or self.fps
        
        # Save using pillow writer
        writer = animation.PillowWriter(fps=fps)
        self.anim.save(str(filepath), writer=writer, dpi=dpi)
        
        plt.close(self.fig)
        return str(filepath)
    
    def save_video(
        self,
        filename: str,
        output_dir: str = 'output/videos',
        fps: Optional[int] = None,
        dpi: int = 150,
        codec: str = 'libx264'
    ) -> str:
        """
        Save the current animation as a video (MP4).
        
        Args:
            filename: Output filename
            output_dir: Output directory
            fps: Frames per second
            dpi: Resolution
            codec: Video codec
            
        Returns:
            Path to saved file
        """
        if self.anim is None:
            raise ValueError("No animation created yet. Call an animation method first.")
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        filepath = Path(output_dir) / filename
        
        fps = fps or self.fps
        
        # Save using ffmpeg writer
        writer = animation.FFMpegWriter(fps=fps, codec=codec, bitrate=2000)
        self.anim.save(str(filepath), writer=writer, dpi=dpi)
        
        plt.close(self.fig)
        return str(filepath)


class GoalSequenceAnimator:
    """
    Specialized animator for creating goal sequence visualizations.
    """
    
    def __init__(self, events: pd.DataFrame):
        """
        Initialize with match events.
        
        Args:
            events: DataFrame with match event data
        """
        self.events = events.copy()
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare event data for animation."""
        # Extract locations
        if 'x' not in self.events.columns:
            self.events['x'] = self.events['location'].apply(
                lambda loc: loc[0] if isinstance(loc, list) else None
            )
            self.events['y'] = self.events['location'].apply(
                lambda loc: loc[1] if isinstance(loc, list) else None
            )
    
    def get_goals(self) -> pd.DataFrame:
        """Get all goals from the match."""
        return self.events[
            (self.events['type'] == 'Shot') &
            (self.events['shot_outcome'] == 'Goal')
        ]
    
    def get_buildup_events(
        self,
        goal_index: int,
        num_events: int = 10
    ) -> pd.DataFrame:
        """
        Get the events leading up to a goal.
        
        Args:
            goal_index: Index of the goal in events DataFrame
            num_events: Number of events before the goal to include
            
        Returns:
            DataFrame with buildup events
        """
        start_idx = max(0, goal_index - num_events)
        return self.events.iloc[start_idx:goal_index + 1]
    
    def animate_goal(
        self,
        goal_index: int,
        num_buildup_events: int = 10,
        fps: int = 5,
        figsize: Tuple[int, int] = (12, 8)
    ) -> animation.FuncAnimation:
        """
        Create an animation of a goal and its buildup.
        
        Args:
            goal_index: Index of the goal in events DataFrame
            num_buildup_events: Number of events to show before the goal
            fps: Frames per second
            figsize: Figure size
            
        Returns:
            Matplotlib animation object
        """
        buildup = self.get_buildup_events(goal_index, num_buildup_events)
        goal = self.events.iloc[goal_index]
        
        animator = MatchAnimator(buildup, fps=fps, figsize=figsize)
        
        scorer = goal.get('player', 'Unknown')
        minute = int(goal.get('minute', 0))
        
        return animator.create_event_sequence_animation(
            title=f"⚽ GOAL! {scorer} ({minute}')",
            show_trails=True
        )

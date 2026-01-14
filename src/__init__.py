"""
Division FC Soccer Analytics Package

A comprehensive toolkit for creating soccer visualizations and animations
using StatsBomb data, optimized for Instagram content.

Author: Division FC
Data Source: StatsBomb Open Data (CC BY 4.0)
"""

__version__ = "1.0.0"
__author__ = "Division FC"

from src.data.loader import (
    StatsBombLoader,
    get_teams,
    get_players, 
    get_goals,
    get_shots,
    get_passes,
    calculate_xg,
    get_top_players_by_stat,
    get_match_stats
)
from src.animations.match_animation import MatchAnimator, GoalSequenceAnimator
from src.export.instagram import InstagramExporter

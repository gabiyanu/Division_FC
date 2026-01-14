"""
Soccer Analytics Visualization Package

A comprehensive toolkit for creating soccer visualizations and animations
using StatsBomb data, optimized for Instagram content.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from src.data.loader import StatsBombLoader, load_match_events, load_competitions
from src.visualizations.pitch import SoccerViz
from src.animations.match_animation import MatchAnimator, GoalSequenceAnimator
from src.export.instagram import InstagramExporter

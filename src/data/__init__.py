"""Data loading and processing module."""
from src.data.loader import (
    StatsBombLoader,
    get_teams,
    get_players,
    get_goals,
    get_shots,
    get_passes,
    calculate_xg,
    calculate_possession,
    get_top_players_by_stat,
    get_match_stats,
    get_display_name,
    get_short_name,
    KNOWN_NAMES,
)

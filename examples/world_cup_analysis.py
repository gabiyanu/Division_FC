#!/usr/bin/env python3
"""
Division FC - World Cup 2022 Final Analysis
============================================

This script demonstrates all visualization and animation capabilities
using the Argentina vs France World Cup 2022 Final.

All data is dynamically sourced from StatsBomb API - nothing is hardcoded.

Usage:
    python examples/world_cup_analysis.py

Author: Division FC
Data Source: StatsBomb Open Data (CC BY 4.0)
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch, Sbopen

# Import our modules
from src.branding.style import (
    ColorPalette, Typography, BrandElements, 
    apply_brand_style, get_brand_cmap
)
from src.animations.match_animation import MatchAnimator, GoalSequenceAnimator


# ============================================================================
# CONFIGURATION
# ============================================================================

# Output directories
OUTPUT_DIR = project_root / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
GIFS_DIR = OUTPUT_DIR / "gifs"

# Create directories
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
GIFS_DIR.mkdir(parents=True, exist_ok=True)

# Brand colors (bright neon palette)
COLORS = {
    'background': '#0D1117',
    'background_secondary': '#161B22',
    'cyan': '#00FFCC',
    'magenta': '#FF66B2',
    'purple': '#AA66FF',
    'gold': '#FFD700',
    'text_primary': '#F0F6FC',
    'text_secondary': '#8B949E',
    'success': '#3FB950',
    'danger': '#F85149',
}


# ============================================================================
# DATA LOADING - ALL VALUES SOURCED FROM API
# ============================================================================

def get_competition_id(parser, competition_name="FIFA World Cup"):
    """
    Dynamically fetch competition ID by name.
    
    Args:
        parser: Sbopen parser instance
        competition_name: Name of competition to find
    
    Returns:
        tuple: (competition_id, season_id) for most recent season
    """
    competitions = parser.competition()
    
    # Find competition by name
    comp = competitions[
        competitions['competition_name'].str.contains(competition_name, case=False, na=False)
    ]
    
    if len(comp) == 0:
        raise ValueError(f"Competition '{competition_name}' not found")
    
    # Get most recent season
    comp = comp.sort_values('season_id', ascending=False).iloc[0]
    
    return int(comp['competition_id']), int(comp['season_id'])


def get_final_match(parser, competition_id, season_id):
    """
    Dynamically find the final match of a competition.
    Handles different column name conventions from mplsoccer.
    
    Args:
        parser: Sbopen parser instance
        competition_id: Competition ID
        season_id: Season ID
    
    Returns:
        tuple: (Match info Series with standardized names, all matches DataFrame)
    """
    matches = parser.match(competition_id, season_id)
    
    # Find the stage column (mplsoccer may use different names)
    stage_col = None
    for col in ['competition_stage_name', 'competition_stage']:
        if col in matches.columns:
            stage_col = col
            break
    
    # Find final by competition_stage
    if stage_col:
        final = matches[
            matches[stage_col].str.contains('Final', case=False, na=False) &
            ~matches[stage_col].str.contains('Semi|Quarter', case=False, na=False)
        ]
        if len(final) > 0:
            return _standardize_match_info(final.iloc[0]), matches
    
    # Fallback: get last match by date
    matches_sorted = matches.sort_values('match_date', ascending=False)
    return _standardize_match_info(matches_sorted.iloc[0]), matches


def _standardize_match_info(match_row):
    """
    Standardize match info column names for consistent access.
    mplsoccer uses 'home_team_name' while we want 'home_team'.
    
    Args:
        match_row: Raw match Series from mplsoccer
    
    Returns:
        Series with standardized column names
    """
    result = match_row.copy()
    
    # Map mplsoccer column names to our standard names
    column_mappings = {
        'home_team_name': 'home_team',
        'away_team_name': 'away_team',
        'home_team_home_team_name': 'home_team',
        'away_team_away_team_name': 'away_team',
        'competition_stage_name': 'competition_stage',
        'competition_competition_name': 'competition',
        'competition_name': 'competition',
        'season_season_name': 'season',
        'season_name': 'season',
    }
    
    for old_name, new_name in column_mappings.items():
        if old_name in result.index and new_name not in result.index:
            result[new_name] = result[old_name]
    
    # Ensure essential columns exist by searching for patterns
    if 'home_team' not in result.index:
        for col in result.index:
            if 'home' in col.lower() and 'team' in col.lower() and 'name' in col.lower():
                result['home_team'] = result[col]
                break
    
    if 'away_team' not in result.index:
        for col in result.index:
            if 'away' in col.lower() and 'team' in col.lower() and 'name' in col.lower():
                result['away_team'] = result[col]
                break
    
    return result


def get_top_players(events, team_name, stat='shots', n=2):
    """
    Dynamically get top players for a team by a given stat.
    
    Args:
        events: Match events DataFrame
        team_name: Team to filter
        stat: Statistic to rank by ('shots', 'passes', 'touches')
        n: Number of players to return
    
    Returns:
        list: Player names
    """
    team_events = events[events['team_name'] == team_name]
    
    if stat == 'shots':
        player_stats = team_events[team_events['type_name'] == 'Shot'].groupby('player_name').size()
    elif stat == 'passes':
        player_stats = team_events[team_events['type_name'] == 'Pass'].groupby('player_name').size()
    else:  # touches
        player_stats = team_events[team_events['x'].notna()].groupby('player_name').size()
    
    return player_stats.nlargest(n).index.tolist()


def get_goals_from_data(events):
    """
    Dynamically extract all goals from match events.
    
    Args:
        events: Match events DataFrame
    
    Returns:
        DataFrame: Goal events with player, team, minute
    """
    goals = events[
        (events['type_name'] == 'Shot') &
        (events['outcome_name'] == 'Goal')
    ][['player_name', 'team_name', 'minute', 'second']].copy()
    
    return goals


def load_world_cup_final():
    """
    Load World Cup 2022 Final event data from StatsBomb.
    All IDs and values are dynamically sourced from the API.
    
    Returns:
        tuple: (events DataFrame, match info dict, all matches DataFrame)
    """
    print("=" * 60)
    print("DIVISION FC - WORLD CUP FINAL ANALYSIS")
    print("=" * 60)
    print("\n📊 Loading StatsBomb data...")
    
    parser = Sbopen()
    
    # Step 1: Get competition ID dynamically
    print("   🔍 Finding FIFA World Cup competition...")
    competition_id, season_id = get_competition_id(parser, "FIFA World Cup")
    print(f"   ✅ Found: competition_id={competition_id}, season_id={season_id}")
    
    # Step 2: Get final match dynamically
    print("   🔍 Finding Final match...")
    match_info, all_matches = get_final_match(parser, competition_id, season_id)
    match_id = int(match_info['match_id'])
    print(f"   ✅ Found: match_id={match_id}")
    
    # Step 3: Load events
    print("   📥 Loading match events...")
    events, related, freeze, tactics = parser.event(match_id)
    
    # Extract info from data (not hardcoded)
    home_team = match_info['home_team']
    away_team = match_info['away_team']
    home_score = match_info['home_score']
    away_score = match_info['away_score']
    match_date = match_info['match_date']
    
    print(f"\n✅ Loaded {len(events)} events")
    print(f"   Match: {home_team} vs {away_team}")
    print(f"   Score: {int(home_score)} - {int(away_score)}")
    print(f"   Date: {match_date}")
    
    # Show dynamically extracted goals
    goals = get_goals_from_data(events)
    print(f"\n⚽ Goals found in data ({len(goals)} total):")
    for _, goal in goals.iterrows():
        player_short = goal['player_name'].split()[-1]
        print(f"   {int(goal['minute'])}' - {player_short} ({goal['team_name']})")
    
    return events, match_info, all_matches


# ============================================================================
# VISUALIZATION 1: SHOT MAP
# ============================================================================

def create_shot_map(events, player_name, filename):
    """
    Create a branded shot map for a specific player.
    
    Inputs:
        events (DataFrame): Match event data
        player_name (str): Full player name to filter
        filename (str): Output filename
    """
    print(f"\n🎯 Creating shot map for {player_name.split()[-1]}...")
    
    # Filter shots for player
    shots = events[
        (events['type_name'] == 'Shot') & 
        (events['player_name'] == player_name)
    ].copy()
    
    if len(shots) == 0:
        print(f"   ⚠️ No shots found for {player_name}")
        return
    
    # Create figure with dark background
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Draw pitch
    pitch = VerticalPitch(
        pitch_type='statsbomb',
        half=True,
        pitch_color=COLORS['background'],
        line_color=COLORS['text_secondary'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Plot shots
    for idx, shot in shots.iterrows():
        # Determine color based on outcome
        if shot['outcome_name'] == 'Goal':
            color = COLORS['gold']
            size = 400
            marker = '*'
            zorder = 10
        else:
            color = COLORS['cyan'] if shot.get('shot_statsbomb_xg', 0) > 0.1 else COLORS['magenta']
            size = 150 + (shot.get('shot_statsbomb_xg', 0.1) * 500)
            marker = 'o'
            zorder = 5
        
        ax.scatter(
            shot['y'], shot['x'],
            s=size,
            c=color,
            marker=marker,
            edgecolors='white',
            linewidths=1,
            alpha=0.9,
            zorder=zorder
        )
    
    # Calculate stats
    total_shots = len(shots)
    goals = len(shots[shots['outcome_name'] == 'Goal'])
    total_xg = shots['shot_statsbomb_xg'].sum() if 'shot_statsbomb_xg' in shots.columns else 0
    
    # Title
    short_name = player_name.split()[-1]
    ax.text(
        40, 125, short_name.upper(),
        fontsize=28, fontweight='bold',
        color=COLORS['text_primary'],
        ha='center'
    )
    ax.text(
        40, 122, 'SHOT MAP • WORLD CUP 2022 FINAL',
        fontsize=12,
        color=COLORS['text_secondary'],
        ha='center'
    )
    
    # Stats box
    stats_text = f"Shots: {total_shots}  |  Goals: {goals}  |  xG: {total_xg:.2f}"
    ax.text(
        40, 2, stats_text,
        fontsize=10,
        color=COLORS['cyan'],
        ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['background_secondary'], edgecolor=COLORS['cyan'], alpha=0.8)
    )
    
    # Legend
    ax.scatter([], [], s=150, c=COLORS['cyan'], marker='o', label='Shot')
    ax.scatter([], [], s=300, c=COLORS['gold'], marker='*', label='Goal')
    ax.legend(
        loc='upper right',
        facecolor=COLORS['background_secondary'],
        edgecolor=COLORS['text_secondary'],
        labelcolor=COLORS['text_primary'],
        fontsize=9
    )
    
    # Watermark
    ax.text(
        78, 2, 'DIVISION FC',
        fontsize=8, color=COLORS['cyan'],
        alpha=0.7, ha='right'
    )
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved to {filepath}")


# ============================================================================
# VISUALIZATION 2: TOUCH HEATMAP
# ============================================================================

def create_touch_heatmap(events, player_name, filename):
    """
    Create a branded touch heatmap for a specific player.
    
    Inputs:
        events (DataFrame): Match event data
        player_name (str): Full player name to filter
        filename (str): Output filename
    """
    print(f"\n🔥 Creating touch heatmap for {player_name.split()[-1]}...")
    
    # Filter events for player with location
    player_events = events[
        (events['player_name'] == player_name) &
        (events['x'].notna()) &
        (events['y'].notna())
    ].copy()
    
    if len(player_events) == 0:
        print(f"   ⚠️ No events found for {player_name}")
        return
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Draw pitch
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color=COLORS['background'],
        line_color=COLORS['text_secondary'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Create heatmap using kernel density
    from scipy.ndimage import gaussian_filter
    
    # Bin the data
    x_bins = np.linspace(0, 120, 25)
    y_bins = np.linspace(0, 80, 17)
    
    heatmap, xedges, yedges = np.histogram2d(
        player_events['x'], 
        player_events['y'],
        bins=[x_bins, y_bins]
    )
    
    # Smooth the heatmap
    heatmap = gaussian_filter(heatmap, sigma=1.5)
    
    # Create custom colormap (cyan to magenta)
    from matplotlib.colors import LinearSegmentedColormap
    aurora_cmap = LinearSegmentedColormap.from_list(
        'aurora',
        ['#0D1117', '#00FFCC', '#AA66FF', '#FF66B2', '#FFD700']
    )
    
    # Plot heatmap
    extent = [0, 120, 0, 80]
    im = ax.imshow(
        heatmap.T,
        extent=extent,
        origin='lower',
        cmap=aurora_cmap,
        alpha=0.7,
        aspect='auto',
        zorder=1
    )
    
    # Title
    short_name = player_name.split()[-1]
    ax.text(
        60, 86, short_name.upper(),
        fontsize=28, fontweight='bold',
        color=COLORS['text_primary'],
        ha='center'
    )
    ax.text(
        60, 83, 'TOUCH HEATMAP • WORLD CUP 2022 FINAL',
        fontsize=12,
        color=COLORS['text_secondary'],
        ha='center'
    )
    
    # Stats
    total_touches = len(player_events)
    ax.text(
        60, -4, f"Total Touches: {total_touches}",
        fontsize=11,
        color=COLORS['cyan'],
        ha='center'
    )
    
    # Watermark
    ax.text(
        118, -4, 'DIVISION FC',
        fontsize=8, color=COLORS['cyan'],
        alpha=0.7, ha='right'
    )
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved to {filepath}")


# ============================================================================
# VISUALIZATION 3: PASS NETWORK
# ============================================================================

def create_pass_network(events, team_name, filename):
    """
    Create a branded pass network for a team.
    
    Inputs:
        events (DataFrame): Match event data
        team_name (str): Team name to filter
        filename (str): Output filename
    """
    print(f"\n🔗 Creating pass network for {team_name}...")
    
    # Filter passes for team
    passes = events[
        (events['type_name'] == 'Pass') &
        (events['team_name'] == team_name) &
        (events['outcome_name'].isna())  # Successful passes only
    ].copy()
    
    if len(passes) == 0:
        print(f"   ⚠️ No passes found for {team_name}")
        return
    
    # Calculate average positions
    avg_positions = passes.groupby('player_name').agg({
        'x': 'mean',
        'y': 'mean',
        'id': 'count'
    }).rename(columns={'id': 'count'}).reset_index()
    
    # Get pass combinations
    passes['pass_recipient_name'] = passes['pass_recipient_name'].fillna('')
    pass_combinations = passes.groupby(['player_name', 'pass_recipient_name']).size().reset_index(name='pass_count')
    pass_combinations = pass_combinations[pass_combinations['pass_recipient_name'] != '']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Draw pitch
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color=COLORS['background'],
        line_color=COLORS['text_secondary'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Draw pass lines
    for _, row in pass_combinations.iterrows():
        if row['pass_count'] >= 3:  # Only show frequent combinations
            passer = avg_positions[avg_positions['player_name'] == row['player_name']]
            receiver = avg_positions[avg_positions['player_name'] == row['pass_recipient_name']]
            
            if len(passer) > 0 and len(receiver) > 0:
                ax.plot(
                    [passer['x'].values[0], receiver['x'].values[0]],
                    [passer['y'].values[0], receiver['y'].values[0]],
                    color=COLORS['cyan'],
                    linewidth=min(row['pass_count'] / 3, 5),
                    alpha=0.6,
                    zorder=1
                )
    
    # Draw player nodes
    for _, player in avg_positions.iterrows():
        ax.scatter(
            player['x'], player['y'],
            s=player['count'] * 3,
            c=COLORS['magenta'],
            edgecolors='white',
            linewidths=2,
            zorder=5
        )
        
        # Add name label
        short_name = player['player_name'].split()[-1][:8]
        ax.text(
            player['x'], player['y'] - 4,
            short_name,
            fontsize=7,
            color=COLORS['text_primary'],
            ha='center',
            zorder=6
        )
    
    # Title
    ax.text(
        60, 86, team_name.upper(),
        fontsize=28, fontweight='bold',
        color=COLORS['text_primary'],
        ha='center'
    )
    ax.text(
        60, 83, 'PASS NETWORK • WORLD CUP 2022 FINAL',
        fontsize=12,
        color=COLORS['text_secondary'],
        ha='center'
    )
    
    # Watermark
    ax.text(
        118, -4, 'DIVISION FC',
        fontsize=8, color=COLORS['cyan'],
        alpha=0.7, ha='right'
    )
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved to {filepath}")


# ============================================================================
# VISUALIZATION 4: ZONE CONTROL
# ============================================================================

def create_zone_control(events, home_team, away_team, filename):
    """
    Create a territorial control map showing pitch dominance.
    
    Inputs:
        events (DataFrame): Match event data
        home_team (str): Home team name
        away_team (str): Away team name
        filename (str): Output filename
    """
    print(f"\n🗺️ Creating zone control map...")
    
    # Filter events with locations
    home_events = events[
        (events['team_name'] == home_team) &
        (events['x'].notna()) &
        (events['y'].notna())
    ]
    away_events = events[
        (events['team_name'] == away_team) &
        (events['x'].notna()) &
        (events['y'].notna())
    ]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Draw pitch
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color=COLORS['background'],
        line_color=COLORS['text_secondary'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Define zones
    x_zones = [0, 40, 80, 120]
    y_zones = [0, 26.67, 53.33, 80]
    
    for i in range(len(x_zones) - 1):
        for j in range(len(y_zones) - 1):
            x_min, x_max = x_zones[i], x_zones[i + 1]
            y_min, y_max = y_zones[j], y_zones[j + 1]
            
            # Count events in zone
            home_count = len(home_events[
                (home_events['x'] >= x_min) & (home_events['x'] < x_max) &
                (home_events['y'] >= y_min) & (home_events['y'] < y_max)
            ])
            away_count = len(away_events[
                (away_events['x'] >= x_min) & (away_events['x'] < x_max) &
                (away_events['y'] >= y_min) & (away_events['y'] < y_max)
            ])
            
            total = home_count + away_count
            if total > 0:
                home_pct = home_count / total
                
                # Color based on dominance
                if home_pct > 0.55:
                    color = COLORS['cyan']
                    alpha = min(0.3 + (home_pct - 0.5) * 0.8, 0.7)
                elif home_pct < 0.45:
                    color = COLORS['magenta']
                    alpha = min(0.3 + (0.5 - home_pct) * 0.8, 0.7)
                else:
                    color = COLORS['purple']
                    alpha = 0.2
                
                # Draw zone
                rect = plt.Rectangle(
                    (x_min, y_min), x_max - x_min, y_max - y_min,
                    facecolor=color,
                    alpha=alpha,
                    edgecolor='white',
                    linewidth=0.5,
                    zorder=1
                )
                ax.add_patch(rect)
                
                # Add percentage text
                ax.text(
                    (x_min + x_max) / 2, (y_min + y_max) / 2,
                    f"{home_pct:.0%}",
                    fontsize=10, fontweight='bold',
                    color='white',
                    ha='center', va='center',
                    zorder=2
                )
    
    # Title
    ax.text(
        60, 86, 'TERRITORIAL CONTROL',
        fontsize=28, fontweight='bold',
        color=COLORS['text_primary'],
        ha='center'
    )
    ax.text(
        60, 83, f'{home_team} vs {away_team} • WORLD CUP 2022 FINAL',
        fontsize=12,
        color=COLORS['text_secondary'],
        ha='center'
    )
    
    # Legend
    ax.text(5, -4, f"■ {home_team}", fontsize=10, color=COLORS['cyan'])
    ax.text(50, -4, "■ Contested", fontsize=10, color=COLORS['purple'])
    ax.text(95, -4, f"■ {away_team}", fontsize=10, color=COLORS['magenta'])
    
    # Watermark
    ax.text(
        118, -8, 'DIVISION FC',
        fontsize=8, color=COLORS['cyan'],
        alpha=0.7, ha='right'
    )
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved to {filepath}")


# ============================================================================
# VISUALIZATION 5: MATCH SUMMARY
# ============================================================================

def create_match_summary(events, match_info, filename):
    """
    Create an Instagram-ready match summary graphic.
    All values sourced from data.
    
    Inputs:
        events (DataFrame): Match event data
        match_info (Series): Match metadata
        filename (str): Output filename
    """
    print(f"\n📱 Creating match summary graphic...")
    
    # Extract all values from data (not hardcoded)
    home_team = match_info['home_team']
    away_team = match_info['away_team']
    home_score = int(match_info['home_score'])
    away_score = int(match_info['away_score'])
    match_date = str(match_info['match_date'])
    competition = match_info.get('competition', 'Match')
    
    # Calculate stats from event data
    home_events = events[events['team_name'] == home_team]
    away_events = events[events['team_name'] == away_team]
    
    home_shots = len(home_events[home_events['type_name'] == 'Shot'])
    away_shots = len(away_events[away_events['type_name'] == 'Shot'])
    
    home_passes = len(home_events[home_events['type_name'] == 'Pass'])
    away_passes = len(away_events[away_events['type_name'] == 'Pass'])
    
    # Calculate xG from data
    home_shot_data = home_events[home_events['type_name'] == 'Shot']
    away_shot_data = away_events[away_events['type_name'] == 'Shot']
    
    home_xg = home_shot_data['shot_statsbomb_xg'].sum() if 'shot_statsbomb_xg' in home_shot_data.columns else 0
    away_xg = away_shot_data['shot_statsbomb_xg'].sum() if 'shot_statsbomb_xg' in away_shot_data.columns else 0
    
    # Calculate possession from data (based on events)
    total_events = len(events[events['team_name'].isin([home_team, away_team])])
    home_possession = len(home_events) / total_events * 100 if total_events > 0 else 50
    away_possession = 100 - home_possession
    
    # Create figure (Instagram square format)
    fig, ax = plt.subplots(figsize=(10, 10), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title from data
    stage = match_info.get('competition_stage', '')
    title_text = f"{competition}" if not stage else f"{competition} - {stage}"
    ax.text(50, 92, title_text.upper(), fontsize=14, color=COLORS['text_secondary'], ha='center', fontweight='bold')
    
    # Team names from data
    ax.text(25, 80, home_team.upper(), fontsize=20, color=COLORS['cyan'], ha='center', fontweight='bold')
    ax.text(75, 80, away_team.upper(), fontsize=20, color=COLORS['magenta'], ha='center', fontweight='bold')
    
    # Score from data
    ax.text(25, 68, str(home_score), fontsize=48, color=COLORS['gold'], ha='center', fontweight='bold')
    ax.text(50, 68, '-', fontsize=48, color=COLORS['text_secondary'], ha='center')
    ax.text(75, 68, str(away_score), fontsize=48, color=COLORS['gold'], ha='center', fontweight='bold')
    
    # Date from data
    ax.text(50, 55, match_date, fontsize=11, color=COLORS['text_secondary'], ha='center')
    
    # Stats - all calculated from event data
    stats_y = 42
    stat_spacing = 8
    
    stats = [
        ('xG', f'{home_xg:.2f}', f'{away_xg:.2f}'),
        ('Shots', str(home_shots), str(away_shots)),
        ('Passes', str(home_passes), str(away_passes)),
        ('Possession', f'{home_possession:.0f}%', f'{away_possession:.0f}%'),
    ]
    
    for i, (label, home_val, away_val) in enumerate(stats):
        y = stats_y - (i * stat_spacing)
        ax.text(25, y, home_val, fontsize=16, color=COLORS['text_primary'], ha='center', fontweight='bold')
        ax.text(50, y, label.upper(), fontsize=11, color=COLORS['text_secondary'], ha='center')
        ax.text(75, y, away_val, fontsize=16, color=COLORS['text_primary'], ha='center', fontweight='bold')
    
    # Divider line
    ax.axhline(y=48, xmin=0.15, xmax=0.85, color=COLORS['purple'], linewidth=2, alpha=0.5)
    
    # Watermark
    ax.text(50, 5, 'DIVISION FC', fontsize=12, color=COLORS['cyan'], ha='center', alpha=0.8)
    ax.text(50, 2, 'Data: StatsBomb', fontsize=8, color=COLORS['text_secondary'], ha='center')
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved to {filepath}")


# ============================================================================
# ANIMATION: GOAL SEQUENCE
# ============================================================================

def create_goal_animation(events, goal_minute, team_name, filename):
    """
    Create an animated GIF showing goal buildup.
    
    Inputs:
        events (DataFrame): Match event data
        goal_minute (int): Minute of the goal
        team_name (str): Scoring team
        filename (str): Output filename
    """
    print(f"\n🎬 Creating goal animation ({team_name}, {goal_minute}')...")
    
    try:
        # Find goal
        goals = events[
            (events['type_name'] == 'Shot') &
            (events['outcome_name'] == 'Goal') &
            (events['team_name'] == team_name) &
            (events['minute'] >= goal_minute - 1) &
            (events['minute'] <= goal_minute + 1)
        ]
        
        if len(goals) == 0:
            print(f"   ⚠️ Goal not found at minute {goal_minute}")
            return
        
        goal_idx = goals.index[0]
        
        # Get buildup events (10 events before goal)
        buildup_start = max(0, goal_idx - 10)
        buildup_events = events.iloc[buildup_start:goal_idx + 1].copy()
        
        # Filter to relevant team and events with locations
        buildup_events = buildup_events[
            buildup_events['x'].notna() &
            buildup_events['y'].notna()
        ]
        
        # Create animator
        animator = MatchAnimator(buildup_events, fps=5, figsize=(12, 8))
        
        # Create animation
        scorer = goals.iloc[0]['player_name'].split()[-1]
        anim = animator.create_event_sequence_animation(
            title=f"⚽ GOAL! {scorer} ({goal_minute}')",
            show_trails=True,
            trail_length=5
        )
        
        # Save GIF
        filepath = GIFS_DIR / filename
        animator.save_gif(filename, output_dir=str(GIFS_DIR), fps=5, dpi=100)
        print(f"   ✅ Saved to {filepath}")
        
    except Exception as e:
        print(f"   ⚠️ Animation error: {e}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run the complete World Cup analysis demo with all data sourced from API."""
    
    # Load data - all values sourced dynamically
    events, match_info, all_matches = load_world_cup_final()
    
    # Extract team names from data (not hardcoded)
    home_team = match_info['home_team']
    away_team = match_info['away_team']
    
    print("\n" + "=" * 60)
    print("CREATING VISUALIZATIONS")
    print("=" * 60)
    
    # Dynamically get top shooters from each team
    home_shooters = get_top_players(events, home_team, stat='shots', n=1)
    away_shooters = get_top_players(events, away_team, stat='shots', n=1)
    
    print(f"\n🎯 Top shooters found in data:")
    print(f"   {home_team}: {[p.split()[-1] for p in home_shooters]}")
    print(f"   {away_team}: {[p.split()[-1] for p in away_shooters]}")
    
    # 1. Shot Maps - players sourced from data
    for player in home_shooters:
        short_name = player.split()[-1].lower()
        create_shot_map(events, player, f'{short_name}_shot_map.png')
    
    for player in away_shooters:
        short_name = player.split()[-1].lower()
        create_shot_map(events, player, f'{short_name}_shot_map.png')
    
    # 2. Touch Heatmaps - get top players by touches
    home_touch_leaders = get_top_players(events, home_team, stat='touches', n=1)
    away_touch_leaders = get_top_players(events, away_team, stat='touches', n=1)
    
    for player in home_touch_leaders:
        short_name = player.split()[-1].lower()
        create_touch_heatmap(events, player, f'{short_name}_heatmap.png')
    
    for player in away_touch_leaders:
        short_name = player.split()[-1].lower()
        create_touch_heatmap(events, player, f'{short_name}_heatmap.png')
    
    # 3. Pass Networks - team names from data
    create_pass_network(events, home_team, f'{home_team.lower().replace(" ", "_")}_pass_network.png')
    create_pass_network(events, away_team, f'{away_team.lower().replace(" ", "_")}_pass_network.png')
    
    # 4. Zone Control - teams from data
    create_zone_control(events, home_team, away_team, 'zone_control.png')
    
    # 5. Match Summary - all info from data
    create_match_summary(events, match_info, 'match_summary.png')
    
    print("\n" + "=" * 60)
    print("CREATING ANIMATIONS")
    print("=" * 60)
    
    # Get goals dynamically from data
    goals = get_goals_from_data(events)
    
    # Create animation for first goal from each team (if exists)
    teams_with_goals = goals['team_name'].unique()
    
    for team in teams_with_goals:
        team_goals = goals[goals['team_name'] == team]
        if len(team_goals) > 0:
            first_goal = team_goals.iloc[0]
            goal_minute = int(first_goal['minute'])
            team_short = team.lower().replace(" ", "_")
            create_goal_animation(events, goal_minute, team, f'{team_short}_goal_1.gif')
    
    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Output files saved to:")
    print(f"   Images: {IMAGES_DIR}")
    print(f"   GIFs: {GIFS_DIR}")
    print(f"\n🏆 Division FC - {match_info['competition']} Analysis")
    print("   Data provided by StatsBomb (CC BY 4.0)")


if __name__ == "__main__":
    main()

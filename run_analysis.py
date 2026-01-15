#!/usr/bin/env python3
import pandas as pd
"""
Division FC - Main Analysis Script
===================================

Run all visualizations and animations for the configured match.
Match settings are in: config/match_config.py

Usage:
    python run_analysis.py

Author: Division FC
Data Source: StatsBomb Open Data (CC BY 4.0)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import Pitch, VerticalPitch

# Import config (SINGLE SOURCE OF TRUTH)
from config.match_config import (
    get_match_data,
    get_home_team,
    get_away_team,
    COLORS,
    IMAGES_DIR,
    GIFS_DIR,
    VIZ_CONFIG,
)

# Import utilities
from src.data.loader import (
    get_goals,
    get_shots,
    get_passes,
    get_top_players_by_stat,
    get_display_name,
    calculate_xg,
)


def get_player_name(full_name):
    """
    Get player name based on config setting.
    Uses full name or display name based on VIZ_CONFIG.
    """
    if VIZ_CONFIG.get('use_display_names', False):
        return get_display_name(full_name)
    return full_name


def get_clean_filename(name):
    """
    Create a clean filename from a name.
    Handles long names by taking last name portion.
    """
    # Remove special characters and spaces
    clean = name.lower().replace(' ', '_').replace("'", "").replace("á", "a").replace("é", "e")
    clean = clean.replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
    
    # If name is too long, use last part
    if len(clean) > 30:
        parts = name.split()
        clean = parts[-1].lower() if parts else clean[:20]
    
    return clean


# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def create_shot_map(events, player_name, filename):
    """
    Create branded shot map for a player.
    
    Args:
        events: Match events DataFrame
        player_name: Full player name from data
        filename: Output filename
    """
    # Filter shots for player
    shots = events[
        (events['type_name'] == 'Shot') &
        (events['player_name'] == player_name)
    ].copy()
    
    if len(shots) == 0:
        print(f"⚠️ No shots found for {player_name}")
        return
    
    # Stats from data
    total_shots = len(shots)
    goals = len(shots[shots['outcome_name'] == 'Goal'])
    total_xg = calculate_xg(shots)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 12), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Draw pitch
    pitch = VerticalPitch(
        pitch_type='statsbomb',
        half=True,
        pitch_color=COLORS['background'],
        line_color=COLORS['pitch_line'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Plot shots
    for _, shot in shots.iterrows():
        is_goal = shot['outcome_name'] == 'Goal'
        xg = shot.get('shot_statsbomb_xg', 0.1)
        
        ax.scatter(
            shot['y'], shot['x'],
            s=400 if is_goal else (100 + xg * 400),
            c=COLORS['gold'] if is_goal else COLORS['cyan'],
            marker='*' if is_goal else 'o',
            edgecolors='white',
            linewidths=1.5,
            alpha=0.9,
            zorder=10 if is_goal else 5
        )
    
    # Title - use display name
    display_name = get_player_name(player_name)
    ax.text(40, 125, display_name.upper(), fontsize=28, fontweight='bold',
            color=COLORS['text'], ha='center')
    ax.text(40, 121, 'SHOT MAP', fontsize=12,
            color=COLORS['text_secondary'], ha='center')
    
    # Stats box
    stats_text = f"Shots: {total_shots}  •  Goals: {goals}  •  xG: {total_xg:.2f}"
    ax.text(40, 4, stats_text, fontsize=10, fontweight='bold',
            color=COLORS['cyan'], ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['background'],
                     edgecolor=COLORS['cyan'], alpha=0.9))
    
    # Legend
    ax.scatter([], [], s=100, c=COLORS['cyan'], marker='o', label='Shot')
    ax.scatter([], [], s=300, c=COLORS['gold'], marker='*', label='Goal')
    ax.legend(loc='upper right', facecolor=COLORS['background'],
              edgecolor=COLORS['text_secondary'], labelcolor=COLORS['text'], fontsize=9)
    
    # Watermark
    ax.text(78, 2, 'DIVISION FC', fontsize=8, color=COLORS['cyan'], alpha=0.7, ha='right')
    
    plt.tight_layout()
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=VIZ_CONFIG['dpi'], bbox_inches='tight',
                facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved: {filepath}")


def create_touch_heatmap(events, player_name, filename):
    """
    Create branded touch heatmap for a player.
    
    Args:
        events: Match events DataFrame
        player_name: Full player name from data
        filename: Output filename
    """
    # Filter events with valid locations
    player_events = events[
        (events['player_name'] == player_name) &
        (events['x'].notna()) &
        (events['y'].notna())
    ].copy()
    
    if len(player_events) == 0:
        print(f"⚠️ No events found for {player_name}")
        return
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Draw pitch
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color=COLORS['background'],
        line_color=COLORS['pitch_line'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Create heatmap
    x_bins = np.linspace(0, 120, 25)
    y_bins = np.linspace(0, 80, 17)
    heatmap, _, _ = np.histogram2d(player_events['x'], player_events['y'], bins=[x_bins, y_bins])
    heatmap = gaussian_filter(heatmap, sigma=1.5)
    
    # Custom colormap
    aurora_cmap = LinearSegmentedColormap.from_list(
        'aurora', [COLORS['background'], COLORS['cyan'], COLORS['purple'], COLORS['magenta'], COLORS['gold']]
    )
    
    # Plot heatmap
    ax.imshow(heatmap.T, extent=[0, 120, 0, 80], origin='lower',
              cmap=aurora_cmap, alpha=0.8, aspect='auto', zorder=1)
    
    # Title - use display name
    display_name = get_player_name(player_name)
    ax.text(60, 86, display_name.upper(), fontsize=24, fontweight='bold',
            color=COLORS['text'], ha='center')
    ax.text(60, 83, 'TOUCH HEATMAP', fontsize=11,
            color=COLORS['text_secondary'], ha='center')
    
    # Stats
    ax.text(60, -4, f"Total Touches: {len(player_events)}", fontsize=10,
            color=COLORS['cyan'], ha='center')
    
    # Watermark
    ax.text(118, -4, 'DIVISION FC', fontsize=8, color=COLORS['cyan'], alpha=0.7, ha='right')
    
    plt.tight_layout()
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=VIZ_CONFIG['dpi'], bbox_inches='tight',
                facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved: {filepath}")


def create_pass_network(events, team_name, filename):
    """
    Create branded pass network for a team.
    
    Args:
        events: Match events DataFrame
        team_name: Team name from data
        filename: Output filename
    """
    # Filter successful passes
    passes = events[
        (events['type_name'] == 'Pass') &
        (events['team_name'] == team_name) &
        (events['outcome_name'].isna())  # Successful passes
    ].copy()
    
    if len(passes) == 0:
        print(f"⚠️ No passes found for {team_name}")
        return
    
    # Calculate average positions
    avg_positions = passes.groupby('player_name').agg({
        'x': 'mean',
        'y': 'mean',
        'id': 'count'
    }).rename(columns={'id': 'count'}).reset_index()
    
    # Get pass combinations
    passes['recipient'] = passes['pass_recipient_name'].fillna('')
    pass_combos = passes.groupby(['player_name', 'recipient']).size().reset_index(name='pass_count')
    pass_combos = pass_combos[pass_combos['recipient'] != '']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color=COLORS['background'],
        line_color=COLORS['pitch_line'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Draw pass lines (minimum 3 passes to show)
    for _, row in pass_combos.iterrows():
        if row['pass_count'] >= 3:
            passer_pos = avg_positions[avg_positions['player_name'] == row['player_name']]
            receiver_pos = avg_positions[avg_positions['player_name'] == row['recipient']]
            
            if len(passer_pos) > 0 and len(receiver_pos) > 0:
                ax.plot(
                    [passer_pos['x'].values[0], receiver_pos['x'].values[0]],
                    [passer_pos['y'].values[0], receiver_pos['y'].values[0]],
                    color=COLORS['cyan'],
                    linewidth=min(row['pass_count'] / 3, 5),
                    alpha=0.6,
                    zorder=1
                )
    
    # Draw player nodes with names
    for _, player in avg_positions.iterrows():
        # Node
        ax.scatter(player['x'], player['y'],
                   s=player['count'] * 3,
                   c=COLORS['magenta'],
                   edgecolors='white',
                   linewidths=2,
                   zorder=5)
        
        # Player name - use display name
        display_name = get_player_name(player['player_name'])
        ax.text(player['x'], player['y'] - 4, display_name,
                fontsize=7, color=COLORS['text'], ha='center', zorder=6)
    
    # Title
    ax.text(60, 86, team_name.upper(), fontsize=24, fontweight='bold',
            color=COLORS['text'], ha='center')
    ax.text(60, 83, 'PASS NETWORK', fontsize=11,
            color=COLORS['text_secondary'], ha='center')
    
    # Watermark
    ax.text(118, -4, 'DIVISION FC', fontsize=8, color=COLORS['cyan'], alpha=0.7, ha='right')
    
    plt.tight_layout()
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=VIZ_CONFIG['dpi'], bbox_inches='tight',
                facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved: {filepath}")


def create_zone_control(events, home_team, away_team, filename):
    """
    Create zone control visualization showing territorial dominance.
    
    Args:
        events: Match events DataFrame
        home_team: Home team name
        away_team: Away team name
        filename: Output filename
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color=COLORS['background'],
        line_color=COLORS['pitch_line'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Define zones (3x3 grid)
    x_zones = [0, 40, 80, 120]
    y_zones = [0, 26.67, 53.33, 80]
    
    zone_labels = [
        ['DEF\nLEFT', 'DEF\nCENTER', 'DEF\nRIGHT'],
        ['MID\nLEFT', 'MID\nCENTER', 'MID\nRIGHT'],
        ['ATT\nLEFT', 'ATT\nCENTER', 'ATT\nRIGHT']
    ]
    
    # Calculate control per zone
    for i in range(3):
        for j in range(3):
            x_min, x_max = x_zones[i], x_zones[i+1]
            y_min, y_max = y_zones[j], y_zones[j+1]
            
            zone_events = events[
                (events['x'] >= x_min) & (events['x'] < x_max) &
                (events['y'] >= y_min) & (events['y'] < y_max) &
                (events['x'].notna())
            ]
            
            home_events = len(zone_events[zone_events['team_name'] == home_team])
            away_events = len(zone_events[zone_events['team_name'] == away_team])
            total = home_events + away_events
            
            if total > 0:
                home_pct = home_events / total
                
                # Color based on dominance
                if home_pct > 0.55:
                    color = COLORS['cyan']
                    alpha = 0.3 + (home_pct - 0.5) * 0.8
                elif home_pct < 0.45:
                    color = COLORS['magenta']
                    alpha = 0.3 + (0.5 - home_pct) * 0.8
                else:
                    color = COLORS['purple']
                    alpha = 0.2
                
                # Draw zone rectangle
                rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                                     facecolor=color, alpha=alpha, zorder=1)
                ax.add_patch(rect)
                
                # Add percentage text
                x_center = (x_min + x_max) / 2
                y_center = (y_min + y_max) / 2
                ax.text(x_center, y_center, f"{home_pct*100:.0f}%",
                       fontsize=16, fontweight='bold', color=COLORS['text'],
                       ha='center', va='center', zorder=3)
    
    # Title
    ax.text(60, 86, 'ZONE CONTROL', fontsize=24, fontweight='bold',
            color=COLORS['text'], ha='center')
    
    # Legend
    ax.text(30, -6, f"■ {home_team}", fontsize=10, color=COLORS['cyan'], ha='center')
    ax.text(90, -6, f"■ {away_team}", fontsize=10, color=COLORS['magenta'], ha='center')
    
    # Watermark
    ax.text(118, -6, 'DIVISION FC', fontsize=8, color=COLORS['cyan'], alpha=0.7, ha='right')
    
    plt.tight_layout()
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=VIZ_CONFIG['dpi'], bbox_inches='tight',
                facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved: {filepath}")


def create_match_summary(events, match_info, filename):
    """
    Create Instagram-ready match summary (1080x1080).
    
    Args:
        events: Match events DataFrame
        match_info: Match metadata Series
        filename: Output filename
    """
    home_team = match_info['home_team']
    away_team = match_info['away_team']
    home_score = int(match_info['home_score'])
    away_score = int(match_info['away_score'])
    
    # Calculate stats from data
    home_events = events[events['team_name'] == home_team]
    away_events = events[events['team_name'] == away_team]
    
    home_shots = len(home_events[home_events['type_name'] == 'Shot'])
    away_shots = len(away_events[away_events['type_name'] == 'Shot'])
    
    home_passes = len(home_events[home_events['type_name'] == 'Pass'])
    away_passes = len(away_events[away_events['type_name'] == 'Pass'])
    
    home_xg = calculate_xg(get_shots(events, home_team))
    away_xg = calculate_xg(get_shots(events, away_team))
    
    # Create square figure
    fig, ax = plt.subplots(figsize=(10, 10), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 92, 'MATCH SUMMARY', fontsize=14, color=COLORS['text_secondary'],
            ha='center', fontweight='bold')
    
    # Teams and score
    ax.text(25, 78, home_team.upper(), fontsize=18, color=COLORS['cyan'],
            ha='center', fontweight='bold')
    ax.text(75, 78, away_team.upper(), fontsize=18, color=COLORS['magenta'],
            ha='center', fontweight='bold')
    
    ax.text(50, 70, f"{home_score} - {away_score}", fontsize=36, color=COLORS['gold'],
            ha='center', fontweight='bold')
    
    # Stats
    stats = [
        ('Shots', home_shots, away_shots),
        ('Passes', home_passes, away_passes),
        ('xG', f"{home_xg:.2f}", f"{away_xg:.2f}"),
    ]
    
    y_pos = 50
    for stat_name, home_val, away_val in stats:
        ax.text(25, y_pos, str(home_val), fontsize=16, color=COLORS['text'],
                ha='center', fontweight='bold')
        ax.text(50, y_pos, stat_name, fontsize=12, color=COLORS['text_secondary'],
                ha='center')
        ax.text(75, y_pos, str(away_val), fontsize=16, color=COLORS['text'],
                ha='center', fontweight='bold')
        y_pos -= 12
    
    # Goals
    goals = get_goals(events)
    ax.text(50, 15, 'GOALSCORERS', fontsize=10, color=COLORS['text_secondary'],
            ha='center', fontweight='bold')
    
    home_goals = goals[goals['team_name'] == home_team]
    away_goals = goals[goals['team_name'] == away_team]
    
    home_scorers = ', '.join([f"{get_player_name(g['player_name'])} {int(g['minute'])}'" 
                              for _, g in home_goals.iterrows()])
    away_scorers = ', '.join([f"{get_player_name(g['player_name'])} {int(g['minute'])}'" 
                              for _, g in away_goals.iterrows()])
    
    ax.text(25, 8, home_scorers[:40] if len(home_scorers) > 40 else home_scorers,
            fontsize=8, color=COLORS['cyan'], ha='center', wrap=True)
    ax.text(75, 8, away_scorers[:40] if len(away_scorers) > 40 else away_scorers,
            fontsize=8, color=COLORS['magenta'], ha='center', wrap=True)
    
    # Watermark
    ax.text(95, 2, 'DIVISION FC', fontsize=8, color=COLORS['cyan'], alpha=0.7, ha='right')
    
    plt.tight_layout()
    
    # Save
    filepath = IMAGES_DIR / filename
    fig.savefig(filepath, dpi=VIZ_CONFIG['dpi'], bbox_inches='tight',
                facecolor=COLORS['background'])
    plt.close(fig)
    print(f"   ✅ Saved: {filepath}")


# =============================================================================
# ANIMATION FUNCTIONS
# =============================================================================

def create_goal_animation(events, goal_minute, team_name, filename, num_events=10):
    """
    Create goal buildup animation showing player positions and names.
    
    Args:
        events: Match events DataFrame
        goal_minute: Minute of the goal
        team_name: Scoring team name
        filename: Output filename
        num_events: Number of buildup events to show
    """
    import matplotlib.animation as animation
    
    # Get events leading up to goal
    goal_events = events[
        (events['minute'] <= goal_minute) &
        (events['minute'] >= goal_minute - 2)
    ].sort_values(['minute', 'second']).tail(num_events)
    
    if len(goal_events) == 0:
        print(f"⚠️ No events found for goal at {goal_minute}'")
        return
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color=COLORS['background'],
        line_color=COLORS['pitch_line'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Title
    title = ax.text(60, 86, f"GOAL - {goal_minute}'", fontsize=20, fontweight='bold',
                   color=COLORS['gold'], ha='center')
    
    # Initialize scatter plots
    home_scatter = ax.scatter([], [], s=300, c=COLORS['cyan'], edgecolors='white',
                              linewidths=2, zorder=10, label=get_home_team())
    away_scatter = ax.scatter([], [], s=300, c=COLORS['magenta'], edgecolors='white',
                              linewidths=2, zorder=10, label=get_away_team())
    ball_scatter = ax.scatter([], [], s=150, c=COLORS['gold'], marker='o',
                              edgecolors='white', linewidths=2, zorder=15)
    
    # Player name annotations (will be updated)
    player_texts = []
    
    def init():
        home_scatter.set_offsets(np.empty((0, 2)))
        away_scatter.set_offsets(np.empty((0, 2)))
        ball_scatter.set_offsets(np.empty((0, 2)))
        return [home_scatter, away_scatter, ball_scatter]
    
    def animate(frame):
        # Clear previous text annotations
        for txt in player_texts:
            txt.remove()
        player_texts.clear()
        
        # Get current event
        if frame >= len(goal_events):
            return [home_scatter, away_scatter, ball_scatter]
        
        current_event = goal_events.iloc[frame]
        
        # Update title
        event_type = current_event['type_name']
        player = get_player_name(current_event['player_name']) if pd.notna(current_event['player_name']) else ''
        minute = int(current_event['minute'])
        title.set_text(f"{event_type} - {player} ({minute}')")
        
        # Ball position
        if pd.notna(current_event['x']) and pd.notna(current_event['y']):
            ball_scatter.set_offsets([[current_event['x'], current_event['y']]])
        
        # Get freeze frame data if available (for player positions)
        # For now, show the event location with player info
        home_team = get_home_team()
        away_team = get_away_team()
        
        team = current_event['team_name']
        color = COLORS['cyan'] if team == home_team else COLORS['magenta']
        
        if pd.notna(current_event['x']) and pd.notna(current_event['y']):
            # Add player name annotation
            txt = ax.text(current_event['x'], current_event['y'] + 4,
                         get_player_name(current_event['player_name']),
                         fontsize=9, color=color, ha='center', fontweight='bold')
            player_texts.append(txt)
        
        return [home_scatter, away_scatter, ball_scatter, title]
    
    # Create animation
    anim = animation.FuncAnimation(
        fig, animate, init_func=init,
        frames=len(goal_events) + 3,  # Extra frames at end
        interval=800,
        blit=False
    )
    
    # Add legend
    ax.legend(loc='upper right', facecolor=COLORS['background'],
              edgecolor=COLORS['text_secondary'], labelcolor=COLORS['text'])
    
    # Watermark
    ax.text(118, -4, 'DIVISION FC', fontsize=8, color=COLORS['cyan'], alpha=0.7, ha='right')
    
    # Save
    filepath = GIFS_DIR / filename
    writer = animation.PillowWriter(fps=2)
    anim.save(str(filepath), writer=writer, dpi=150)
    plt.close(fig)
    print(f"   ✅ Saved: {filepath}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 60)
    print("⚽ DIVISION FC - MATCH ANALYSIS")
    print("=" * 60)
    
    # Load match data (from config - single source of truth)
    print("\n📊 Loading match data...")
    events, match_info = get_match_data()
    
    home_team = get_home_team()
    away_team = get_away_team()
    
    # Show goals
    print("\n⚽ Goals:")
    goals = get_goals(events)
    for _, goal in goals.iterrows():
        player = get_player_name(goal['player_name'])
        minute = int(goal['minute'])
        team = goal['team_name']
        print(f"   {minute}' - {player} ({team})")
    
    # Get top players from data
    print("\n🎯 Top Shooters:")
    home_shooters = get_top_players_by_stat(events, home_team, stat='shots', n=2)
    away_shooters = get_top_players_by_stat(events, away_team, stat='shots', n=2)
    
    print(f"   {home_team}: {[get_player_name(p) for p in home_shooters]}")
    print(f"   {away_team}: {[get_player_name(p) for p in away_shooters]}")
    
    # Generate visualizations
    print("\n🎨 Creating visualizations...")
    
    # Shot maps for top shooters
    print("\n   📍 Shot Maps:")
    for player in home_shooters[:1]:
        create_shot_map(events, player, f"{get_clean_filename(player)}_shots.png")
    for player in away_shooters[:1]:
        create_shot_map(events, player, f"{get_clean_filename(player)}_shots.png")
    
    # Heatmaps
    print("\n   🔥 Heatmaps:")
    for player in home_shooters[:1]:
        create_touch_heatmap(events, player, f"{get_clean_filename(player)}_heatmap.png")
    for player in away_shooters[:1]:
        create_touch_heatmap(events, player, f"{get_clean_filename(player)}_heatmap.png")
    
    # Pass networks
    print("\n   🔗 Pass Networks:")
    create_pass_network(events, home_team, f"{get_clean_filename(home_team)}_passes.png")
    create_pass_network(events, away_team, f"{get_clean_filename(away_team)}_passes.png")
    
    # Zone control
    print("\n   📊 Zone Control:")
    create_zone_control(events, home_team, away_team, "zone_control.png")
    
    # Match summary
    print("\n   📱 Match Summary:")
    create_match_summary(events, match_info, "match_summary.png")
    
    # Animations
    print("\n🎬 Creating animations...")
    home_goals = goals[goals['team_name'] == home_team]
    away_goals = goals[goals['team_name'] == away_team]
    
    if len(home_goals) > 0:
        first_home_goal = int(home_goals.iloc[0]['minute'])
        create_goal_animation(events, first_home_goal, home_team,
                            f"{get_clean_filename(home_team)}_goal.gif")
    
    if len(away_goals) > 0:
        first_away_goal = int(away_goals.iloc[0]['minute'])
        create_goal_animation(events, first_away_goal, away_team,
                            f"{get_clean_filename(away_team)}_goal.gif")
    
    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Output files saved to:")
    print(f"   Images: {IMAGES_DIR}")
    print(f"   GIFs:   {GIFS_DIR}")


if __name__ == "__main__":
    main()

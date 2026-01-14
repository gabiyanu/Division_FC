#!/usr/bin/env python3
"""
Division FC - Instagram Export Example
=======================================

Complete workflow from data loading to Instagram-ready exports.
All data is dynamically sourced from StatsBomb API.

Usage:
    python examples/instagram_export.py

Output:
    - output/images/instagram_post.png (1080x1080)
    - output/images/instagram_story.png (1080x1920)
    - Suggested caption printed to console

Author: Division FC
Data Source: StatsBomb Open Data (CC BY 4.0)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import VerticalPitch, Sbopen

# Import our modules
from src.data.loader import (
    StatsBombLoader, 
    get_top_players_by_stat, 
    get_goals,
    get_shots,
    calculate_xg
)
from src.export.instagram import InstagramExporter


# ============================================================================
# CONFIGURATION
# ============================================================================

OUTPUT_DIR = project_root / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Brand colors
COLORS = {
    'background': '#0D1117',
    'cyan': '#00FFCC',
    'magenta': '#FF66B2',
    'purple': '#AA66FF',
    'gold': '#FFD700',
    'text': '#F0F6FC',
    'text_secondary': '#8B949E',
}

# Instagram handle (customize this)
INSTAGRAM_HANDLE = '@divisionfc'


# ============================================================================
# HASHTAG LIBRARY
# ============================================================================

HASHTAGS = {
    'base': '#football #soccer #dataviz #socceranalytics #footballanalytics',
    'worldcup': '#worldcup #fifaworldcup #qatar2022',
    'ucl': '#ucl #championsleague #uefachampionsleague',
    'shotmap': '#shotmap #xg #expectedgoals #finishing',
    'heatmap': '#heatmap #touches #movement',
    'passmap': '#passmap #passing #buildup',
}


def get_hashtag_string(viz_type='shotmap', competition='worldcup'):
    """Generate hashtag string for caption."""
    tags = [
        HASHTAGS['base'],
        HASHTAGS.get(competition, ''),
        HASHTAGS.get(viz_type, ''),
    ]
    return ' '.join(filter(None, tags))


# ============================================================================
# VISUALIZATION CREATION
# ============================================================================

def create_shot_map_figure(events, player_name, match_info):
    """
    Create a shot map figure ready for Instagram export.
    
    All data is sourced from the events DataFrame.
    """
    # Filter shots for player (from data)
    shots = events[
        (events['type_name'] == 'Shot') &
        (events['player_name'] == player_name)
    ].copy()
    
    # Calculate stats from data
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
        line_color=COLORS['text_secondary'],
        linewidth=1
    )
    pitch.draw(ax=ax)
    
    # Plot shots
    for idx, shot in shots.iterrows():
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
    
    # Title (player name from data)
    short_name = player_name.split()[-1]
    ax.text(
        40, 125, short_name.upper(),
        fontsize=32, fontweight='bold',
        color=COLORS['text'],
        ha='center'
    )
    
    # Subtitle (competition from data)
    competition = match_info.get('competition', 'Match')
    stage = match_info.get('competition_stage', '')
    subtitle = f"{competition} {stage}".strip()
    ax.text(
        40, 121, subtitle.upper(),
        fontsize=12,
        color=COLORS['text_secondary'],
        ha='center'
    )
    
    # Stats box (calculated from data)
    stats_text = f"Shots: {total_shots}  •  Goals: {goals}  •  xG: {total_xg:.2f}"
    ax.text(
        40, 4, stats_text,
        fontsize=11, fontweight='bold',
        color=COLORS['cyan'],
        ha='center',
        bbox=dict(
            boxstyle='round,pad=0.5',
            facecolor=COLORS['background'],
            edgecolor=COLORS['cyan'],
            alpha=0.9
        )
    )
    
    # Legend
    ax.scatter([], [], s=100, c=COLORS['cyan'], marker='o', label='Shot')
    ax.scatter([], [], s=300, c=COLORS['gold'], marker='*', label='Goal')
    ax.legend(
        loc='upper right',
        facecolor=COLORS['background'],
        edgecolor=COLORS['text_secondary'],
        labelcolor=COLORS['text'],
        fontsize=9
    )
    
    plt.tight_layout()
    return fig, {'shots': total_shots, 'goals': goals, 'xg': total_xg, 'player': short_name}


# ============================================================================
# CAPTION GENERATION
# ============================================================================

def generate_caption(stats, match_info, viz_type='shotmap'):
    """
    Generate Instagram caption with data-sourced information.
    """
    player = stats['player']
    shots = stats['shots']
    goals = stats['goals']
    xg = stats['xg']
    
    home_team = match_info['home_team']
    away_team = match_info['away_team']
    competition = match_info.get('competition', 'Match')
    stage = match_info.get('competition_stage', '')
    
    # Build caption
    caption = f"""🎯 {player.upper()} SHOT MAP

{competition} {stage}: {home_team} vs {away_team}

📊 {shots} shots • {goals} goals • {xg:.2f} xG

Data: StatsBomb
Viz: Division FC

{get_hashtag_string(viz_type, 'worldcup')}
#{player.lower()} #{home_team.lower().replace(' ', '')}"""
    
    return caption


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def main():
    """Complete Instagram export workflow."""
    
    print("=" * 60)
    print("📱 DIVISION FC - INSTAGRAM EXPORT")
    print("=" * 60)
    
    # -------------------------------------------------------------------------
    # 1. LOAD DATA (all dynamically sourced)
    # -------------------------------------------------------------------------
    print("\n📊 Loading data from StatsBomb API...")
    
    loader = StatsBombLoader()
    events, match_info = loader.load_match_by_criteria(
        competition_name="World Cup",
        stage="Final"
    )
    
    # Extract info from data
    home_team = match_info['home_team']
    away_team = match_info['away_team']
    
    print(f"   ✅ Loaded: {home_team} vs {away_team}")
    
    # -------------------------------------------------------------------------
    # 2. SELECT PLAYER (from data)
    # -------------------------------------------------------------------------
    print("\n🎯 Finding top shooter from data...")
    
    top_shooters = get_top_players_by_stat(events, home_team, stat='shots', n=1)
    
    if not top_shooters:
        print("   ⚠️ No shooters found, exiting")
        return
    
    player_name = top_shooters[0]
    print(f"   ✅ Selected: {player_name.split()[-1]}")
    
    # -------------------------------------------------------------------------
    # 3. CREATE VISUALIZATION
    # -------------------------------------------------------------------------
    print("\n🎨 Creating visualization...")
    
    fig, stats = create_shot_map_figure(events, player_name, match_info)
    print(f"   ✅ Shot map created")
    
    # -------------------------------------------------------------------------
    # 4. EXPORT FOR INSTAGRAM
    # -------------------------------------------------------------------------
    print("\n📱 Exporting for Instagram...")
    
    exporter = InstagramExporter(output_dir=str(OUTPUT_DIR))
    
    # Save raw figure first
    raw_path = IMAGES_DIR / 'shot_map_raw.png'
    fig.savefig(raw_path, dpi=150, bbox_inches='tight', facecolor=COLORS['background'])
    plt.close(fig)
    
    # Export as Instagram post (1080x1080)
    from PIL import Image
    img = Image.open(raw_path)
    
    # Square post
    post_img = exporter._resize_with_padding(img, (1080, 1080), COLORS['background'])
    post_img = exporter._add_watermark(post_img, INSTAGRAM_HANDLE)
    post_path = IMAGES_DIR / 'instagram_post.png'
    post_img.save(post_path, 'PNG', quality=95)
    print(f"   ✅ Post: {post_path}")
    
    # Story (1080x1920)
    story_img = exporter._resize_with_padding(img, (1080, 1920), COLORS['background'])
    story_img = exporter._add_watermark(story_img, INSTAGRAM_HANDLE, position='bottom')
    story_path = IMAGES_DIR / 'instagram_story.png'
    story_img.save(story_path, 'PNG', quality=95)
    print(f"   ✅ Story: {story_path}")
    
    # Clean up raw
    raw_path.unlink()
    
    # -------------------------------------------------------------------------
    # 5. GENERATE CAPTION
    # -------------------------------------------------------------------------
    caption = generate_caption(stats, match_info)
    
    # -------------------------------------------------------------------------
    # 6. PRINT RESULTS
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("✅ INSTAGRAM EXPORT COMPLETE!")
    print("=" * 60)
    
    print(f"\n📸 FILES READY:")
    print(f"   Post (1080x1080): {post_path}")
    print(f"   Story (1080x1920): {story_path}")
    
    print(f"\n📝 SUGGESTED CAPTION:")
    print("-" * 40)
    print(caption)
    print("-" * 40)
    
    print(f"\n🚀 NEXT STEPS:")
    print("   1. Transfer images to your phone")
    print("   2. Open Instagram app")
    print("   3. Create new post → select instagram_post.png")
    print("   4. Copy/paste the caption above")
    print("   5. Post! 🎉")
    
    print(f"\n📖 For more options, see: docs/INSTAGRAM_GUIDE.md")
    
    return {
        'post_path': str(post_path),
        'story_path': str(story_path),
        'caption': caption
    }


if __name__ == "__main__":
    main()

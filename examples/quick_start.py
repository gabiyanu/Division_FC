#!/usr/bin/env python3
"""
Division FC - Quick Start Example
==================================

A minimal example to get you started with Division FC analytics.
All data is dynamically sourced from StatsBomb API - nothing is hardcoded.

Usage:
    python examples/quick_start.py

Author: Division FC
Data Source: StatsBomb Open Data (CC BY 4.0)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mplsoccer import Sbopen
import matplotlib.pyplot as plt

# Brand colors
CYAN = '#00FFCC'
MAGENTA = '#FF66B2'
BACKGROUND = '#0D1117'


def get_world_cup_final(parser):
    """
    Dynamically find the World Cup final match.
    All values sourced from API, nothing hardcoded.
    
    Returns:
        tuple: (match_id, match_info)
    """
    # Get all competitions
    competitions = parser.competition()
    
    # Find FIFA World Cup
    wc = competitions[
        competitions['competition_name'].str.contains('World Cup', case=False, na=False) &
        ~competitions['competition_name'].str.contains('Women', case=False, na=False)
    ]
    
    if len(wc) == 0:
        raise ValueError("World Cup competition not found")
    
    # Get most recent season
    wc = wc.sort_values('season_id', ascending=False).iloc[0]
    competition_id = int(wc['competition_id'])
    season_id = int(wc['season_id'])
    
    print(f"   Found: {wc['competition_name']} ({wc['season_name']})")
    
    # Get matches
    matches = parser.match(competition_id, season_id)
    
    # Find final
    if 'competition_stage' in matches.columns:
        final = matches[
            matches['competition_stage'].str.contains('Final', case=False, na=False) &
            ~matches['competition_stage'].str.contains('Semi|Quarter|Third', case=False, na=False)
        ]
        if len(final) > 0:
            match_info = final.iloc[0]
            return int(match_info['match_id']), match_info
    
    # Fallback: last match by date
    matches = matches.sort_values('match_date', ascending=False)
    match_info = matches.iloc[0]
    return int(match_info['match_id']), match_info


def main():
    print("⚽ Division FC - Quick Start")
    print("=" * 40)
    print("\n📊 Loading data from StatsBomb API...")
    
    parser = Sbopen()
    
    # 1. Dynamically find World Cup Final
    print("\n🔍 Finding World Cup Final...")
    match_id, match_info = get_world_cup_final(parser)
    
    # 2. Load Events
    print(f"\n📥 Loading match events (ID: {match_id})...")
    events, related, freeze, tactics = parser.event(match_id)
    print(f"   Loaded {len(events)} events")
    
    # 3. Extract info from data (not hardcoded)
    home_team = match_info['home_team']
    away_team = match_info['away_team']
    home_score = int(match_info['home_score'])
    away_score = int(match_info['away_score'])
    match_date = match_info['match_date']
    
    print(f"\n📋 Match Info (from data):")
    print(f"   {home_team} {home_score} - {away_score} {away_team}")
    print(f"   Date: {match_date}")
    
    # 4. Quick Stats - calculated from data
    print("\n📈 Quick Stats (calculated from events):")
    shots = events[events['type_name'] == 'Shot']
    goals = shots[shots['outcome_name'] == 'Goal']
    passes = events[events['type_name'] == 'Pass']
    
    print(f"   Total shots: {len(shots)}")
    print(f"   Total goals: {len(goals)}")
    print(f"   Total passes: {len(passes)}")
    
    # 5. Show goalscorers - extracted from data
    print("\n⚽ Goalscorers (from event data):")
    for _, goal in goals.iterrows():
        player = goal['player_name'].split()[-1]
        minute = int(goal['minute'])
        team = goal['team_name']
        print(f"   {minute}' - {player} ({team})")
    
    # 6. Top players by shots - from data
    print("\n🎯 Top Shooters (from data):")
    shot_counts = shots.groupby(['player_name', 'team_name']).size().sort_values(ascending=False)
    for (player, team), count in shot_counts.head(3).items():
        short_name = player.split()[-1]
        print(f"   {short_name} ({team}): {count} shots")
    
    print("\n✅ Quick start complete!")
    print("   All data dynamically sourced from StatsBomb API")
    print("   Run world_cup_analysis.py for full visualizations")


if __name__ == "__main__":
    main()

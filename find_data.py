#!/usr/bin/env python3
"""
Division FC - Data Explorer
============================

Utility script to find available competitions, seasons, stages, and teams.
Run this to discover what data is available before configuring your analysis.

Usage:
    python find_data.py                    # Show all options
    python find_data.py --competitions     # List competitions only
    python find_data.py --matches "World Cup" "2022"  # List matches in competition
    python find_data.py --teams "World Cup" "2022"    # List teams in competition

Author: Division FC
Data Source: StatsBomb Open Data (CC BY 4.0)
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from mplsoccer import Sbopen
import pandas as pd


def get_all_competitions():
    """
    Get all available competitions with seasons.
    
    Returns:
        DataFrame with competition_id, competition_name, season_id, season_name
    """
    parser = Sbopen()
    comps = parser.competition()
    return comps[['competition_id', 'competition_name', 'season_id', 'season_name']].sort_values(
        ['competition_name', 'season_name']
    )


def get_matches(competition_name: str, season: str = None):
    """
    Get all matches for a competition/season.
    
    Args:
        competition_name: Competition name (partial match)
        season: Season year (optional)
    
    Returns:
        DataFrame with match details
    """
    parser = Sbopen()
    comps = parser.competition()
    
    # Filter by competition name
    filtered = comps[comps['competition_name'].str.contains(competition_name, case=False, na=False)]
    
    # Exclude youth competitions
    filtered = filtered[~filtered['competition_name'].str.contains('U20|U17|U21|U19|Women|Youth', case=False, na=False)]
    
    if season:
        filtered = filtered[filtered['season_name'].str.contains(str(season), case=False, na=False)]
    
    if len(filtered) == 0:
        print(f"❌ No competition found matching '{competition_name}'")
        return None
    
    # Get first matching competition
    comp = filtered.sort_values('season_id', ascending=False).iloc[0]
    comp_id = int(comp['competition_id'])
    season_id = int(comp['season_id'])
    
    print(f"📊 Found: {comp['competition_name']} ({comp['season_name']})")
    print(f"   Competition ID: {comp_id}, Season ID: {season_id}")
    
    # Get matches
    matches = parser.match(comp_id, season_id)
    
    # Find column names
    home_col = 'home_team_name' if 'home_team_name' in matches.columns else 'home_team'
    away_col = 'away_team_name' if 'away_team_name' in matches.columns else 'away_team'
    stage_col = 'competition_stage_name' if 'competition_stage_name' in matches.columns else 'competition_stage'
    
    # Select relevant columns
    cols = ['match_id', 'match_date', home_col, away_col, 'home_score', 'away_score']
    if stage_col in matches.columns:
        cols.append(stage_col)
    
    return matches[cols].sort_values('match_date')


def get_teams(competition_name: str, season: str = None):
    """
    Get all teams in a competition/season.
    
    Args:
        competition_name: Competition name (partial match)
        season: Season year (optional)
    
    Returns:
        List of team names
    """
    matches = get_matches(competition_name, season)
    if matches is None:
        return []
    
    home_col = 'home_team_name' if 'home_team_name' in matches.columns else 'home_team'
    away_col = 'away_team_name' if 'away_team_name' in matches.columns else 'away_team'
    
    teams = set(matches[home_col].unique()) | set(matches[away_col].unique())
    return sorted(teams)


def get_stages(competition_name: str, season: str = None):
    """
    Get all stages in a competition/season.
    
    Args:
        competition_name: Competition name (partial match)
        season: Season year (optional)
    
    Returns:
        List of stage names
    """
    matches = get_matches(competition_name, season)
    if matches is None:
        return []
    
    stage_col = 'competition_stage_name' if 'competition_stage_name' in matches.columns else 'competition_stage'
    
    if stage_col in matches.columns:
        return sorted(matches[stage_col].dropna().unique())
    return []


def print_competitions():
    """Print all available competitions."""
    print("\n" + "=" * 70)
    print("📋 AVAILABLE COMPETITIONS")
    print("=" * 70)
    
    comps = get_all_competitions()
    
    # Group by competition
    for comp_name in comps['competition_name'].unique():
        comp_data = comps[comps['competition_name'] == comp_name]
        seasons = comp_data['season_name'].tolist()
        comp_id = comp_data['competition_id'].iloc[0]
        
        print(f"\n🏆 {comp_name} (ID: {comp_id})")
        print(f"   Seasons: {', '.join(seasons)}")


def print_matches(competition_name: str, season: str = None):
    """Print all matches for a competition."""
    print("\n" + "=" * 70)
    print(f"⚽ MATCHES: {competition_name}" + (f" ({season})" if season else ""))
    print("=" * 70)
    
    matches = get_matches(competition_name, season)
    if matches is None:
        return
    
    home_col = 'home_team_name' if 'home_team_name' in matches.columns else 'home_team'
    away_col = 'away_team_name' if 'away_team_name' in matches.columns else 'away_team'
    stage_col = 'competition_stage_name' if 'competition_stage_name' in matches.columns else 'competition_stage'
    
    print(f"\n{'ID':<10} {'Date':<12} {'Stage':<20} {'Match':<40} {'Score':<6}")
    print("-" * 90)
    
    for _, match in matches.iterrows():
        match_id = int(match['match_id'])
        date = str(match['match_date'])[:10]
        stage = match.get(stage_col, 'N/A')[:18] if stage_col in match.index else 'N/A'
        home = match[home_col][:15]
        away = match[away_col][:15]
        home_score = int(match['home_score']) if pd.notna(match['home_score']) else 0
        away_score = int(match['away_score']) if pd.notna(match['away_score']) else 0
        
        print(f"{match_id:<10} {date:<12} {stage:<20} {home} vs {away:<15} {home_score}-{away_score}")


def print_teams(competition_name: str, season: str = None):
    """Print all teams in a competition."""
    print("\n" + "=" * 70)
    print(f"👕 TEAMS: {competition_name}" + (f" ({season})" if season else ""))
    print("=" * 70)
    
    teams = get_teams(competition_name, season)
    if not teams:
        return
    
    print(f"\nFound {len(teams)} teams:\n")
    for i, team in enumerate(teams, 1):
        print(f"   {i:2}. {team}")


def print_stages(competition_name: str, season: str = None):
    """Print all stages in a competition."""
    print("\n" + "=" * 70)
    print(f"🏟️ STAGES: {competition_name}" + (f" ({season})" if season else ""))
    print("=" * 70)
    
    stages = get_stages(competition_name, season)
    if not stages:
        print("\nNo stages found (might be a league format)")
        return
    
    print(f"\nFound {len(stages)} stages:\n")
    for i, stage in enumerate(stages, 1):
        print(f"   {i:2}. {stage}")


def print_all():
    """Print everything available."""
    print_competitions()
    
    print("\n\n" + "=" * 70)
    print("💡 TIP: To see matches for a specific competition, run:")
    print("   python find_data.py --matches \"FIFA World Cup\" \"2022\"")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description='Explore available StatsBomb data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python find_data.py                           # Show all competitions
  python find_data.py --matches "World Cup" "2022"    # List World Cup 2022 matches
  python find_data.py --teams "La Liga" "2020"        # List La Liga 2020 teams
  python find_data.py --stages "Champions" "2019"     # List UCL 2019 stages
        """
    )
    
    parser.add_argument('--competitions', '-c', action='store_true',
                        help='List all available competitions')
    parser.add_argument('--matches', '-m', nargs='+', metavar=('COMP', 'SEASON'),
                        help='List matches for competition (optionally with season)')
    parser.add_argument('--teams', '-t', nargs='+', metavar=('COMP', 'SEASON'),
                        help='List teams in competition')
    parser.add_argument('--stages', '-s', nargs='+', metavar=('COMP', 'SEASON'),
                        help='List stages in competition')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Show everything for a competition')
    
    args = parser.parse_args()
    
    print("\n⚽ DIVISION FC - DATA EXPLORER")
    print("=" * 70)
    
    if args.matches:
        comp = args.matches[0]
        season = args.matches[1] if len(args.matches) > 1 else None
        print_matches(comp, season)
    elif args.teams:
        comp = args.teams[0]
        season = args.teams[1] if len(args.teams) > 1 else None
        print_teams(comp, season)
    elif args.stages:
        comp = args.stages[0]
        season = args.stages[1] if len(args.stages) > 1 else None
        print_stages(comp, season)
    elif args.all and len(sys.argv) > 2:
        comp = sys.argv[-2] if len(sys.argv) > 3 else sys.argv[-1]
        season = sys.argv[-1] if len(sys.argv) > 3 else None
        print_matches(comp, season)
        print_teams(comp, season)
        print_stages(comp, season)
    else:
        print_all()


if __name__ == "__main__":
    main()

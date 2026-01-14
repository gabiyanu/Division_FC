"""
Data Loading Module for StatsBomb Data

All functions dynamically source data from APIs - no hardcoded IDs.
Use the search/find functions to discover competitions, matches, and players.

Author: Division FC
Data Source: StatsBomb Open Data (CC BY 4.0)

Usage:
    from src.data.loader import StatsBombLoader
    
    loader = StatsBombLoader()
    
    # Find competition dynamically
    comp_id, season_id = loader.find_competition("World Cup")
    
    # Find final match
    final = loader.find_final(comp_id, season_id)
    
    # Load events
    events, info = loader.load_match_by_criteria(
        competition_name="World Cup",
        stage="Final"
    )
"""

import pandas as pd
from mplsoccer import Sbopen
from typing import Tuple, Optional, List, Dict, Any


class StatsBombLoader:
    """
    Loader for StatsBomb open data.
    All match/competition IDs are sourced dynamically from the API.
    No hardcoded values - everything is discovered from the data.
    """
    
    def __init__(self):
        """Initialize the StatsBomb parser."""
        self.parser = Sbopen()
        self._competitions = None
        self._matches_cache = {}
    
    # =========================================================================
    # COMPETITION DISCOVERY
    # =========================================================================
    
    @property
    def competitions(self) -> pd.DataFrame:
        """Get all available competitions (cached)."""
        if self._competitions is None:
            self._competitions = self.parser.competition()
        return self._competitions
    
    def list_competitions(self, search: Optional[str] = None) -> pd.DataFrame:
        """
        List all available competitions with their IDs.
        
        Args:
            search: Optional search string to filter competitions
        
        Returns:
            DataFrame with competition_id, competition_name, season_id, season_name
        """
        df = self.competitions[['competition_id', 'competition_name', 'season_id', 'season_name']]
        if search:
            df = df[df['competition_name'].str.contains(search, case=False, na=False)]
        return df
    
    def find_competition(
        self, 
        name: str, 
        season: Optional[str] = None,
        exclude_women: bool = False
    ) -> Tuple[int, int]:
        """
        Find competition and season IDs by name - NO hardcoding.
        
        Args:
            name: Competition name to search (partial match)
            season: Optional season name to filter (e.g., "2022")
            exclude_women: Exclude women's competitions
        
        Returns:
            Tuple of (competition_id, season_id)
        
        Example:
            comp_id, season_id = loader.find_competition("World Cup", "2022")
        """
        comps = self.competitions.copy()
        
        # Filter by name (partial match)
        comps = comps[comps['competition_name'].str.contains(name, case=False, na=False)]
        
        # Optionally exclude women's competitions
        if exclude_women:
            comps = comps[~comps['competition_name'].str.contains('Women', case=False, na=False)]
        
        # Filter by season if provided
        if season:
            comps = comps[comps['season_name'].str.contains(str(season), case=False, na=False)]
        
        if len(comps) == 0:
            available = self.list_competitions()['competition_name'].unique()
            raise ValueError(f"Competition '{name}' not found. Available: {list(available)[:10]}...")
        
        # Get most recent season
        comps = comps.sort_values('season_id', ascending=False)
        row = comps.iloc[0]
        
        return int(row['competition_id']), int(row['season_id'])
    
    # =========================================================================
    # MATCH DISCOVERY
    # =========================================================================
    
    def get_matches(
        self, 
        competition_id: int, 
        season_id: int
    ) -> pd.DataFrame:
        """
        Get all matches for a competition/season.
        
        Args:
            competition_id: Competition ID (from find_competition)
            season_id: Season ID (from find_competition)
        
        Returns:
            DataFrame of matches
        """
        cache_key = (competition_id, season_id)
        if cache_key not in self._matches_cache:
            self._matches_cache[cache_key] = self.parser.match(competition_id, season_id)
        return self._matches_cache[cache_key]
    
    def list_matches(
        self,
        competition_id: int,
        season_id: int,
        team: Optional[str] = None
    ) -> pd.DataFrame:
        """
        List matches with key info for browsing.
        
        Args:
            competition_id: Competition ID
            season_id: Season ID
            team: Optional team name to filter
        
        Returns:
            DataFrame with match_id, date, teams, score, stage
        """
        matches = self.get_matches(competition_id, season_id)
        
        if team:
            matches = matches[
                matches['home_team'].str.contains(team, case=False, na=False) |
                matches['away_team'].str.contains(team, case=False, na=False)
            ]
        
        cols = ['match_id', 'match_date', 'home_team', 'away_team', 'home_score', 'away_score']
        if 'competition_stage' in matches.columns:
            cols.append('competition_stage')
        
        return matches[cols]
    
    def find_match(
        self,
        competition_id: int,
        season_id: int,
        home_team: Optional[str] = None,
        away_team: Optional[str] = None,
        stage: Optional[str] = None,
        match_date: Optional[str] = None
    ) -> pd.Series:
        """
        Find a specific match by criteria - NO hardcoding.
        
        Args:
            competition_id: Competition ID
            season_id: Season ID
            home_team: Home team name (partial match)
            away_team: Away team name (partial match)
            stage: Competition stage (e.g., "Final", "Semi")
            match_date: Match date string (e.g., "2022-12-18")
        
        Returns:
            Match info Series with standardized column names
        
        Example:
            match = loader.find_match(comp_id, season_id, home_team="Argentina")
        """
        matches = self.get_matches(competition_id, season_id)
        
        # Find the team name column (mplsoccer uses 'home_team_name')
        home_col = self._find_column(matches, ['home_team_name', 'home_team'])
        away_col = self._find_column(matches, ['away_team_name', 'away_team'])
        stage_col = self._find_column(matches, ['competition_stage_name', 'competition_stage'])
        
        if home_team and home_col:
            matches = matches[matches[home_col].str.contains(home_team, case=False, na=False)]
        if away_team and away_col:
            matches = matches[matches[away_col].str.contains(away_team, case=False, na=False)]
        if stage and stage_col:
            matches = matches[matches[stage_col].str.contains(stage, case=False, na=False)]
        if match_date:
            matches = matches[matches['match_date'].astype(str).str.contains(match_date)]
        
        if len(matches) == 0:
            raise ValueError("No matches found with given criteria")
        
        return self._standardize_match_info(matches.iloc[0])
    
    def _find_column(self, df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
        """Find the first matching column name from candidates."""
        for col in candidates:
            if col in df.columns:
                return col
        return None
    
    def find_final(self, competition_id: int, season_id: int) -> pd.Series:
        """
        Find the final match of a competition - NO hardcoding.
        
        Args:
            competition_id: Competition ID
            season_id: Season ID
        
        Returns:
            Match info Series with standardized column names
        """
        matches = self.get_matches(competition_id, season_id)
        
        # Try to find by competition_stage
        if 'competition_stage_name' in matches.columns:
            final = matches[
                matches['competition_stage_name'].str.contains('Final', case=False, na=False) &
                ~matches['competition_stage_name'].str.contains('Semi|Quarter|Third', case=False, na=False)
            ]
            if len(final) > 0:
                return self._standardize_match_info(final.iloc[0])
        
        # Try alternate column name
        if 'competition_stage' in matches.columns:
            final = matches[
                matches['competition_stage'].str.contains('Final', case=False, na=False) &
                ~matches['competition_stage'].str.contains('Semi|Quarter|Third', case=False, na=False)
            ]
            if len(final) > 0:
                return self._standardize_match_info(final.iloc[0])
        
        # Fallback: last match by date
        matches = matches.sort_values('match_date', ascending=False)
        return self._standardize_match_info(matches.iloc[0])
    
    def _standardize_match_info(self, match_row: pd.Series) -> pd.Series:
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
        
        # Ensure essential columns exist
        if 'home_team' not in result.index:
            # Try to find any column containing team info
            for col in result.index:
                if 'home' in col.lower() and 'team' in col.lower() and 'name' in col.lower():
                    result['home_team'] = result[col]
                    break
                elif 'home' in col.lower() and 'team' in col.lower() and 'id' not in col.lower():
                    result['home_team'] = result[col]
                    break
        
        if 'away_team' not in result.index:
            for col in result.index:
                if 'away' in col.lower() and 'team' in col.lower() and 'name' in col.lower():
                    result['away_team'] = result[col]
                    break
                elif 'away' in col.lower() and 'team' in col.lower() and 'id' not in col.lower():
                    result['away_team'] = result[col]
                    break
        
        return result
    
    # =========================================================================
    # DATA LOADING
    # =========================================================================
    
    def load_events(self, match_id: int) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load all event data for a match.
        
        Args:
            match_id: Match ID (from find_match or find_final)
        
        Returns:
            Tuple of (events, related, freeze_frame, tactics) DataFrames
        """
        return self.parser.event(match_id)
    
    def load_match_by_criteria(
        self,
        competition_name: str,
        season: Optional[str] = None,
        stage: Optional[str] = None,
        home_team: Optional[str] = None,
        away_team: Optional[str] = None
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load match events by search criteria - fully dynamic, NO hardcoding.
        
        This is the recommended method for loading data.
        
        Args:
            competition_name: Competition name to search
            season: Optional season name (e.g., "2022")
            stage: Optional competition stage (e.g., "Final")
            home_team: Optional home team name
            away_team: Optional away team name
        
        Returns:
            Tuple of (events DataFrame, match_info Series)
        
        Examples:
            # Load World Cup Final
            events, info = loader.load_match_by_criteria(
                competition_name="World Cup",
                stage="Final"
            )
            
            # Load specific match
            events, info = loader.load_match_by_criteria(
                competition_name="La Liga",
                season="2020",
                home_team="Barcelona",
                away_team="Real Madrid"
            )
        """
        # Find competition
        comp_id, season_id = self.find_competition(competition_name, season)
        
        # Find match
        if stage:
            if stage.lower() == "final":
                match_info = self.find_final(comp_id, season_id)
            else:
                match_info = self.find_match(comp_id, season_id, home_team, away_team, stage)
        elif home_team or away_team:
            match_info = self.find_match(comp_id, season_id, home_team, away_team)
        else:
            # Default to final
            match_info = self.find_final(comp_id, season_id)
        
        # Load events
        match_id = int(match_info['match_id'])
        events, _, _, _ = self.load_events(match_id)
        
        return events, match_info


# =============================================================================
# UTILITY FUNCTIONS FOR DATA EXTRACTION
# =============================================================================

def get_teams(events: pd.DataFrame) -> List[str]:
    """Extract unique team names from events."""
    return events['team_name'].dropna().unique().tolist()


def get_players(events: pd.DataFrame, team: Optional[str] = None) -> List[str]:
    """Extract unique player names from events."""
    df = events.copy()
    if team:
        df = df[df['team_name'] == team]
    return df['player_name'].dropna().unique().tolist()


def get_goals(events: pd.DataFrame) -> pd.DataFrame:
    """Extract all goals from events - sourced from data."""
    return events[
        (events['type_name'] == 'Shot') &
        (events['outcome_name'] == 'Goal')
    ][['minute', 'second', 'player_name', 'team_name']].copy()


def get_shots(events: pd.DataFrame, team: Optional[str] = None) -> pd.DataFrame:
    """Extract shots from events."""
    df = events[events['type_name'] == 'Shot'].copy()
    if team:
        df = df[df['team_name'] == team]
    return df


def get_passes(
    events: pd.DataFrame, 
    team: Optional[str] = None, 
    successful_only: bool = False
) -> pd.DataFrame:
    """Extract passes from events."""
    df = events[events['type_name'] == 'Pass'].copy()
    if team:
        df = df[df['team_name'] == team]
    if successful_only:
        df = df[df['outcome_name'].isna()]
    return df


def calculate_xg(shots: pd.DataFrame) -> float:
    """Calculate total xG from shots DataFrame."""
    if 'shot_statsbomb_xg' in shots.columns:
        return shots['shot_statsbomb_xg'].sum()
    return 0.0


def calculate_possession(events: pd.DataFrame, team: str) -> float:
    """Calculate possession percentage from events."""
    teams = get_teams(events)
    if team not in teams:
        raise ValueError(f"Team '{team}' not found. Available: {teams}")
    
    team_events = len(events[events['team_name'] == team])
    total_events = len(events[events['team_name'].isin(teams)])
    
    return (team_events / total_events * 100) if total_events > 0 else 0.0


def get_top_players_by_stat(
    events: pd.DataFrame,
    team: str,
    stat: str = 'touches',
    n: int = 5
) -> List[str]:
    """
    Get top players by a statistic - dynamically from data.
    
    Args:
        events: Match events
        team: Team to filter
        stat: 'touches', 'shots', 'passes', 'goals', 'xg'
        n: Number of players to return
    
    Returns:
        List of player names
    """
    team_events = events[events['team_name'] == team]
    
    if stat == 'shots':
        counts = team_events[team_events['type_name'] == 'Shot'].groupby('player_name').size()
    elif stat == 'passes':
        counts = team_events[team_events['type_name'] == 'Pass'].groupby('player_name').size()
    elif stat == 'goals':
        goals = team_events[(team_events['type_name'] == 'Shot') & (team_events['outcome_name'] == 'Goal')]
        counts = goals.groupby('player_name').size()
    elif stat == 'xg':
        shots = team_events[team_events['type_name'] == 'Shot']
        if 'shot_statsbomb_xg' in shots.columns:
            counts = shots.groupby('player_name')['shot_statsbomb_xg'].sum()
        else:
            counts = pd.Series()
    else:  # touches
        counts = team_events[team_events['x'].notna()].groupby('player_name').size()
    
    if len(counts) == 0:
        return []
    
    return counts.nlargest(n).index.tolist()


def get_match_stats(events: pd.DataFrame, match_info: pd.Series) -> Dict[str, Any]:
    """
    Calculate comprehensive match statistics - all from data.
    
    Args:
        events: Match events DataFrame
        match_info: Match info Series
    
    Returns:
        Dictionary with all match statistics
    """
    home_team = match_info['home_team']
    away_team = match_info['away_team']
    
    home_events = events[events['team_name'] == home_team]
    away_events = events[events['team_name'] == away_team]
    
    home_shots = get_shots(events, home_team)
    away_shots = get_shots(events, away_team)
    
    return {
        'home_team': home_team,
        'away_team': away_team,
        'home_score': int(match_info['home_score']),
        'away_score': int(match_info['away_score']),
        'match_date': str(match_info['match_date']),
        'home_shots': len(home_shots),
        'away_shots': len(away_shots),
        'home_xg': calculate_xg(home_shots),
        'away_xg': calculate_xg(away_shots),
        'home_passes': len(get_passes(events, home_team)),
        'away_passes': len(get_passes(events, away_team)),
        'home_possession': calculate_possession(events, home_team),
        'away_possession': calculate_possession(events, away_team),
        'total_events': len(events),
        'goals': get_goals(events).to_dict('records'),
    }

"""
Race Analyzer for RaceStory Pro
Core analysis engine for race progression, overtakes, and key moments.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RaceAnalyzer:
    """Analyze race progression and key moments."""
    
    def __init__(self):
        """Initialize Race Analyzer."""
        pass
    
    def analyze_race_progression(self, results_df: pd.DataFrame, 
                                 lap_chart_df: Optional[pd.DataFrame] = None) -> Dict:
        """
        Analyze race progression from start to finish.
        
        Args:
            results_df: DataFrame with final race results
            lap_chart_df: Optional DataFrame with lap-by-lap positions
            
        Returns:
            Dictionary with race progression analysis
        """
        analysis = {
            'total_finishers': 0,
            'total_classified': 0,
            'dnf_count': 0,
            'average_laps': 0,
            'position_changes': []
        }
        
        if results_df.empty:
            return analysis
        
        # Basic statistics
        analysis['total_finishers'] = len(results_df)
        analysis['total_classified'] = len(results_df[results_df['STATUS'] == 'Classified'])
        analysis['dnf_count'] = analysis['total_finishers'] - analysis['total_classified']
        
        if 'LAPS' in results_df.columns:
            analysis['average_laps'] = results_df['LAPS'].mean()
        
        logger.info(f"Race analysis: {analysis['total_classified']} classified finishers")
        return analysis
    
    def identify_key_battles(self, results_df: pd.DataFrame, 
                            gap_threshold: float = 5.0) -> List[Dict]:
        """
        Identify close battles based on final gaps.
        
        Args:
            results_df: DataFrame with race results
            gap_threshold: Maximum gap in seconds to consider a battle
            
        Returns:
            List of battle information
        """
        battles = []
        
        if results_df.empty or 'GAP_PREV' not in results_df.columns:
            return battles
        
        for idx, row in results_df.iterrows():
            if idx == 0:  # Skip leader
                continue
                
            try:
                # Parse gap (format: "+X.XXX")
                gap_str = str(row.get('GAP_PREV', ''))
                if gap_str.startswith('+'):
                    gap = float(gap_str[1:])
                    
                    if gap <= gap_threshold:
                        driver_name = row.get('DRIVER', '')
                        if not driver_name:
                            driver_name = f"{row.get('DRIVER_FIRST', '')} {row.get('DRIVER_LAST', '')}".strip()
                        
                        battle = {
                            'position': row.get('POSITION', idx + 1),
                            'driver': driver_name or 'Unknown',
                            'car_number': row.get('NUMBER', 'N/A'),
                            'gap': gap,
                            'classification': 'Close Battle'
                        }
                        battles.append(battle)
                        
            except (ValueError, TypeError):
                continue
        
        logger.info(f"Identified {len(battles)} close battles")
        return battles
    
    def analyze_fastest_laps(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze fastest lap times and identify top performers.
        
        Args:
            results_df: DataFrame with race results
            
        Returns:
            DataFrame sorted by fastest lap time
        """
        if results_df.empty or 'FL_TIME' not in results_df.columns:
            return pd.DataFrame()
        
        # Create fastest lap analysis
        fl_df = results_df[[
            'POSITION', 'NUMBER', 'DRIVER_FIRSTNAME', 'DRIVER_SECONDNAME',
            'FL_TIME', 'FL_LAPNUM', 'FL_KPH', 'TEAM'
        ]].copy()
        
        # Sort by fastest lap time
        fl_df = fl_df.sort_values('FL_TIME')
        fl_df['FL_RANK'] = range(1, len(fl_df) + 1)
        
        logger.info(f"Analyzed fastest laps for {len(fl_df)} drivers")
        return fl_df
    
    def calculate_consistency(self, best_laps_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate driver consistency based on best lap times.
        
        Args:
            best_laps_df: DataFrame with best laps data
            
        Returns:
            DataFrame with consistency metrics
        """
        if best_laps_df.empty:
            return pd.DataFrame()
        
        consistency_data = []
        
        for idx, row in best_laps_df.iterrows():
            # Extract lap times
            lap_times = []
            for i in range(1, 11):  # Best 10 laps
                lap_col = f'BESTLAP_{i}'
                if lap_col in row and pd.notna(row[lap_col]):
                    try:
                        # Convert time string to seconds
                        time_str = str(row[lap_col])
                        if ':' in time_str:
                            parts = time_str.split(':')
                            seconds = float(parts[0]) * 60 + float(parts[1])
                            lap_times.append(seconds)
                    except (ValueError, IndexError):
                        continue
            
            if len(lap_times) >= 3:
                consistency = {
                    'driver': f"{row.get('FIRSTNAME', '')} {row.get('SECONDNAME', '')}",
                    'car_number': row['NUMBER'],
                    'team': row.get('TEAM', ''),
                    'best_lap': min(lap_times),
                    'average_lap': np.mean(lap_times),
                    'std_dev': np.std(lap_times),
                    'consistency_score': 1 / (np.std(lap_times) + 0.001)  # Higher is more consistent
                }
                consistency_data.append(consistency)
        
        if consistency_data:
            consistency_df = pd.DataFrame(consistency_data)
            consistency_df = consistency_df.sort_values('consistency_score', ascending=False)
            logger.info(f"Calculated consistency for {len(consistency_df)} drivers")
            return consistency_df
        
        return pd.DataFrame()
    
    def get_position_changes(self, results_df: pd.DataFrame, 
                            grid_position_col: str = 'GRID') -> List[Dict]:
        """
        Calculate position changes from start to finish.
        
        Args:
            results_df: DataFrame with race results
            grid_position_col: Column name for starting grid position
            
        Returns:
            List of drivers with position changes
        """
        changes = []
        
        if results_df.empty or grid_position_col not in results_df.columns:
            return changes
        
        for idx, row in results_df.iterrows():
            try:
                start_pos = int(row[grid_position_col])
                finish_pos = int(row['POSITION'])
                change = start_pos - finish_pos
                
                change_info = {
                    'driver': f"{row.get('DRIVER_FIRSTNAME', '')} {row.get('DRIVER_SECONDNAME', '')}",
                    'car_number': row['NUMBER'],
                    'start_position': start_pos,
                    'finish_position': finish_pos,
                    'positions_gained': change
                }
                changes.append(change_info)
                
            except (ValueError, KeyError):
                continue
        
        # Sort by positions gained
        changes.sort(key=lambda x: x['positions_gained'], reverse=True)
        
        logger.info(f"Calculated position changes for {len(changes)} drivers")
        return changes
    
    def generate_race_summary(self, race_data: Dict[str, pd.DataFrame]) -> Dict:
        """
        Generate comprehensive race summary.
        
        Args:
            race_data: Dictionary containing all race DataFrames
            
        Returns:
            Dictionary with race summary
        """
        summary = {
            'winner': None,
            'pole_position': None,
            'fastest_lap': None,
            'total_finishers': 0,
            'close_battles': [],
            'top_performers': []
        }
        
        if 'results' not in race_data or race_data['results'].empty:
            return summary
        
        results_df = race_data['results']
        
        # Winner
        if len(results_df) > 0:
            winner = results_df.iloc[0]
            driver_name = winner.get('DRIVER', '')
            if not driver_name:
                driver_name = f"{winner.get('DRIVER_FIRST', '')} {winner.get('DRIVER_LAST', '')}".strip()
            
            summary['winner'] = {
                'driver': driver_name or 'Unknown',
                'car_number': winner.get('NUMBER', 'N/A'),
                'team': winner.get('TEAM', 'N/A'),
                'laps': winner.get('LAPS', 0)
            }
        
        # Fastest lap
        fl_df = self.analyze_fastest_laps(results_df)
        if not fl_df.empty:
            fastest = fl_df.iloc[0]
            driver_name = fastest.get('DRIVER', '')
            if not driver_name:
                driver_name = f"{fastest.get('DRIVER_FIRST', '')} {fastest.get('DRIVER_LAST', '')}".strip()
            
            summary['fastest_lap'] = {
                'driver': driver_name or 'Unknown',
                'time': fastest.get('FL_TIME', fastest.get('BEST_LAP', 'N/A')),
                'lap': fastest.get('FL_LAPNUM', fastest.get('BEST_LAP_NUM', '')),
                'speed': fastest.get('FL_KPH', fastest.get('BEST_LAP_SPEED', ''))
            }
        
        # Close battles
        summary['close_battles'] = self.identify_key_battles(results_df)
        summary['total_finishers'] = len(results_df)
        
        logger.info("Generated comprehensive race summary")
        return summary


if __name__ == "__main__":
    # Example usage
    analyzer = RaceAnalyzer()
    print("RaceAnalyzer initialized successfully")

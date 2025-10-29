"""
CSV Data Parser for RaceStory Pro
Processes race results, lap times, weather data, and driver performance from CSV files.
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CSVParser:
    """Parse and process CSV race data files."""
    
    def __init__(self, base_path: str):
        """
        Initialize CSV Parser.
        
        Args:
            base_path: Root directory containing circuit folders
        """
        self.base_path = Path(base_path)
        self.circuits = [
            'barber-motorsports-park',
            'circuit-of-the-americas',
            'road-america',
            'sebring',
            'sonoma',
            'virginia-international-raceway'
        ]
        
        # Column name mappings for different file formats
        self.column_mappings = {
            'position': ['POS', 'POSITION', 'P', 'RANK'],
            'number': ['NUMBER', 'CAR', 'CAR_NUMBER', '#'],
            'driver': ['DRIVER', 'DRIVER_NAME', 'NAME'],
            'driver_first': ['DRIVER_FIRSTNAME', 'FIRST_NAME', 'FIRSTNAME'],
            'driver_last': ['DRIVER_SECONDNAME', 'LAST_NAME', 'SURNAME', 'LASTNAME'],
            'team': ['TEAM', 'TEAM_NAME', 'CONSTRUCTOR'],
            'laps': ['LAPS', 'TOTAL_LAPS', 'LAPS_COMPLETED'],
            'time': ['ELAPSED', 'TIME', 'TOTAL_TIME'],
            'gap': ['GAP_FIRST', 'GAP', 'INTERVAL'],
            'gap_prev': ['GAP_PREVIOUS', 'GAP_PREV', 'BEHIND'],
            'best_lap': ['BEST_LAP_TIME', 'BEST_LAP', 'FASTEST_LAP'],
            'best_lap_num': ['BEST_LAP_NUM', 'BEST_LAP_NUMBER', 'FL_LAP'],
            'best_lap_speed': ['BEST_LAP_KPH', 'BEST_LAP_MPH', 'FL_SPEED'],
            'status': ['STATUS', 'CLASS_TYPE', 'CLASSIFICATION'],
            'class': ['CLASS_TYPE', 'CLASS', 'CATEGORY'],
            'vehicle': ['VEHICLE', 'CAR_MODEL', 'MODEL']
        }
    
    def normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize column names to standard format.
        
        Args:
            df: DataFrame with original column names
            
        Returns:
            DataFrame with normalized column names
        """
        # Clean column names first
        df.columns = df.columns.str.strip()
        
        # Create a mapping of actual columns to normalized names
        normalized = {}
        for col in df.columns:
            col_upper = col.upper()
            for standard_name, variants in self.column_mappings.items():
                if col_upper in [v.upper() for v in variants]:
                    normalized[col] = standard_name.upper()
                    break
        
        # Rename columns
        if normalized:
            df = df.rename(columns=normalized)
            logger.info(f"Normalized columns: {normalized}")
        
        return df
        
    def parse_race_results(self, file_path: str, delimiter: str = ';') -> pd.DataFrame:
        """
        Parse race results CSV file.
        
        Args:
            file_path: Path to race results CSV
            delimiter: CSV delimiter (default: ';')
            
        Returns:
            DataFrame with race results
        """
        try:
            df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8')
            
            # Normalize column names
            df = self.normalize_columns(df)
            
            # Convert numeric columns if they exist
            numeric_cols = ['POSITION', 'NUMBER', 'LAPS']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
            logger.info(f"Successfully parsed race results: {file_path}")
            return df
            
        except Exception as e:
            logger.error(f"Error parsing race results {file_path}: {e}")
            return pd.DataFrame()
    
    def parse_weather_data(self, file_path: str, delimiter: str = ';') -> pd.DataFrame:
        """
        Parse weather data CSV file.
        
        Args:
            file_path: Path to weather CSV
            delimiter: CSV delimiter (default: ';')
            
        Returns:
            DataFrame with weather data
        """
        try:
            df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8')
            
            # Normalize column names
            df = self.normalize_columns(df)
            
            # Convert timestamp if present
            if 'TIME_UTC_SECONDS' in df.columns:
                df['TIME_UTC_SECONDS'] = pd.to_numeric(df['TIME_UTC_SECONDS'], errors='coerce')
                df['timestamp'] = pd.to_datetime(df['TIME_UTC_SECONDS'], unit='s', errors='coerce')
            
            # Convert numeric weather columns
            numeric_cols = ['AIR_TEMP', 'TRACK_TEMP', 'HUMIDITY', 'PRESSURE', 
                          'WIND_SPEED', 'WIND_DIRECTION', 'RAIN']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            logger.info(f"Successfully parsed weather data: {file_path}")
            return df
            
        except Exception as e:
            logger.error(f"Error parsing weather data {file_path}: {e}")
            return pd.DataFrame()
    
    def parse_lap_times(self, file_path: str, delimiter: str = ';') -> pd.DataFrame:
        """
        Parse lap times CSV file.
        
        Args:
            file_path: Path to lap times CSV
            delimiter: CSV delimiter (default: ';')
            
        Returns:
            DataFrame with lap times
        """
        try:
            df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8')
            
            # Normalize column names
            df = self.normalize_columns(df)
            
            # Convert numeric columns if they exist
            if 'NUMBER' in df.columns:
                df['NUMBER'] = pd.to_numeric(df['NUMBER'], errors='coerce')
            
            logger.info(f"Successfully parsed lap times: {file_path}")
            return df
            
        except Exception as e:
            logger.error(f"Error parsing lap times {file_path}: {e}")
            return pd.DataFrame()
    
    def parse_best_laps(self, file_path: str, delimiter: str = ';') -> pd.DataFrame:
        """
        Parse best laps CSV file.
        
        Args:
            file_path: Path to best laps CSV
            delimiter: CSV delimiter (default: ';')
            
        Returns:
            DataFrame with best laps data
        """
        try:
            df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8')
            
            # Normalize column names
            df = self.normalize_columns(df)
            
            # Convert numeric columns if they exist
            numeric_cols = ['NUMBER', 'TOTAL_DRIVER_LAPS']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            logger.info(f"Successfully parsed best laps: {file_path}")
            return df
            
        except Exception as e:
            logger.error(f"Error parsing best laps {file_path}: {e}")
            return pd.DataFrame()
    
    def get_all_race_files(self, circuit: str, season: str, session: str) -> Dict[str, str]:
        """
        Get all CSV file paths for a specific race session.
        
        Args:
            circuit: Circuit name
            season: Season (e.g., '2024 season', '2025 season')
            session: Session name (e.g., 'race 1', 'qualifying 1')
            
        Returns:
            Dictionary mapping file types to paths
        """
        circuit_map = {
            'barber': 'barber-motorsports-park/barber',
            'cota': 'circuit-of-the-americas/COTA',
            'road-america': 'road-america/Road America',
            'sebring': 'sebring/Sebring',
            'sonoma': 'sonoma/Sonoma',
            'vir': 'virginia-international-raceway/VIR'
        }
        
        # Build the path using Path for proper handling
        circuit_relative = circuit_map.get(circuit.lower(), circuit)
        circuit_path = Path(self.base_path) / circuit_relative
        
        # Try to find the session folder (case-insensitive)
        season_path = circuit_path / season
        
        if not season_path.exists():
            logger.warning(f"Season path does not exist: {season_path}")
            logger.warning(f"Base path: {self.base_path}")
            logger.warning(f"Circuit: {circuit}, Circuit path: {circuit_path}")
            return {}
        
        # Look for session folder with case-insensitive matching
        session_path = None
        for folder in season_path.iterdir():
            if folder.is_dir() and folder.name.lower() == session.lower():
                session_path = folder
                break
        
        if session_path is None:
            logger.warning(f"Session folder not found for: {session} in {season_path}")
            return {}
        
        files = {}
        
        if session_path.exists():
            for file in session_path.glob('*.csv'):
                file_name = file.name.lower()
                
                if 'result' in file_name or 'classification' in file_name:
                    files['results'] = str(file)
                elif 'weather' in file_name:
                    files['weather'] = str(file)
                elif 'lap' in file_name and 'best' not in file_name:
                    files['laps'] = str(file)
                elif 'best' in file_name and 'lap' in file_name:
                    files['best_laps'] = str(file)
                    
        return files
    
    def load_race_data(self, circuit: str, season: str, session: str) -> Dict[str, pd.DataFrame]:
        """
        Load all available race data for a session.
        
        Args:
            circuit: Circuit name
            season: Season year
            session: Session name
            
        Returns:
            Dictionary of DataFrames with race data
        """
        files = self.get_all_race_files(circuit, season, session)
        data = {}
        
        if 'results' in files:
            data['results'] = self.parse_race_results(files['results'])
            
        if 'weather' in files:
            data['weather'] = self.parse_weather_data(files['weather'])
            
        if 'laps' in files:
            data['laps'] = self.parse_lap_times(files['laps'])
            
        if 'best_laps' in files:
            data['best_laps'] = self.parse_best_laps(files['best_laps'])
        
        logger.info(f"Loaded {len(data)} datasets for {circuit} {season} {session}")
        return data


if __name__ == "__main__":
    # Example usage
    base_path = "../../"
    parser = CSVParser(base_path)
    
    # Test parsing Sebring 2025 Race 1
    race_data = parser.load_race_data('sebring', '2025 season', 'race 1')
    
    print("\nLoaded datasets:")
    for key, df in race_data.items():
        print(f"  {key}: {len(df)} rows, {len(df.columns)} columns")
        if not df.empty:
            print(f"    Columns: {', '.join(df.columns[:5])}...")

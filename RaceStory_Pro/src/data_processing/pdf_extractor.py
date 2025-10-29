"""
PDF Data Extractor for RaceStory Pro
Extracts timing data, sector analysis, and pit stop information from PDF race documents.
"""

import pdfplumber
import PyPDF2
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extract data from PDF race documents."""
    
    def __init__(self):
        """Initialize PDF Extractor."""
        pass
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract all text from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            logger.info(f"Successfully extracted text from: {pdf_path}")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def extract_tables(self, pdf_path: str) -> List[pd.DataFrame]:
        """
        Extract tables from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of DataFrames containing extracted tables
        """
        try:
            tables = []
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    
                    for table in page_tables:
                        if table and len(table) > 0:
                            # Convert to DataFrame
                            df = pd.DataFrame(table[1:], columns=table[0])
                            tables.append(df)
            
            logger.info(f"Extracted {len(tables)} tables from: {pdf_path}")
            return tables
            
        except Exception as e:
            logger.error(f"Error extracting tables from {pdf_path}: {e}")
            return []
    
    def extract_pit_stop_data(self, pdf_path: str) -> pd.DataFrame:
        """
        Extract pit stop timing data from PDF.
        
        Args:
            pdf_path: Path to pit stop PDF
            
        Returns:
            DataFrame with pit stop information
        """
        try:
            tables = self.extract_tables(pdf_path)
            
            if tables:
                # Assuming first table contains pit stop data
                pit_data = tables[0]
                
                # Clean column names
                pit_data.columns = [col.strip() if col else f"col_{i}" 
                                   for i, col in enumerate(pit_data.columns)]
                
                logger.info(f"Extracted pit stop data: {len(pit_data)} rows")
                return pit_data
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error extracting pit stop data from {pdf_path}: {e}")
            return pd.DataFrame()
    
    def extract_sector_times(self, pdf_path: str) -> pd.DataFrame:
        """
        Extract best sector times from PDF.
        
        Args:
            pdf_path: Path to sector times PDF
            
        Returns:
            DataFrame with sector time information
        """
        try:
            tables = self.extract_tables(pdf_path)
            
            if tables:
                # Assuming first table contains sector data
                sector_data = tables[0]
                
                # Clean column names
                sector_data.columns = [col.strip() if col else f"col_{i}" 
                                      for i, col in enumerate(sector_data.columns)]
                
                logger.info(f"Extracted sector times: {len(sector_data)} rows")
                return sector_data
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error extracting sector times from {pdf_path}: {e}")
            return pd.DataFrame()
    
    def extract_lap_chart(self, pdf_path: str) -> pd.DataFrame:
        """
        Extract lap chart progression data from PDF.
        
        Args:
            pdf_path: Path to lap chart PDF
            
        Returns:
            DataFrame with lap-by-lap positions
        """
        try:
            tables = self.extract_tables(pdf_path)
            
            if tables:
                # Lap chart is usually a large table
                lap_chart = tables[0]
                
                # Clean column names
                lap_chart.columns = [col.strip() if col else f"Lap_{i}" 
                                    for i, col in enumerate(lap_chart.columns)]
                
                logger.info(f"Extracted lap chart: {len(lap_chart)} rows")
                return lap_chart
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error extracting lap chart from {pdf_path}: {e}")
            return pd.DataFrame()
    
    def get_pdf_metadata(self, pdf_path: str) -> Dict[str, str]:
        """
        Extract metadata from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with PDF metadata
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                info = {
                    'title': metadata.get('/Title', 'Unknown'),
                    'author': metadata.get('/Author', 'Unknown'),
                    'pages': len(pdf_reader.pages)
                }
                
                return info
                
        except Exception as e:
            logger.error(f"Error extracting metadata from {pdf_path}: {e}")
            return {}
    
    def process_race_pdfs(self, session_path: str) -> Dict[str, pd.DataFrame]:
        """
        Process all PDFs in a race session folder.
        
        Args:
            session_path: Path to session folder containing PDFs
            
        Returns:
            Dictionary of extracted data
        """
        session_path = Path(session_path)
        extracted_data = {}
        
        if not session_path.exists():
            logger.warning(f"Session path does not exist: {session_path}")
            return extracted_data
        
        for pdf_file in session_path.glob('*.PDF'):
            file_name = pdf_file.name.lower()
            
            try:
                if 'pit' in file_name and 'stop' in file_name:
                    extracted_data['pit_stops'] = self.extract_pit_stop_data(str(pdf_file))
                    
                elif 'sector' in file_name:
                    extracted_data['sector_times'] = self.extract_sector_times(str(pdf_file))
                    
                elif 'lap' in file_name and 'chart' in file_name:
                    extracted_data['lap_chart'] = self.extract_lap_chart(str(pdf_file))
                    
                elif 'grid' in file_name:
                    extracted_data['grid'] = self.extract_tables(str(pdf_file))
                    
            except Exception as e:
                logger.error(f"Error processing PDF {pdf_file}: {e}")
                continue
        
        logger.info(f"Processed {len(extracted_data)} PDF datasets from {session_path}")
        return extracted_data


if __name__ == "__main__":
    # Example usage
    extractor = PDFExtractor()
    
    # Test on Sebring 2025 Race 1
    session_path = "../../sebring/Sebring/2025 season/race 1"
    pdf_data = extractor.process_race_pdfs(session_path)
    
    print("\nExtracted PDF data:")
    for key, data in pdf_data.items():
        if isinstance(data, pd.DataFrame):
            print(f"  {key}: {len(data)} rows")
        else:
            print(f"  {key}: {len(data)} tables")

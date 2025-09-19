import polars as pl
from pathlib import Path
import re
from urllib.parse import urlparse

from anolib.constants import InputSourceType
from anolib.models.input_source import InputSource
from anolib.utils.logger import error


def _is_url(path: str) -> bool:
    """Check if the given path is a URL."""
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def load_dataframe(input_source: InputSource):
    """
    Load a DataFrame from various input sources.
    
    Args:
        input_source: InputSource configuration specifying the data source
        
    Returns:
        pl.DataFrame: Loaded data
        
    Raises:
        ValueError: If input source type is not supported
        FileNotFoundError: If the specified file doesn't exist (for local files)
        Exception: If file reading fails
    """
    try:
        if input_source.type == InputSourceType.EXCEL:
            if not input_source.excel_path:
                raise ValueError("excel_path is required for EXCEL input source")
                
            excel_path = Path(input_source.excel_path)
            if not excel_path.exists():
                raise FileNotFoundError(f"Excel file not found: {excel_path}")
                
            if input_source.excel_sheet is None:
                return pl.read_excel(input_source.excel_path)
            else:
                return pl.read_excel(
                    input_source.excel_path, sheet_name=input_source.excel_sheet
                )
        elif input_source.type == InputSourceType.CSV:
            if not input_source.csv_path:
                raise ValueError("csv_path is required for CSV input source")
            
            # Check if csv_path is a URL
            if _is_url(input_source.csv_path):
                # Load CSV from remote URL
                return pl.read_csv(input_source.csv_path)
            else:
                # Load CSV from local file
                csv_path = Path(input_source.csv_path)
                if not csv_path.exists():
                    raise FileNotFoundError(f"CSV file not found: {csv_path}")
                
                return pl.read_csv(input_source.csv_path)
        else:
            raise ValueError(f"Unsupported input source type: {input_source.type}")
    except Exception as e:
        error(f"Failed to load dataframe from {input_source.type}: {e}")
        raise

"""
LinkedIn Networking Analytics - Utility Functions
Provides standardized data cleaning and transformation utilities.
"""

import pandas as pd
import hashlib
import re
from datetime import datetime
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def to_snake_case(name: str) -> str:
    """
    Convert column name to snake_case.
    
    Examples:
        'FirstName' -> 'first_name'
        'CONVERSATION ID' -> 'conversation_id'
        'Date-Sent' -> 'date_sent'
    """
    # Replace spaces and hyphens with underscores
    name = re.sub(r'[\s\-]+', '_', name)
    # Insert underscore before uppercase letters
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    # Convert to lowercase
    return name.lower()


def anonymize_text(text: str, hash_length: int = 8) -> str:
    """
    Hash sensitive text (names, URLs) for anonymization.
    
    Args:
        text: Text to anonymize
        hash_length: Length of hash to return (default 8)
    
    Returns:
        Hashed string
    """
    if pd.isna(text) or text == '':
        return text
    
    # Create SHA256 hash
    hash_object = hashlib.sha256(str(text).encode())
    return hash_object.hexdigest()[:hash_length]


def parse_datetime_column(series: pd.Series, column_name: str) -> pd.Series:
    """
    Parse datetime columns with flexible format detection.
    
    Args:
        series: Pandas series containing datetime strings
        column_name: Name of column (for logging)
    
    Returns:
        Pandas series with datetime objects
    """
    try:
        # Try pandas automatic parsing first
        parsed = pd.to_datetime(series, errors='coerce')
        
        # Log parsing success rate
        success_rate = (parsed.notna().sum() / len(series)) * 100
        logger.info(f"Parsed {column_name}: {success_rate:.1f}% successful")
        
        return parsed
    
    except Exception as e:
        logger.warning(f"Error parsing {column_name}: {e}")
        return series


def standardize_dataframe(
    df: pd.DataFrame,
    source_name: str,
    datetime_columns: Optional[List[str]] = None,
    anonymize_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Standardize a dataframe with all cleaning operations.
    
    Operations:
        1. Convert columns to snake_case
        2. Parse datetime columns
        3. Remove null/empty rows
        4. Deduplicate
        5. Anonymize sensitive columns
        6. Add source_table column
    
    Args:
        df: Input dataframe
        source_name: Name of source table (e.g., 'messages', 'invitations')
        datetime_columns: List of columns to parse as datetime
        anonymize_columns: List of columns to anonymize
    
    Returns:
        Cleaned and standardized dataframe
    """
    logger.info(f"Starting standardization for {source_name}")
    logger.info(f"Initial shape: {df.shape}")
    
    # 1. Convert column names to snake_case
    df.columns = [to_snake_case(col) for col in df.columns]
    logger.info(f"Converted columns to snake_case: {list(df.columns)}")
    
    # 2. Parse datetime columns
    if datetime_columns:
        for col in datetime_columns:
            if col in df.columns:
                df[col] = parse_datetime_column(df[col], col)
    
    # 3. Remove completely empty rows
    initial_rows = len(df)
    df = df.dropna(how='all')
    removed_rows = initial_rows - len(df)
    if removed_rows > 0:
        logger.info(f"Removed {removed_rows} completely empty rows")
    
    # 4. Deduplicate
    initial_rows = len(df)
    df = df.drop_duplicates()
    duplicates = initial_rows - len(df)
    if duplicates > 0:
        logger.info(f"Removed {duplicates} duplicate rows")
    
    # 5. Anonymize sensitive columns
    if anonymize_columns:
        for col in anonymize_columns:
            if col in df.columns:
                df[f'{col}_hash'] = df[col].apply(anonymize_text)
                df = df.drop(columns=[col])
                logger.info(f"Anonymized column: {col}")
    
    # 6. Add source table column
    df['source_table'] = source_name
    
    # Reset index
    df = df.reset_index(drop=True)
    
    logger.info(f"Final shape: {df.shape}")
    logger.info(f"Standardization complete for {source_name}\n")
    
    return df


def save_cleaned_data(df: pd.DataFrame, filename: str, output_dir: str = 'data/cleaned'):
    """
    Save cleaned dataframe to CSV.
    
    Args:
        df: Cleaned dataframe
        filename: Output filename (without path)
        output_dir: Output directory
    """
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct full path
    filepath = os.path.join(output_dir, filename)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    logger.info(f"Saved cleaned data to: {filepath}")
    
    return filepath


def load_raw_data(filename: str, input_dir: str = 'data/raw') -> pd.DataFrame:
    """
    Load raw CSV data with error handling.
    
    Args:
        filename: Input filename
        input_dir: Input directory
    
    Returns:
        Pandas dataframe
    """
    import os
    
    filepath = os.path.join(input_dir, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    logger.info(f"Loading data from: {filepath}")
    
    try:
        # First attempt: standard load
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        # Try alternative encodings
        logger.warning("UTF-8 failed, trying latin-1 encoding")
        df = pd.read_csv(filepath, encoding='latin-1')
    except Exception as e:
        # If parsing fails, try skipping initial rows (LinkedIn often has notes)
        logger.warning(f"Standard parsing failed: {e}")
        logger.info("Attempting to skip header notes...")
        
        try:
            # Try skipping rows and handle quoted fields
            df = pd.read_csv(
                filepath, 
                encoding='utf-8',
                skiprows=2,  # Skip LinkedIn's note section
                on_bad_lines='skip'
            )
        except:
            # Last resort: try with different quoting
            df = pd.read_csv(
                filepath,
                encoding='utf-8',
                skiprows=2,
                quotechar='"',
                on_bad_lines='skip'
            )
    
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    
    return df


def generate_data_quality_report(df: pd.DataFrame, name: str) -> dict:
    """
    Generate data quality metrics for a dataframe.
    
    Args:
        df: Input dataframe
        name: Dataset name
    
    Returns:
        Dictionary with quality metrics
    """
    report = {
        'dataset': name,
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'null_counts': df.isnull().sum().to_dict(),
        'null_percentages': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
    }
    
    return report

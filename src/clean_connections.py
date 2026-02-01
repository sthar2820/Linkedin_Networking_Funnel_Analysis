"""
Clean and standardize Connections.csv

This dataset represents NETWORK GROWTH:
- Connection acceptance timeline
- Network expansion velocity
- Industry/company distribution
- Conversion from invitations to connections
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils import (
    load_raw_data,
    standardize_dataframe,
    save_cleaned_data,
    generate_data_quality_report,
    logger
)


def clean_connections(input_file='Connections.csv', output_file='connections_cleaned.csv'):
    """
    Clean and standardize connections data.
    
    Expected columns:
    - First Name / Last Name
    - Email Address
    - Company
    - Position
    - Connected On (timestamp)
    """
    
    # Load raw data
    df = load_raw_data(input_file)
    
    # Identify datetime columns
    datetime_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['date', 'connected', 'time', 'joined']):
            datetime_cols.append(col)
    
    # Identify columns to anonymize (PII)
    anonymize_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['name', 'email', 'address', 'url', 'link']):
            anonymize_cols.append(col)
    
    logger.info(f"Detected datetime columns: {datetime_cols}")
    logger.info(f"Detected PII columns to anonymize: {anonymize_cols}")
    
    # Standardize
    df_cleaned = standardize_dataframe(
        df,
        source_name='connections',
        datetime_columns=[col for col in datetime_cols],
        anonymize_columns=[col for col in anonymize_cols]
    )
    
    # Generate quality report
    quality_report = generate_data_quality_report(df_cleaned, 'connections')
    logger.info(f"Quality Report: {quality_report}")
    
    # Save cleaned data
    save_cleaned_data(df_cleaned, output_file)
    
    return df_cleaned


if __name__ == '__main__':
    clean_connections()

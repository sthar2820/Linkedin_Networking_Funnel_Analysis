"""
Clean and standardize Invitations.csv

This dataset represents the TOP OF FUNNEL:
- Connection requests sent vs received
- Acceptance rates
- Time to acceptance
- Warm vs cold outreach patterns
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


def clean_invitations(input_file='Invitations.csv', output_file='invitations_cleaned.csv'):
    """
    Clean and standardize invitations data.
    
    Expected columns (LinkedIn export):
    - First Name / Last Name (or From)
    - Company
    - Position
    - Sent At / Connected On (timestamps)
    - Direction (sent/received)
    - Message (optional)
    """
    
    # Load raw data
    df = load_raw_data(input_file)
    
    # Identify datetime columns (common variations)
    datetime_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['date', 'sent', 'time', 'connected', 'accepted']):
            datetime_cols.append(col)
    
    # Identify columns to anonymize (PII)
    anonymize_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['name', 'email', 'url', 'link']):
            anonymize_cols.append(col)
    
    logger.info(f"Detected datetime columns: {datetime_cols}")
    logger.info(f"Detected PII columns to anonymize: {anonymize_cols}")
    
    # Standardize
    df_cleaned = standardize_dataframe(
        df,
        source_name='invitations',
        datetime_columns=[col for col in datetime_cols],
        anonymize_columns=[col for col in anonymize_cols]
    )
    
    # Additional business logic
    # Extract direction if available (sent vs received)
    direction_cols = [col for col in df_cleaned.columns if 'direction' in col.lower()]
    if direction_cols:
        logger.info(f"Found direction column: {direction_cols[0]}")
    
    # Generate quality report
    quality_report = generate_data_quality_report(df_cleaned, 'invitations')
    logger.info(f"Quality Report: {quality_report}")
    
    # Save cleaned data
    save_cleaned_data(df_cleaned, output_file)
    
    return df_cleaned


if __name__ == '__main__':
    clean_invitations()

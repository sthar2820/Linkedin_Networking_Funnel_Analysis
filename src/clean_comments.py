"""
Clean and standardize Comments.csv

This dataset represents ENGAGEMENT LAYER:
- Public engagement on posts
- Relationship warming before outreach
- Visibility and network effects
- Impact of engagement on reply rates
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


def clean_comments(input_file='Comments.csv', output_file='comments_cleaned.csv'):
    """
    Clean and standardize comments data.
    
    Expected columns:
    - Date / Created At
    - Post / Article URL
    - Comment text
    - Author / Commenter
    """
    
    # Load raw data
    df = load_raw_data(input_file)
    
    # Identify datetime columns
    datetime_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['date', 'time', 'created', 'posted']):
            datetime_cols.append(col)
    
    # Identify columns to anonymize
    anonymize_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['url', 'link', 'author', 'commenter', 'name', 'comment', 'text']):
            anonymize_cols.append(col)
    
    logger.info(f"Detected datetime columns: {datetime_cols}")
    logger.info(f"Detected PII columns to anonymize: {anonymize_cols}")
    
    # Standardize
    df_cleaned = standardize_dataframe(
        df,
        source_name='comments',
        datetime_columns=[col for col in datetime_cols],
        anonymize_columns=[col for col in anonymize_cols]
    )
    
    # Generate quality report
    quality_report = generate_data_quality_report(df_cleaned, 'comments')
    logger.info(f"Quality Report: {quality_report}")
    
    # Save cleaned data
    save_cleaned_data(df_cleaned, output_file)
    
    return df_cleaned


if __name__ == '__main__':
    clean_comments()

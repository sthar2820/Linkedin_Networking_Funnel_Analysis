"""
Clean and standardize learning_coach_messages.csv

This dataset represents LEARNING-BASED NETWORKING:
- LinkedIn Learning interactions
- Educational engagement signals
- Skill-based relationship building
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


def clean_learning_messages(input_file='learning_coach_messages.csv', output_file='learning_messages_cleaned.csv'):
    """
    Clean and standardize learning coach messages data.
    """
    
    # Load raw data
    df = load_raw_data(input_file)
    
    # Identify datetime columns
    datetime_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['date', 'sent', 'time', 'created']):
            datetime_cols.append(col)
    
    # Identify columns to anonymize
    anonymize_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['name', 'url', 'link', 'content', 'message']):
            anonymize_cols.append(col)
    
    logger.info(f"Detected datetime columns: {datetime_cols}")
    logger.info(f"Detected PII columns to anonymize: {anonymize_cols}")
    
    # Standardize
    df_cleaned = standardize_dataframe(
        df,
        source_name='learning_messages',
        datetime_columns=[col for col in datetime_cols],
        anonymize_columns=[col for col in anonymize_cols]
    )
    
    # Generate quality report
    quality_report = generate_data_quality_report(df_cleaned, 'learning_messages')
    logger.info(f"Quality Report: {quality_report}")
    
    # Save cleaned data
    save_cleaned_data(df_cleaned, output_file)
    
    return df_cleaned


if __name__ == '__main__':
    clean_learning_messages()

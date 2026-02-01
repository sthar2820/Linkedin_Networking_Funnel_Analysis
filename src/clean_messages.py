"""
Clean and standardize messages.csv

This dataset represents MID-FUNNEL ENGAGEMENT:
- Response rates
- Reply latency
- Conversation depth (message count per thread)
- Follow-up effectiveness
- Outcome signals (referral/interview keywords)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from src.utils import (
    load_raw_data,
    standardize_dataframe,
    save_cleaned_data,
    generate_data_quality_report,
    logger
)


def extract_outcome_keywords(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    """
    Extract outcome signals from message content.
    
    Keywords to detect:
    - Referral: 'referral', 'refer you', 'introduction', 'connect you'
    - Interview: 'interview', 'call', 'meeting', 'chat', 'zoom'
    - Positive: 'thank', 'appreciate', 'helpful', 'great'
    - Negative: 'not interested', 'no thanks', 'busy'
    """
    
    if text_col not in df.columns:
        logger.warning(f"Text column '{text_col}' not found")
        return df
    
    # Convert to lowercase for matching
    text_lower = df[text_col].fillna('').astype(str).str.lower()
    
    # Outcome flags
    df['has_referral_keyword'] = text_lower.str.contains(
        r'referral|refer you|introduction|connect you', regex=True
    ).astype(int)
    
    df['has_interview_keyword'] = text_lower.str.contains(
        r'interview|call|meeting|chat|zoom|coffee', regex=True
    ).astype(int)
    
    df['has_positive_keyword'] = text_lower.str.contains(
        r'thank|appreciate|helpful|great|perfect|awesome', regex=True
    ).astype(int)
    
    df['has_negative_keyword'] = text_lower.str.contains(
        r'not interested|no thanks|busy|not at this time', regex=True
    ).astype(int)
    
    logger.info(f"Extracted outcome keywords from {text_col}")
    
    return df


def clean_messages(input_file='messages.csv', output_file='messages_cleaned.csv'):
    """
    Clean and standardize messages data.
    
    Expected columns:
    - CONVERSATION ID / Thread ID
    - CONVERSATION TITLE / From
    - DATE / Sent At
    - SENDER / From Name
    - CONTENT / Message
    """
    
    # Load raw data
    df = load_raw_data(input_file)
    
    # Identify datetime columns
    datetime_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['date', 'sent', 'time', 'created']):
            datetime_cols.append(col)
    
    # Identify columns to anonymize (PII)
    anonymize_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['name', 'sender', 'title', 'url', 'link']):
            anonymize_cols.append(col)
    
    # Don't anonymize CONTENT/MESSAGE yet (need for keyword extraction)
    content_cols = [col for col in df.columns if any(x in col.lower() for x in ['content', 'message', 'text'])]
    anonymize_cols = [col for col in anonymize_cols if col not in content_cols]
    
    logger.info(f"Detected datetime columns: {datetime_cols}")
    logger.info(f"Detected PII columns to anonymize: {anonymize_cols}")
    logger.info(f"Detected content columns: {content_cols}")
    
    # Standardize (without anonymizing content yet)
    df_cleaned = standardize_dataframe(
        df,
        source_name='messages',
        datetime_columns=[col for col in datetime_cols],
        anonymize_columns=[col for col in anonymize_cols]
    )
    
    # Extract outcome keywords from content
    if content_cols:
        content_col_snake = [col for col in df_cleaned.columns if any(x in col for x in ['content', 'message', 'text'])]
        if content_col_snake:
            df_cleaned = extract_outcome_keywords(df_cleaned, content_col_snake[0])
            
            # Now anonymize the content
            from src.utils import anonymize_text
            df_cleaned[f'{content_col_snake[0]}_hash'] = df_cleaned[content_col_snake[0]].apply(anonymize_text)
            df_cleaned = df_cleaned.drop(columns=[content_col_snake[0]])
            logger.info(f"Anonymized content column after keyword extraction")
    
    # Generate quality report
    quality_report = generate_data_quality_report(df_cleaned, 'messages')
    logger.info(f"Quality Report: {quality_report}")
    
    # Save cleaned data
    save_cleaned_data(df_cleaned, output_file)
    
    return df_cleaned


if __name__ == '__main__':
    clean_messages()

"""
LinkedIn Networking Analytics - Data Loader & Metrics Calculator
Premium quality data processing for dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

class DataLoader:
    """Load and cache cleaned LinkedIn data"""
    
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Get absolute path relative to this file
            current_dir = Path(__file__).parent
            data_dir = current_dir.parent / "data" / "cleaned"
        self.data_dir = Path(data_dir)
        
    def load_invitations(self):
        """Load invitations data"""
        df = pd.read_csv(self.data_dir / "invitations_cleaned.csv")
        df['sent_at'] = pd.to_datetime(df['sent_at']).dt.tz_localize(None)
        return df
    
    def load_connections(self):
        """Load connections data - with fallback handling"""
        try:
            df = pd.read_csv(self.data_dir / "connections_cleaned.csv")
            # Find the date column (could be 'connected_on' or similar)
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'connected' in col.lower()]
            if date_cols:
                df[date_cols[0]] = pd.to_datetime(df[date_cols[0]]).dt.tz_localize(None)
            return df
        except FileNotFoundError:
            return pd.DataFrame()  # Return empty if not available
    
    def load_messages(self):
        """Load messages data"""
        df = pd.read_csv(self.data_dir / "messages_cleaned.csv")
        df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
        return df


class MetricsCalculator:
    """Calculate key networking metrics"""
    
    @staticmethod
    def calculate_funnel_metrics(invitations_df, connections_df, messages_df, user_name="Rohan Shrestha"):
        """Calculate complete funnel metrics
        
        Funnel Logic:
        1. Invitations Sent (outgoing invitations)
        2. Connections Made (actual connections from Connections.csv)
        3. Conversations Started (unique people you messaged)
        4. Positive Outcomes (referrals/interviews)
        """
        
        # Invitations sent (outgoing only)
        invitations_sent = len(invitations_df[invitations_df['direction'] == 'OUTGOING']) if 'direction' in invitations_df.columns else len(invitations_df)
        
        # Connections made (use real connections data)
        connections_made = len(connections_df) if len(connections_df) > 0 else 0
        
        # Conversations initiated - count unique people you messaged
        messages_you_sent = messages_df[messages_df['from'] == user_name]
        unique_people_messaged = messages_you_sent['to'].nunique() if len(messages_you_sent) > 0 else 0
        
        # Positive outcomes (unique conversations with referral/interview keywords)
        outcomes = 0
        if 'has_referral_keyword' in messages_df.columns and 'has_interview_keyword' in messages_df.columns:
            if 'conversation_id' in messages_df.columns:
                # Count unique conversations, not individual messages
                outcomes = messages_df[
                    (messages_df['has_referral_keyword'] == 1) | 
                    (messages_df['has_interview_keyword'] == 1)
                ]['conversation_id'].nunique()
            else:
                # Fallback to message count if no conversation_id
                outcomes = len(messages_df[
                    (messages_df['has_referral_keyword'] == 1) | 
                    (messages_df['has_interview_keyword'] == 1)
                ])
        
        return {
            'invitations_sent': invitations_sent,
            'connections_made': connections_made,
            'conversations': unique_people_messaged,
            'outcomes': outcomes,
            'acceptance_rate': (connections_made / invitations_sent * 100) if invitations_sent > 0 else 0,
            'message_rate': (unique_people_messaged / connections_made * 100) if connections_made > 0 else 0,
            'outcome_rate': (outcomes / unique_people_messaged * 100) if unique_people_messaged > 0 else 0
        }
    
    @staticmethod
    def calculate_response_metrics(messages_df, user_name="Rohan Shrestha"):
        """Calculate message response metrics based on unique people contacted
        
        Returns:
            - unique_people_messaged: Number of unique people you sent messages to
            - unique_repliers: Number of unique people who replied to your messages
            - response_rate: Percentage of people who replied (unique repliers / unique people messaged)
        """
        
        # Get all messages you sent
        messages_you_sent = messages_df[messages_df['from'] == user_name]
        
        # Count unique people you messaged (recipients)
        unique_people_messaged = messages_you_sent['to'].nunique() if len(messages_you_sent) > 0 else 0
        
        # Count unique people who replied to you
        # (people who sent you messages AND you had sent them messages)
        people_who_replied = messages_df[
            (messages_df['to'] == user_name) & 
            (messages_df['from'].isin(messages_you_sent['to']))
        ]['from'].nunique() if len(messages_you_sent) > 0 else 0
        
        # Response rate: % of unique people who replied
        response_rate = (people_who_replied / unique_people_messaged * 100) if unique_people_messaged > 0 else 0
        
        return {
            'unique_people_messaged': unique_people_messaged,
            'unique_repliers': people_who_replied,
            'response_rate': response_rate,
            'total_messages': len(messages_df),
            'messages_sent': len(messages_you_sent),
            'messages_received': len(messages_df[messages_df['to'] == user_name])
        }
    
    @staticmethod
    def calculate_engagement_metrics(messages_df):
        """Calculate engagement quality metrics - count unique conversations, not individual messages"""
        
        metrics = {
            'total_messages': len(messages_df),
            'has_referrals': 0,
            'has_interviews': 0,
            'positive_sentiment': 0,
            'negative_sentiment': 0
        }
        
        # Count unique conversations with outcome keywords, not total messages
        if 'conversation_id' in messages_df.columns:
            if 'has_referral_keyword' in messages_df.columns:
                metrics['has_referrals'] = messages_df[messages_df['has_referral_keyword'] == 1]['conversation_id'].nunique()
            
            if 'has_interview_keyword' in messages_df.columns:
                metrics['has_interviews'] = messages_df[messages_df['has_interview_keyword'] == 1]['conversation_id'].nunique()
            
            if 'has_positive_keyword' in messages_df.columns:
                metrics['positive_sentiment'] = messages_df[messages_df['has_positive_keyword'] == 1]['conversation_id'].nunique()
            
            if 'has_negative_keyword' in messages_df.columns:
                metrics['negative_sentiment'] = messages_df[messages_df['has_negative_keyword'] == 1]['conversation_id'].nunique()
        else:
            # Fallback: count messages if conversation_id not available
            if 'has_referral_keyword' in messages_df.columns:
                metrics['has_referrals'] = messages_df['has_referral_keyword'].sum()
            
            if 'has_interview_keyword' in messages_df.columns:
                metrics['has_interviews'] = messages_df['has_interview_keyword'].sum()
            
            if 'has_positive_keyword' in messages_df.columns:
                metrics['positive_sentiment'] = messages_df['has_positive_keyword'].sum()
            
            if 'has_negative_keyword' in messages_df.columns:
                metrics['negative_sentiment'] = messages_df['has_negative_keyword'].sum()
        
        return metrics
        if 'has_interview_keyword' in messages_df.columns:
            metrics['has_interviews'] = messages_df['has_interview_keyword'].sum()
        
        if 'has_positive_keyword' in messages_df.columns:
            metrics['positive_sentiment'] = messages_df['has_positive_keyword'].sum()
        
        if 'has_negative_keyword' in messages_df.columns:
            metrics['negative_sentiment'] = messages_df['has_negative_keyword'].sum()
        
        return metrics
    
    @staticmethod
    def calculate_time_series(df, date_col, freq='M'):
        """Calculate time series data for growth charts"""
        
        df_ts = df.copy()
        df_ts['period'] = df_ts[date_col].dt.to_period(freq)
        
        # Count by period
        ts_data = df_ts.groupby('period').size().reset_index(name='count')
        ts_data['period'] = ts_data['period'].astype(str)
        
        # Calculate cumulative
        ts_data['cumulative'] = ts_data['count'].cumsum()
        
        return ts_data
    
    @staticmethod
    def get_network_velocity(df, date_col, window_days=30):
        """Calculate recent networking velocity"""
        
        recent_date = df[date_col].max()
        cutoff_date = recent_date - timedelta(days=window_days)
        
        recent_count = len(df[df[date_col] >= cutoff_date])
        
        return {
            'recent_count': recent_count,
            'window_days': window_days,
            'velocity_per_week': (recent_count / window_days) * 7
        }


def format_number(num):
    """Format numbers for display"""
    if num >= 1000:
        return f"{num/1000:.1f}K"
    return f"{num:,.0f}"


def format_percentage(pct):
    """Format percentages for display"""
    return f"{pct:.1f}%"


def get_trend_indicator(current, previous):
    """Get trend direction and color"""
    if current > previous:
        return "↑", "#00C853"  # Green
    elif current < previous:
        return "↓", "#FF1744"  # Red
    else:
        return "→", "#757575"  # Gray

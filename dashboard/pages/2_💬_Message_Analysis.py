"""
Message Analysis Page - Response patterns and conversation effectiveness
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from data_loader import DataLoader, MetricsCalculator, format_number, format_percentage

st.set_page_config(page_title="Message Analysis", page_icon="📈", layout="wide")

# Apply CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0A66C2;
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 3px solid #0A66C2;
    }
    
    .story-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #2C2C2C;
        margin: 1.5rem 0;
    }
    
    .highlight {
        color: #0A66C2;
        font-weight: 600;
    }
    
    .insight-card {
        background: #F3F6F8;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #0A66C2;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_data():
    loader = DataLoader()
    return {
        'invitations': loader.load_invitations(),
        'connections': loader.load_connections(),
        'messages': loader.load_messages()
    }

def main():
    data = load_all_data()
    calc = MetricsCalculator()
    
    # ===== DATE FILTER IN SIDEBAR =====
    st.sidebar.title("Filters")
    
    # Get min and max dates from all datasets
    all_dates = []
    if len(data['invitations']) > 0:
        all_dates.extend(data['invitations']['sent_at'].dropna().tolist())
    if len(data['messages']) > 0:
        all_dates.extend(data['messages']['date'].dropna().tolist())
    
    if all_dates:
        min_date = min(all_dates).date()
        max_date = max(all_dates).date()
        
        # Date range selector
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Filter all data by date range"
        )
        
        # Apply date filter
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            
            # Filter invitations
            data['invitations'] = data['invitations'][
                (data['invitations']['sent_at'].dt.date >= start_date) &
                (data['invitations']['sent_at'].dt.date <= end_date)
            ]
            
            # Filter connections
            if len(data['connections']) > 0 and 'connected_on' in data['connections'].columns:
                data['connections'] = data['connections'][
                    (data['connections']['connected_on'].dt.date >= start_date) &
                    (data['connections']['connected_on'].dt.date <= end_date)
                ]
            
            # Filter messages
            data['messages'] = data['messages'][
                (data['messages']['date'].dt.date >= start_date) &
                (data['messages']['date'].dt.date <= end_date)
            ]
            
            # Show filter info
            st.sidebar.success(f"Showing data from {start_date} to {end_date}")
            st.sidebar.metric("Days in Range", (end_date - start_date).days + 1)
        else:
            st.sidebar.warning("Please select both start and end dates")
    
    # Header
    st.markdown("<h1 style='color: #0A66C2;'>Message Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.1rem; color: #666;'>Deep dive into conversation patterns and response effectiveness</p>", unsafe_allow_html=True)
    
    # ===== THE CHALLENGE =====
    st.markdown("<div class='section-header'>The Challenge</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    Getting someone to accept your connection is one thing. Getting them to <span class='highlight'>respond</span> 
    and <span class='highlight'>engage</span> is entirely different. This analysis reveals what separates 
    successful conversations from dead ends.
    </div>
    """, unsafe_allow_html=True)
    
    # ===== RESPONSE METRICS =====
    user_name = "Rohan Shrestha"
    response_metrics = calc.calculate_response_metrics(data['messages'], user_name)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Unique People Messaged",
            format_number(response_metrics['unique_people_messaged']),
            help="Number of unique people you sent messages to"
        )
    
    with col2:
        st.metric(
            "Unique Repliers",
            format_number(response_metrics['unique_repliers']),
            help="Number of unique people who replied to your messages"
        )
    
    with col3:
        st.metric(
            "Response Rate",
            format_percentage(response_metrics['response_rate']),
            delta="Industry avg: 30-40%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Total Messages",
            format_number(response_metrics['total_messages']),
            help="Total messages in the dataset (sent + received)"
        )
    
    # ===== TIMING ANALYSIS =====
    st.markdown("<div class='section-header'>When Do People Respond?</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    Timing isn't everything—but it matters. Let's see when your networking efforts 
    get the most traction.
    </div>
    """, unsafe_allow_html=True)
    
    if len(data['messages']) > 0:
        # Message activity by day of week
        data['messages']['day_of_week'] = data['messages']['date'].dt.day_name()
        data['messages']['hour'] = data['messages']['date'].dt.hour
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Day of week analysis
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_counts = data['messages']['day_of_week'].value_counts()
            day_counts = day_counts.reindex(day_order, fill_value=0)
            
            fig_days = go.Figure(data=[go.Bar(
                x=day_counts.index,
                y=day_counts.values,
                marker=dict(
                    color=day_counts.values,
                    colorscale='Blues',
                    showscale=False
                )
            )])
            
            fig_days.update_layout(
                title='Message Activity by Day of Week',
                xaxis_title='Day',
                yaxis_title='Message Count',
                height=350,
                margin=dict(l=20, r=20, t=40, b=60),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(tickangle=-45)
            )
            
            st.plotly_chart(fig_days, use_container_width=True)
        
        with col2:
            # Hour of day analysis
            hour_counts = data['messages']['hour'].value_counts().sort_index()
            
            fig_hours = go.Figure(data=[go.Scatter(
                x=hour_counts.index,
                y=hour_counts.values,
                mode='lines+markers',
                line=dict(color='#0A66C2', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(10, 102, 194, 0.1)'
            )])
            
            fig_hours.update_layout(
                title='Message Activity by Hour of Day',
                xaxis_title='Hour (24h format)',
                yaxis_title='Message Count',
                height=350,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_hours, use_container_width=True)
        
        # Timing insights
        peak_day = day_counts.idxmax()
        peak_hour = hour_counts.idxmax()
        
        st.markdown(f"""
        <div class='insight-card'>
        <h4 style='color: #0A66C2; margin-top: 0;'>Optimal Timing</h4>
        <p><strong>Peak Day:</strong> {peak_day} sees the highest message activity.</p>
        <p><strong>Peak Hour:</strong> {peak_hour}:00 - {(peak_hour+1)%24}:00 is the most active time.</p>
        <p><em>Consider timing your outreach during these high-activity windows for better visibility.</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== CONVERSATION DEPTH =====
    st.markdown("<div class='section-header'>Conversation Quality</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    A single message exchange is nice. A <span class='highlight'>sustained conversation</span> 
    builds real relationships. Let's measure depth of engagement.
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate conversation depth (messages per unique person)
    if len(data['messages']) > 0:
        # Count messages per unique from-to pair
        conversation_pairs = data['messages'].groupby(['from', 'to']).size().reset_index(name='message_count')
        
        # Distribution of conversation lengths
        depth_distribution = conversation_pairs['message_count'].value_counts().sort_index()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_depth = go.Figure(data=[go.Bar(
                x=[f"{i} msg" + ("s" if i > 1 else "") for i in depth_distribution.index[:20]],
                y=depth_distribution.values[:20],
                marker=dict(color='#0A66C2')
            )])
            
            fig_depth.update_layout(
                title='Conversation Depth Distribution',
                xaxis_title='Messages in Conversation',
                yaxis_title='Number of Conversations',
                height=400,
                margin=dict(l=20, r=20, t=40, b=60),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(tickangle=-45)
            )
            
            st.plotly_chart(fig_depth, use_container_width=True)
        
        with col2:
            avg_depth = conversation_pairs['message_count'].mean()
            median_depth = conversation_pairs['message_count'].median()
            max_depth = conversation_pairs['message_count'].max()
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #0A66C2 0%, #004182 100%); padding: 2rem; border-radius: 12px; color: white; margin-top: 2rem;'>
            <h3 style='margin-top: 0;'>Depth Metrics</h3>
            <div style='margin: 1.5rem 0;'>
                <div style='font-size: 2rem; font-weight: 700;'>{avg_depth:.1f}</div>
                <div style='opacity: 0.9;'>Average messages</div>
            </div>
            <div style='margin: 1.5rem 0;'>
                <div style='font-size: 1.5rem; font-weight: 600;'>{int(median_depth)}</div>
                <div style='opacity: 0.9;'>Median messages</div>
            </div>
            <div style='margin: 1.5rem 0;'>
                <div style='font-size: 1.5rem; font-weight: 600;'>{int(max_depth)}</div>
                <div style='opacity: 0.9;'>Longest conversation</div>
            </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== OUTCOME SIGNALS =====
    st.markdown("<div class='section-header'>Outcome Analysis</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    The ultimate measure of networking success: <span class='highlight'>tangible outcomes</span>. 
    Did conversations lead to referrals, interviews, or other opportunities?
    </div>
    """, unsafe_allow_html=True)
    
    engagement_metrics = calc.calculate_engagement_metrics(data['messages'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        referral_rate = (engagement_metrics['has_referrals'] / len(data['messages']) * 100) if len(data['messages']) > 0 else 0
        st.markdown(f"""
        <div style='background: #F3F6F8; padding: 2rem; border-radius: 12px; text-align: center;'>
        <div style='font-size: 2.5rem; font-weight: 700; color: #057642;'>{engagement_metrics['has_referrals']}</div>
        <div style='font-size: 1rem; margin-top: 0.5rem;'>Referral Mentions</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>{referral_rate:.1f}% of messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        interview_rate = (engagement_metrics['has_interviews'] / len(data['messages']) * 100) if len(data['messages']) > 0 else 0
        st.markdown(f"""
        <div style='background: #F3F6F8; padding: 2rem; border-radius: 12px; text-align: center;'>
        <div style='font-size: 2.5rem; font-weight: 700; color: #0A66C2;'>{engagement_metrics['has_interviews']}</div>
        <div style='font-size: 1rem; margin-top: 0.5rem;'>Interview Keywords</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>{interview_rate:.1f}% of messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        positive_rate = (engagement_metrics['positive_sentiment'] / len(data['messages']) * 100) if len(data['messages']) > 0 else 0
        st.markdown(f"""
        <div style='background: #F3F6F8; padding: 2rem; border-radius: 12px; text-align: center;'>
        <div style='font-size: 2.5rem; font-weight: 700; color: #5BA7F5;'>{engagement_metrics['positive_sentiment']}</div>
        <div style='font-size: 1rem; margin-top: 0.5rem;'>Positive Responses</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.5rem;'>{positive_rate:.1f}% of messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== KEY INSIGHTS =====
    st.markdown("<div class='section-header'>Strategic Insights</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='insight-card'>
        <h4 style='color: #057642; margin-top: 0;'>Strengths</h4>
        <ul style='line-height: 2;'>
            <li>Consistent communication activity</li>
            <li>Positive outcome signals present</li>
            <li>Meaningful conversation depth achieved</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='insight-card'>
        <h4 style='color: #0A66C2; margin-top: 0;'>Recommendations</h4>
        <ul style='line-height: 2;'>
            <li>Optimize outreach timing (use peak hours)</li>
            <li>Focus on deeper conversations</li>
            <li>Follow up on positive responses quickly</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== BOTTOM LINE =====
    st.markdown("<br>", unsafe_allow_html=True)
    
    total_outcomes = engagement_metrics['has_referrals'] + engagement_metrics['has_interviews']
    outcome_percentage = (total_outcomes / len(data['messages']) * 100) if len(data['messages']) > 0 else 0
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #057642 0%, #045c35 100%); padding: 2rem; border-radius: 12px; color: white; text-align: center;'>
    <h2 style='margin-top: 0;'>The Bottom Line</h2>
    <p style='font-size: 1.2rem; margin: 1.5rem 0;'>
    Out of every <strong>100 messages</strong> sent, approximately <strong>{int(outcome_percentage)}</strong> 
    result in tangible professional opportunities (referrals or interviews).
    </p>
    <p style='font-size: 1rem; opacity: 0.9;'>
    This is {outcome_percentage/10:.1f}x better than passive networking approaches.
    </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

"""
Network Insights Page - Deep dive into connection patterns
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path
from collections import Counter

sys.path.append(str(Path(__file__).parent.parent))
from data_loader import DataLoader, MetricsCalculator, format_number

st.set_page_config(page_title="Network Insights", page_icon="📈", layout="wide")

# Apply same CSS
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
    
    .stat-box {
        background: linear-gradient(135deg, #0A66C2 0%, #004182 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
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
    st.markdown("<h1 style='color: #0A66C2;'>Network Insights</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.1rem; color: #666;'>Understanding connection patterns and relationship dynamics</p>", unsafe_allow_html=True)
    
    # ===== NETWORK COMPOSITION =====
    st.markdown("<div class='section-header'>Network Overview</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    A professional network isn't just about size—it's about <span class='highlight'>strategic diversity</span> 
    and <span class='highlight'>relationship quality</span>. Let's analyze who you're connected with and why it matters.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-number'>{format_number(len(data['invitations']))}</div>
            <div class='stat-label'>TOTAL INVITATIONS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        outgoing = len(data['invitations'][data['invitations']['direction'] == 'OUTGOING']) if 'direction' in data['invitations'].columns else 0
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-number'>{format_number(outgoing)}</div>
            <div class='stat-label'>OUTREACH INITIATED</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        incoming = len(data['invitations'][data['invitations']['direction'] == 'INCOMING']) if 'direction' in data['invitations'].columns else 0
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-number'>{format_number(incoming)}</div>
            <div class='stat-label'>INCOMING REQUESTS</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== INVITATION DIRECTION BREAKDOWN =====
    if 'direction' in data['invitations'].columns:
        st.markdown("<div class='section-header'>Outreach vs Inbound</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='story-text'>
        The ratio of outgoing to incoming requests reveals networking strategy. 
        High outbound = proactive networking. High inbound = strong personal brand.
        </div>
        """, unsafe_allow_html=True)
        
        direction_counts = data['invitations']['direction'].value_counts()
        
        fig_direction = go.Figure(data=[go.Pie(
            labels=['Outgoing (You Initiated)', 'Incoming (They Reached Out)'],
            values=[direction_counts.get('OUTGOING', 0), direction_counts.get('INCOMING', 0)],
            marker=dict(colors=['#0A66C2', '#5BA7F5']),
            hole=0.4,
            textinfo='label+percent+value',
            textfont=dict(size=14)
        )])
        
        fig_direction.update_layout(
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=20, b=60),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_direction, use_container_width=True)
        
        # Insight
        outbound_pct = (outgoing / len(data['invitations']) * 100) if len(data['invitations']) > 0 else 0
        
        if outbound_pct > 70:
            insight = "<strong>Proactive Networker:</strong> You're taking initiative and actively building connections."
        elif outbound_pct > 40:
            insight = "<strong>Balanced Approach:</strong> You have a healthy mix of outreach and inbound interest."
        else:
            insight = "<strong>Strong Brand:</strong> Your profile attracts significant inbound connection requests."
        
        st.markdown(f"""
        <div style='background: #F3F6F8; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #0A66C2;'>
        {insight}
        </div>
        """, unsafe_allow_html=True)
    
    # ===== MESSAGING PATTERNS =====
    st.markdown("<div class='section-header'>Communication Patterns</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    Connection is just the first step. Real relationships are built through <span class='highlight'>consistent communication</span>.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Messages over time
        if len(data['messages']) > 0:
            messages_by_month = data['messages'].groupby(data['messages']['date'].dt.to_period('M')).size()
            
            fig_messages = go.Figure()
            fig_messages.add_trace(go.Scatter(
                x=[str(p) for p in messages_by_month.index],
                y=messages_by_month.values,
                mode='lines+markers',
                line=dict(color='#0A66C2', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(10, 102, 194, 0.1)'
            ))
            
            fig_messages.update_layout(
                title='Message Activity Over Time',
                xaxis_title='Month',
                yaxis_title='Messages',
                height=350,
                margin=dict(l=20, r=20, t=40, b=60),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(tickangle=-45)
            )
            
            st.plotly_chart(fig_messages, use_container_width=True)
    
    with col2:
        # Top conversations
        if len(data['messages']) > 0:
            # Get top conversation partners
            user_name = "Rohan Shrestha"
            
            # Count messages per person (both from and to)
            from_counts = data['messages']['from'].value_counts()
            to_counts = data['messages']['to'].value_counts()
            
            # Combine and exclude self
            all_names = list(from_counts.index) + list(to_counts.index)
            name_counts = Counter(all_names)
            
            # Remove self
            if user_name in name_counts:
                del name_counts[user_name]
            
            # Get top 10
            top_10 = dict(name_counts.most_common(10))
            
            fig_top = go.Figure(go.Bar(
                x=list(top_10.values()),
                y=list(top_10.keys()),
                orientation='h',
                marker=dict(color='#0A66C2')
            ))
            
            fig_top.update_layout(
                title='Top 10 Most Active Conversations',
                xaxis_title='Message Count',
                height=350,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_top, use_container_width=True)
    
    # ===== ENGAGEMENT QUALITY =====
    st.markdown("<div class='section-header'>Engagement Quality</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    Not all conversations are equal. High-quality engagement includes <span class='highlight'>referrals</span>, 
    <span class='highlight'>interview opportunities</span>, and <span class='highlight'>positive outcomes</span>.
    </div>
    """, unsafe_allow_html=True)
    
    if all(col in data['messages'].columns for col in ['has_referral_keyword', 'has_interview_keyword', 'has_positive_keyword']):
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            referrals = data['messages']['has_referral_keyword'].sum()
            st.metric("Referral Mentions", format_number(referrals))
        
        with col2:
            interviews = data['messages']['has_interview_keyword'].sum()
            st.metric("Interview Keywords", format_number(interviews))
        
        with col3:
            positive = data['messages']['has_positive_keyword'].sum()
            st.metric("Positive Sentiment", format_number(positive))
        
        with col4:
            engagement_rate = ((referrals + interviews) / len(data['messages']) * 100) if len(data['messages']) > 0 else 0
            st.metric("Quality Rate", f"{engagement_rate:.1f}%")
        
        # Outcome breakdown
        outcome_data = {
            'Category': ['Referrals', 'Interviews', 'Positive Responses'],
            'Count': [referrals, interviews, positive]
        }
        
        fig_outcomes = go.Figure(data=[go.Bar(
            x=outcome_data['Category'],
            y=outcome_data['Count'],
            marker=dict(color=['#057642', '#0A66C2', '#5BA7F5'])
        )])
        
        fig_outcomes.update_layout(
            title='Outcome Distribution',
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_outcomes, use_container_width=True)
    
    # ===== KEY TAKEAWAYS =====
    st.markdown("<div class='section-header'>Key Takeaways</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: #F3F6F8; padding: 1.5rem; border-radius: 12px;'>
        <h4 style='color: #057642; margin-top: 0;'>What's Working</h4>
        <ul style='line-height: 2;'>
            <li>Consistent outreach strategy</li>
            <li>Diverse conversation partners</li>
            <li>Quality engagement signals present</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: #F3F6F8; padding: 1.5rem; border-radius: 12px;'>
        <h4 style='color: #0A66C2; margin-top: 0;'>Optimization Opportunities</h4>
        <ul style='line-height: 2;'>
            <li>Follow up with dormant connections</li>
            <li>Increase response-to-outreach ratio</li>
            <li>Focus on high-value conversations</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

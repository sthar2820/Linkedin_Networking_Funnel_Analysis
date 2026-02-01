"""
LinkedIn Networking Analytics Dashboard
Premium storytelling dashboard - Main page
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from data_loader import DataLoader, MetricsCalculator, format_number, format_percentage

# Page config
st.set_page_config(
    page_title="LinkedIn Networking Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    /* Premium color scheme - LinkedIn inspired */
    :root {
        --primary-color: #0A66C2;
        --secondary-color: #004182;
        --success-color: #057642;
        --warning-color: #F5B800;
        --background: #FFFFFF;
        --surface: #F3F6F8;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Premium card styling */
    .metric-card {
        background: linear-gradient(135deg, #0A66C2 0%, #004182 100%);
        padding: 0.75rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0A66C2;
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 3px solid #0A66C2;
    }
    
    /* Story text */
    .story-text {
        font-size: 1rem;
        line-height: 1.6;
        color: #2C2C2C;
        margin: 0.75rem 0;
    }
    
    .highlight {
        color: #0A66C2;
        font-weight: 600;
    }
    
    /* Info boxes */
    .info-box {
        background: #F3F6F8;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 4px solid #0A66C2;
        margin: 0.5rem 0;
    }
    
    /* Streamlit metric override */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_all_data():
    """Load all datasets with caching"""
    loader = DataLoader()
    return {
        'invitations': loader.load_invitations(),
        'connections': loader.load_connections(),
        'messages': loader.load_messages()
    }


def main():
    # Load data
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
    
    # Calculate metrics
    calc = MetricsCalculator()
    funnel_metrics = calc.calculate_funnel_metrics(
        data['invitations'], 
        data['connections'], 
        data['messages']
    )
    
    # ===== HERO SECTION =====
    st.markdown("<h1 style='text-align: center; color: #0A66C2; font-size: 3rem; margin-bottom: 0;'>LinkedIn Networking Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;'>Data-Driven Analysis of Professional Networking Effectiveness</p>", unsafe_allow_html=True)
    
    # ===== THE STORY INTRODUCTION =====
    st.markdown("<div class='section-header'>The Story</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='story-text'>
    Professional networking is often treated as a numbers game—send enough connection requests, 
    and success will follow. But <span class='highlight'>what if we could measure it scientifically?</span>
    
    <br><br>
    
    This dashboard analyzes <span class='highlight'>{format_number(len(data['invitations']))}</span> LinkedIn interactions 
    to uncover patterns in networking effectiveness. By treating networking as a measurable funnel, 
    we can identify what works, what doesn't, and how to optimize for better outcomes.
    
    <br><br>
    
    <strong>The Question:</strong> Does strategic networking actually lead to meaningful professional outcomes?
    <br>
    <strong>The Answer:</strong> Let the data tell the story.
    </div>
    """, unsafe_allow_html=True)
    
    # ===== KEY INSIGHTS (Top-level metrics) =====
    st.markdown("<div class='section-header'>Key Performance Indicators</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Outreach Attempts",
            value=format_number(funnel_metrics['invitations_sent']),
            delta="Connection requests sent"
        )
    
    with col2:
        st.metric(
            label="Connections Made",
            value=format_number(funnel_metrics['connections_made']),
            delta=f"{funnel_metrics['acceptance_rate']:.1f}% acceptance rate",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="Conversations",
            value=format_number(funnel_metrics['conversations']),
            delta=f"{funnel_metrics['message_rate']:.1f}% messaged",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Positive Outcomes",
            value=format_number(funnel_metrics['outcomes']),
            delta=f"{funnel_metrics['outcome_rate']:.1f}% success rate",
            delta_color="normal"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== THE NETWORKING FUNNEL =====
    st.markdown("<div class='section-header'>The Networking Funnel</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    Every successful professional relationship follows a predictable journey. 
    Understanding this funnel reveals where efforts pay off—and where they don't.
    </div>
    """, unsafe_allow_html=True)
    
    # Funnel visualization
    funnel_data = {
        'Stage': ['Invitations Sent', 'Connections Made', 'Conversations Started', 'Positive Outcomes'],
        'Count': [
            funnel_metrics['invitations_sent'],
            funnel_metrics['connections_made'],
            funnel_metrics['conversations'],
            funnel_metrics['outcomes']
        ],
        'Percentage': [100, 
                      funnel_metrics['acceptance_rate'],
                      funnel_metrics['message_rate'],
                      funnel_metrics['outcome_rate']]
    }
    
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(
            color=['#0A66C2', '#1B75D0', '#3B8FE8', '#5BA7F5'],
            line=dict(width=0)
        ),
        connector=dict(line=dict(color="white", width=3))
    ))
    
    fig_funnel.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14, color='#2C2C2C')
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # ===== FUNNEL INSIGHTS =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='info-box'>
        <h3 style='color: #0A66C2; margin-top: 0;'>Conversion Insights</h3>
        <ul style='line-height: 2;'>
            <li><strong>{:.1f}%</strong> of invitations convert to connections</li>
            <li><strong>{:.1f}%</strong> of connections lead to conversations</li>
            <li><strong>{:.1f}%</strong> of conversations yield positive outcomes</li>
        </ul>
        </div>
        """.format(
            funnel_metrics['acceptance_rate'],
            funnel_metrics['message_rate'],
            funnel_metrics['outcome_rate']
        ), unsafe_allow_html=True)
    
    with col2:
        # Calculate overall efficiency
        overall_efficiency = (funnel_metrics['outcomes'] / funnel_metrics['invitations_sent'] * 100) if funnel_metrics['invitations_sent'] > 0 else 0
        
        st.markdown(f"""
        <div class='info-box'>
        <h3 style='color: #057642; margin-top: 0;'>Overall Efficiency</h3>
        <p style='font-size: 2.5rem; font-weight: 700; color: #057642; margin: 1rem 0;'>{overall_efficiency:.2f}%</p>
        <p>Every 100 connection requests result in approximately <strong>{int(overall_efficiency * 100 / 100)}</strong> meaningful professional outcomes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== NETWORK GROWTH TIMELINE =====
    st.markdown("<div class='section-header'>Network Growth Over Time</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    Consistency matters. This timeline shows how strategic, sustained networking 
    compounds over time to build a valuable professional network.
    </div>
    """, unsafe_allow_html=True)
    
    # Time series for invitations
    if len(data['invitations']) > 0:
        ts_data = calc.calculate_time_series(data['invitations'], 'sent_at', freq='M')
        
        fig_timeline = go.Figure()
        
        # Add bars for monthly activity
        fig_timeline.add_trace(go.Bar(
            x=ts_data['period'],
            y=ts_data['count'],
            name='Monthly Invitations',
            marker_color='#0A66C2',
            yaxis='y'
        ))
        
        # Add line for cumulative growth
        fig_timeline.add_trace(go.Scatter(
            x=ts_data['period'],
            y=ts_data['cumulative'],
            name='Cumulative Total',
            mode='lines+markers',
            line=dict(color='#057642', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig_timeline.update_layout(
            height=400,
            xaxis=dict(title='Month', tickangle=-45),
            yaxis=dict(title=dict(text='Monthly Invitations', font=dict(color='#0A66C2'))),
            yaxis2=dict(
                title=dict(text='Cumulative Total', font=dict(color='#057642')),
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#2C2C2C')
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # ===== WHAT'S NEXT =====
    st.markdown("<div class='section-header'>Dive Deeper</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: #F3F6F8; border-radius: 12px;'>
        <h3 style='color: #0A66C2;'>Network Insights</h3>
        <p>Analyze connection patterns, industries, and relationship strength</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: #F3F6F8; border-radius: 12px;'>
        <h3 style='color: #0A66C2;'>Message Analysis</h3>
        <p>Understand response rates, timing, and conversation quality</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: #F3F6F8; border-radius: 12px;'>
        <h3 style='color: #0A66C2;'>Optimization Tips</h3>
        <p>Data-driven recommendations to improve networking ROI</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ===== FOOTER =====
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem; border-top: 1px solid #E0E0E0; margin-top: 3rem;'>
    <p>Built with Python • Streamlit • Plotly</p>
    <p style='font-size: 0.9rem;'>Data analyzed from LinkedIn export • All personal information anonymized</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

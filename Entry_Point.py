import streamlit as st
from datetime import datetime
import pandas as pd

# Configure page with custom title and wide layout
st.set_page_config(
    page_title="StockMuze | Financial Analytics Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1.5rem;
    }
    .feature-header {
        font-size: 1.2rem;
        color: #1E88E5;
        font-weight: 600;
        margin-top: 1rem;
    }
    .feature-box {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;

    }
    .tech-badge {
        background-color: #e1f5fe;
        color: #0288d1;
        padding: 5px 10px;
        border-radius: 15px;
        margin-right: 5px;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 5px;
    }
    .github-link {
        text-decoration: none;
        color: #424242;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        transition: color 0.3s;
    }
    .github-link:hover {
        color: #1E88E5;
    }
    .footer {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e0e0e0;
        text-align: center;
        color: #757575;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<div class="main-header">StockMuze: Financial Analytics Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Empowering investors with data-driven insights and visualization tools</div>', unsafe_allow_html=True)

# GitHub link
col1, col2 = st.columns([0.85, 0.15])
with col2:
    st.markdown('''
    <a href="https://github.com/shiv060600/StockMuze" class="github-link" target="_blank">
        <svg height="24" width="24" viewBox="0 0 16 16" fill="currentColor" style="vertical-align: middle; margin-right: 6px;">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
        </svg>
        GitHub Repository
    </a>
    ''', unsafe_allow_html=True)

# App introduction
st.markdown("""
This platform provides comprehensive stock market analytics with real-time data, historical analysis, 
and news sentiment. Navigate using the sidebar to explore different features.
""")

# Main features section
st.markdown('<div class="feature-header">Platform Features</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('''
    <div class="feature-box">
        <h3>📊 Historical Stock Data Analysis</h3>
        <p>Access and visualize historical stock performance with customizable date ranges. Analyze trends, patterns, 
        and key metrics to inform your investment decisions.</p>
        <p><b>Key capabilities:</b> Date range selection, multiple technical indicators, comparative analysis</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="feature-box">
        <h3>📰 News Sentiment Analysis</h3>
        <p>Stay informed with the latest market news and sentiment analysis. Our platform aggregates news from trusted 
        sources and applies natural language processing to gauge market sentiment.</p>
        <p><b>Key capabilities:</b> Real-time news aggregation, sentiment scoring, relevance filtering</p>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown('''
    <div class="feature-box">
        <h3>📈 Real-Time Market Data</h3>
        <p>Monitor current stock prices, market indicators, and trading volumes. Get timely insights into market movements
        and make informed decisions based on up-to-date information.</p>
        <p><b>Key capabilities:</b> Live price updates, market indicators, volume analysis</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="feature-box">
        <h3>🧮 Options Analytics</h3>
        <p>Explore options pricing models and strategies. Visualize payoff diagrams, calculate theoretical prices, 
        and understand the risk-reward profiles of different options strategies.</p>
        <p><b>Key capabilities:</b> Black-Scholes modeling, payoff visualization, strategy analysis</p>
    </div>
    ''', unsafe_allow_html=True)

# Technology stack section
st.markdown('<div class="feature-header">Technology Stack</div>', unsafe_allow_html=True)
st.markdown('''
<div style="margin-top: 10px;">
    <span class="tech-badge">Python</span>
    <span class="tech-badge">Streamlit</span>
    <span class="tech-badge">Pandas</span>
    <span class="tech-badge">NumPy</span>
    <span class="tech-badge">Plotly</span>
    <span class="tech-badge">Yfinance</span>
    <span class="tech-badge">Alpha Vantage API</span>
    <span class="tech-badge">SQLite</span>
</div>
''', unsafe_allow_html=True)

# How to use section
st.markdown('<div class="feature-header">How to Navigate</div>', unsafe_allow_html=True)
st.markdown("""
1. **Use the sidebar** to navigate between different analytics tools
2. **Select stocks** by entering ticker symbols (e.g., AAPL, MSFT, GOOGL)
3. **Customize date ranges** to focus on specific time periods
4. **Interact with visualizations** to drill down into specific data points
5. **Export data** for further analysis or reporting
""")

# Call to action
st.markdown("""
## Get Started
Select a feature from the sidebar menu to begin exploring the financial markets.
""")

# Example ticker showcase
st.markdown('<div class="feature-header">Popular Tickers</div>', unsafe_allow_html=True)
popular_tickers = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com, Inc.",
    "TSLA": "Tesla, Inc.",
    "META": "Meta Platforms, Inc."
}

ticker_df = pd.DataFrame(popular_tickers.items(), columns=["Ticker", "Company"])
st.dataframe(ticker_df, use_container_width=True, hide_index=True)

# Footer
st.markdown('''
<div class="footer">
    <p>StockMuze © 2023 | Created by Shiv Bhutani</p>
    <p>This application is for educational and demonstration purposes only. It is not financial advice.</p>
</div>
''', unsafe_allow_html=True)



    
    


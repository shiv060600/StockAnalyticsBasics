import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker
from apis.get_stock_data_range import get_stock_data_range
import streamlit.components.v1 as components
import datetime
import mpld3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os 
import sqlitecloud
load_dotenv()
CLOUD_DB = os.getenv("DB_KEY")
st.set_page_config(page_title="Stock Data By Range", layout="wide")

#DATABASE_NAME = "stock_data.db"
DATABASE_NAME = CLOUD_DB


st.markdown("""
<style>
    .header-container {
        background-color: #141b4a;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color:#05050;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .plotly-chart {
        border-radius: 0.5rem;
        /* background-color: #141b4a */;
        padding: 1rem;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .small-text {
        font-size: 0.8rem;
        color: #6c757d;
    }
    [data-testid="stMetricValue"] {
        font-weight: bold;
        color: #1E88E5;
    }
    .header-container h1 {
        color: #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <h1>Stock Data Analysis By Date Range</h1>
    <p>Analyze historical stock performance over your chosen time period with interactive charts and key metrics.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
with col1:
    ticker = st.text_input("Enter a ticker:", "AAPL")

with col2:
    date_range = date_range_picker("Choose a date range:", None, None)
    start_date = date_range[0].strftime("%Y-%m-%d")
    end_date = date_range[1].strftime("%Y-%m-%d")

st.markdown("---")

@st.cache_data(ttl=3600)
def get_stock_data(stockTicker, start, end):
    return get_stock_data_range(stockTicker, start, end)

with st.spinner(f"Loading data for {ticker}..."):
    #conn = sqlitecloud.connect(DATABASE_NAME)
    #cursor = conn.cursor()

    try:
        #cursor.execute("SELECT * FROM StockPrices WHERE date BETWEEN ? AND ? AND ticker = ?", (start_date, end_date, ticker))
        #data = cursor.fetchall()
        
        stock_df = get_stock_data(ticker, start_date, end_date)
            
        #else:
            #st.info("Data loaded from database")
            #stock_df = pd.DataFrame(data, columns=['date', 'ticker', 'open', 'high', 'low', 'volume', 'close'])
            #stock_df.set_index('date', inplace=True)"""

        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            stock_df[col] = pd.to_numeric(stock_df[col])
        
        stock_df['average_price'] = (stock_df['open'] + stock_df['close']) / 2
        stock_df['daily_change'] = stock_df['close'] - stock_df['open']
        stock_df['daily_pct_change'] = (stock_df['close'] - stock_df['open']) / stock_df['open']
        stock_df['MA20'] = stock_df['close'].rolling(window=20).mean()
        stock_df['MA50'] = stock_df['close'].rolling(window=50).mean()

        st.markdown("<div class ='metric-container'>", unsafe_allow_html= True)

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        overall_change = stock_df['close'].iloc[-1] - stock_df['close'].iloc[0]
        overall_pct_change = (overall_change / stock_df['close'].iloc[0]) * 100

        volatility = stock_df['daily_pct_change'].std()
        avg_volume = stock_df['volume'].mean() 

        highest_price = stock_df['high'].max()
        lowest_price = stock_df['low'].min()

        with metric_col1:
            st.metric(
                    label="Overall Change",
                    value=f"${round(overall_change, 2)}",
                    delta=f"{round(overall_pct_change, 2)}%"
                )
                
        with metric_col2:
            st.metric(
                    label="Price Range",
                    value=f"${round(lowest_price, 2)} - ${round(highest_price, 2)}",
                    delta=f"Spread: ${round(highest_price - lowest_price, 2)}"
                )
                
        with metric_col3:
                st.metric(
                    label="Volatility",
                    value=f"{round(volatility, 2)}%",
                    delta=f"Avg Vol: {int(avg_volume):,}"
                )
                
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='plotly-chart'>", unsafe_allow_html=True)

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=stock_df.index,
                y=stock_df['close'],
                mode='lines',
                name='Price',
                line=dict(color='#1E88E5', width=2),
                hovertemplate='Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'
            )
        )


        fig.update_layout(
            title=f'{ticker} Stock Price ({start_date} to {end_date})',
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, b=40, t=80),
            hovermode="x unified",
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(230, 230, 230, 0.8)'
            )
        )

        fig.update_xaxes(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all", label = "Chosen Range")
                ]),
                bgcolor="#050505",
                activecolor="#141b4a",
                x=0.01,
                y=1.01,
            ),
            rangeslider=dict(visible=True, thickness=0.05),
            type="date"
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Chart Options"):
            chart_options = st.columns(2)
            
            with chart_options[0]:
                show_daily = st.checkbox("Show Daily Changes", value=False)
                
            with chart_options[1]:
                show_volume = st.checkbox("Show Trading Volume", value=False)
            
            if show_daily:
                daily_fig = go.Figure()
                daily_fig.add_trace(
                    go.Bar(
                        x=stock_df.index,
                        y=stock_df['daily_pct_change'] * 100,
                        name="Daily Change %",
                        marker_color=["#EF5350" if x < 0 else "#26A69A" for x in stock_df['daily_pct_change']],
                        hovertemplate='Date: %{x}<br>Change: %{y:.2f}%<extra></extra>'
                    )
                )
                daily_fig.update_layout(
                    title="Daily Price Changes (%)",
                    height=250,
                    margin=dict(l=40, r=40, b=20, t=40),
                    xaxis_rangeslider_visible=False,
                    yaxis_title="Change (%)"
                )
                st.plotly_chart(daily_fig, use_container_width=True)
                
            if show_volume:
                volume_fig = go.Figure()
                volume_fig.add_trace(
                    go.Bar(
                        x=stock_df.index,
                        y=stock_df['volume'],
                        name="Volume",
                        marker_color="rgba(100, 100, 250, 0.5)",
                        hovertemplate='Date: %{x}<br>Volume: %{y:,}<extra></extra>'
                    )
                )
                volume_fig.update_layout(
                    title="Trading Volume",
                    height=250,
                    margin=dict(l=40, r=40, b=20, t=40),
                    xaxis_rangeslider_visible=False,
                    yaxis_title="Volume"
                )
                st.plotly_chart(volume_fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)
        
        with st.expander("View Data Table"):
            st.dataframe(
                stock_df[['open', 'high', 'low', 'close', 'volume', 'daily_pct_change']].style.format({
                    'open': '${:.2f}',
                    'high': '${:.2f}',
                    'low': '${:.2f}',
                    'close': '${:.2f}',
                    'volume': '{:,.0f}',
                    'daily_pct_change': '{:.2f}%'
                }),
                height=300
            )
                
    except Exception as e:
        st.error(f"Error: {e}")
    

st.markdown("---")
st.markdown(
    "<div class='small-text'>Data sourced via Yahoo Finance. Past performance is not indicative of future results.</div>",
    unsafe_allow_html=True
)
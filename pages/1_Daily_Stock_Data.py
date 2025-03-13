import streamlit as st 
from apis.get_current_price import get_current_price
from apis.get_historical_price import get_historical_price
from datetime import datetime, timedelta
import yfinance as yf
import pytz
import os
st.set_page_config(
    page_title="Stock Data",
    page_icon="📈",
    layout="wide",
)

# Simple CSS - only for the success/error boxes
st.markdown("""
<style>
    .success-box {
        background-color: #d4edda; 
        color: #155724; 
        padding: 10px; 
        border-radius: 5px; 
        font-weight: bold;
    }
    .error-box {
        background-color: #f8d7da; 
        color: #721c24; 
        padding: 10px; 
        border-radius: 5px; 
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Simple sidebar
st.sidebar.title("📈 Stock Parameters")
ticker = st.sidebar.text_input("Enter Ticker", "AAPL")
date = st.sidebar.date_input("Select Date (< 3 months prior)")

st.title("Daily Stock Dashboard")

with st.spinner("Loading stock data..."):
    try:
        ticker_info = yf.Ticker(ticker).info
        if 'longName' in ticker_info:
            st.subheader(f"{ticker_info['longName']} ({ticker})")
        if 'logo_url' in ticker_info:
            st.image(ticker_info['logo_url'], width=80)
    except:
        st.subheader(f"{ticker} Stock Data")
    
    # Market status indicator
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now(eastern)
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    is_weekday = now.weekday() < 5
    
    col1, col2 = st.columns([4, 1])
    with col2:
        if is_weekday and market_open <= now <= market_close:
            st.markdown("<div class='success-box'> Market is open</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='error-box'> Market is closed</div>", unsafe_allow_html=True)

    @st.cache_data
    def get_stock_data(tickerSymbol):
        return get_current_price(tickerSymbol)

    # Current date view
    if date == datetime.now().date():
        stock_row = get_stock_data(ticker)
        st.header("Current Stock Price")
        
        try:
            prev_day = get_historical_price(ticker, (datetime.now() - timedelta(days=1)).date())
            
            if prev_day["Open"] > 0:
                # Calculate percent changes
                open_change_pct = ((float(stock_row["Open"].iloc[0]) - float(prev_day["Open"])) / float(prev_day["Open"])) * 100
                low_change_pct = ((float(stock_row["Low"].iloc[0]) - float(prev_day["Low"])) / float(prev_day["Low"])) * 100
                high_change_pct = ((float(stock_row["High"].iloc[0]) - float(prev_day["High"])) / float(prev_day["High"])) * 100
                close_change_pct = ((float(stock_row["Close"].iloc[0]) - float(prev_day["Close"])) / float(prev_day["Close"])) * 100
                
                # Display metrics with percent changes
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Open", f"${round(float(stock_row['Open'].iloc[0]), 2)}",
                            delta=f"{round(open_change_pct, 2)}%")
                col2.metric("Low", f"${round(float(stock_row['Low'].iloc[0]), 2)}",
                            delta=f"{round(low_change_pct, 2)}%")
                col3.metric("High", f"${round(float(stock_row['High'].iloc[0]), 2)}",
                            delta=f"{round(high_change_pct, 2)}%")
                col4.metric("Close", f"${round(float(stock_row['Close'].iloc[0]), 2)}",
                            delta=f"{round(close_change_pct, 2)}%")
                col5.metric("Volume", f"{int(stock_row['Volume'].iloc[0]):,}")
            else:
                raise ValueError("Previous day data not available")
        except:
            # Simple metrics without comparison
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Open", f"${round(float(stock_row['Open'].iloc[0]), 2)}")
            col2.metric("Low", f"${round(float(stock_row['Low'].iloc[0]), 2)}")
            col3.metric("High", f"${round(float(stock_row['High'].iloc[0]), 2)}")
            col4.metric("Close", f"${round(float(stock_row['Close'].iloc[0]), 2)}")
            col5.metric("Volume", f"{int(stock_row['Volume'].iloc[0]):,}")
            
            st.info("Note: Previous day comparison not available")
        
        # Calculate daily change
        daily_change = float(stock_row["Close"].iloc[0]) - float(stock_row["Open"].iloc[0])
        daily_change_pct = (daily_change / float(stock_row["Open"].iloc[0])) * 100
        
        # Show the daily change in a colored box
        if daily_change > 0:
            st.markdown(f"<div class='success-box'>📈 Today's change: +${round(daily_change, 2)} ({round(daily_change_pct, 2)}%)</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='error-box'>📉 Today's change: ${round(daily_change, 2)} ({round(daily_change_pct, 2)}%)</div>", unsafe_allow_html=True)
            
    # Historical date view
    else:
        result = get_historical_price(ticker, date)
        st.header(f"Stock Price on {date.strftime('%A, %B %d, %Y')}")
        
        try:
            prev_date = date - timedelta(days=1)
            prev_day = get_historical_price(ticker, prev_date)
            
            if prev_day["Open"] > 0:
                # Calculate percent changes
                open_change_pct = ((float(result["Open"]) - float(prev_day["Open"])) / float(prev_day["Open"])) * 100
                low_change_pct = ((float(result["Low"]) - float(prev_day["Low"])) / float(prev_day["Low"])) * 100
                high_change_pct = ((float(result["High"]) - float(prev_day["High"])) / float(prev_day["High"])) * 100
                close_change_pct = ((float(result["Close"]) - float(prev_day["Close"])) / float(prev_day["Close"])) * 100
                
                # Display metrics 
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Open", f"${round(float(result['Open']), 2)}",
                            delta=f"{round(open_change_pct, 2)}%")
                col2.metric("Low", f"${round(float(result['Low']), 2)}",
                            delta=f"{round(low_change_pct, 2)}%")
                col3.metric("High", f"${round(float(result['High']), 2)}",
                            delta=f"{round(high_change_pct, 2)}%")
                col4.metric("Close", f"${round(float(result['Close']), 2)}",
                            delta=f"{round(close_change_pct, 2)}%")
                col5.metric("Volume", f"{int(result['Volume']):,}")
                
                # Show note if the date shown is different from the requested date
                if result["Date"].date() != date:
                    st.info(f"Note: Data shown is for {result['Date'].strftime('%A, %B %d, %Y')} (nearest trading day)")
            else:
                raise ValueError("Previous day data not available")
                
        except:
            # Simple metrics without comparison if no prev day
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Open", f"${round(float(result['Open']), 2)}")
            col2.metric("Low", f"${round(float(result['Low']), 2)}")
            col3.metric("High", f"${round(float(result['High']), 2)}")
            col4.metric("Close", f"${round(float(result['Close']), 2)}")
            col5.metric("Volume", f"{int(result['Volume']):,}")
            
            st.info("Note: Previous day comparison not available")
        
        #Net Gain/Loss
        if result["Open"] > 0:
            daily_change = float(result["Close"]) - float(result["Open"])
            daily_change_pct = (daily_change / float(result["Open"])) * 100
            
            if daily_change > 0:
                st.markdown(f"<div class='success-box'>📈 Day's change: +${round(daily_change, 2)} ({round(daily_change_pct, 2)}%)</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='error-box'>📉 Day's change: ${round(daily_change, 2)} ({round(daily_change_pct, 2)}%)</div>", unsafe_allow_html=True)
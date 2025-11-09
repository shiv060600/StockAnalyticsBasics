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

st.sidebar.title("📈 Stock Parameters")
ticker = st.sidebar.text_input("Enter Ticker", "AAPL")
date = st.sidebar.date_input("Select Date")

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

    if date == datetime.now().date():
        stock_row = get_stock_data(ticker)
        st.header("Current Stock Price")
        
        try:
            prev_day = get_historical_price(ticker, (datetime.now() - timedelta(days=1)).date())
            
            if prev_day["Open"] > 0:
                open_change_pct = ((stock_row["Open"] - prev_day["Open"]) / prev_day["Open"]) * 100
                low_change_pct = ((stock_row["Low"] - prev_day["Low"]) / prev_day["Low"]) * 100
                high_change_pct = ((stock_row["High"] - prev_day["High"]) / prev_day["High"]) * 100
                close_change_pct = ((stock_row["Close"] - prev_day["Close"]) / prev_day["Close"]) * 100
                volume_change_pct = ((stock_row["Volume"] - prev_day["Volume"]) / prev_day["Volume"]) * 100
                
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Open", f"${round(stock_row['Open'], 2)}",
                            delta=f"{round(open_change_pct, 2)}%")
                col2.metric("Low", f"${round(stock_row['Low'], 2)}",
                            delta=f"{round(low_change_pct, 2)}%")
                col3.metric("High", f"${round(stock_row['High'], 2)}",
                            delta=f"{round(high_change_pct, 2)}%")
                col4.metric("Close", f"${round(stock_row['Close'], 2)}",
                            delta=f"{round(close_change_pct, 2)}%")
                col5.metric("Volume", f"{int(stock_row['Volume']):,}",
                            delta=f"{round(volume_change_pct, 2)}%")
            else:
                raise ValueError("Previous day data not available")
        except:
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Open", f"${round(stock_row['Open'], 2)}")
            col2.metric("Low", f"${round(stock_row['Low'], 2)}")
            col3.metric("High", f"${round(stock_row['High'], 2)}")
            col4.metric("Close", f"${round(stock_row['Close'], 2)}")
            col5.metric("Volume", f"{int(stock_row['Volume']):,}")
            
            st.info("Note: Previous day comparison not available")
        
        daily_change = stock_row["Close"] - stock_row["Open"]
        daily_change_pct = (daily_change / stock_row["Open"]) * 100
        
        if daily_change > 0:
            st.markdown(f"<div class='success-box'>📈 Today's change: +${round(daily_change, 2)} ({round(daily_change_pct, 2)}%)</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='error-box'>📉 Today's change: ${round(daily_change, 2)} ({round(daily_change_pct, 2)}%)</div>", unsafe_allow_html=True)
            
    else:
        result = get_historical_price(ticker, date)
        st.header(f"Stock Price on {date.strftime('%A, %B %d, %Y')}")
        
        try:
            prev_date = date - timedelta(days=1)
            prev_day = get_historical_price(ticker, prev_date)
            
            if prev_day["Open"] > 0:
                open_change_pct = ((result["Open"] - prev_day["Open"]) / prev_day["Open"]) * 100
                low_change_pct = ((result["Low"] - prev_day["Low"]) / prev_day["Low"]) * 100
                high_change_pct = ((result["High"] - prev_day["High"]) / prev_day["High"]) * 100
                close_change_pct = ((result["Close"] - prev_day["Close"]) / prev_day["Close"]) * 100
                
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Open", f"${round(result['Open'], 2)}",
                            delta=f"{round(open_change_pct, 2)}%")
                col2.metric("Low", f"${round(result['Low'], 2)}",
                            delta=f"{round(low_change_pct, 2)}%")
                col3.metric("High", f"${round(result['High'], 2)}",
                            delta=f"{round(high_change_pct, 2)}%")
                col4.metric("Close", f"${round(result['Close'], 2)}",
                            delta=f"{round(close_change_pct, 2)}%")
                col5.metric("Volume", f"{int(result['Volume']):,}")
                
                # Check if result["Date"] is a scalar or has a date() method
                
            else:
                raise ValueError("Previous day data not available")
                
        except:
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Open", f"${round(result['Open'], 2)}")
            col2.metric("Low", f"${round(result['Low'], 2)}")
            col3.metric("High", f"${round(result['High'], 2)}")
            col4.metric("Close", f"${round(result['Close'], 2)}")
            col5.metric("Volume", f"{int(result['Volume']):,}")
            
            st.info("Note: Previous day comparison not available")
        
        if result["Open"] > 0:
            daily_change = result["Close"] - result["Open"]
            daily_change_pct = (daily_change / result["Open"]) * 100
            
            if daily_change > 0:
                st.markdown(f"<div class='success-box'>📈 Day's change: +${round(daily_change, 2)} ({round(daily_change_pct, 2)}%)</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='error-box'>📉 Day's change: ${round(daily_change, 2)} ({round(daily_change_pct, 2)}%)</div>", unsafe_allow_html=True)
    st.write("**Deltas under open low high close volume are pct change from prev day")

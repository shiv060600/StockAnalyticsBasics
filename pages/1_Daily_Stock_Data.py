import streamlit as st 
import sqlite3
from apis.get_current_price import get_current_price
from apis.get_historical_price import get_historical_price
from datetime import datetime
import yfinance

DATABASE_NAME = "stock_data.db"

st.set_page_config(page_title="Stock Data")
st.title("Real-Time Stock DashBoard")

ticker = st.text_input("Enter Ticker" , "AAPL")

date = st.date_input("Select Date (< 3 months prior)")
@st.cache_data
def get_stock_data(tickerSymbol):
    return get_current_price(tickerSymbol)

def get_data_day(tickerSymbol):
    return get_historical_price(tickerSymbol)
if date == datetime.now().date():
    stock_row = get_stock_data(ticker)
    st.title("Current Stock Metrics")
    col1,col2,col3,col4,col5 = st.columns(5) 
    col1.metric("Open", round(float(stock_row["Open"].iloc[0]),2))
    col2.metric("Low", round(float(stock_row["Low"].iloc[0]),2))
    col3.metric("High", round(float(stock_row["High"].iloc[0]),2))
    col4.metric("Close", round(float(stock_row["Close"].iloc[0]),2))
    col5.metric("Volume", int(stock_row["Volume"].iloc[0]))
else:
    result = get_historical_price(ticker,date)
    st.title(f"Stock Price on Date : {date}")
    col1,col2,col3,col4,col5 = st.columns(5) 
    col1.metric("Open", round(float(result["Open"]),2))
    col2.metric("Low", round(float(result["Low"]),2))
    col3.metric("High", round(float(result["High"]),2))
    col4.metric("Close", round(float(result["Close"]),2))
    col5.metric("Volume", int(result["Volume"]))


    



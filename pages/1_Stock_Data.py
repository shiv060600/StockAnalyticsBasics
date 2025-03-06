import streamlit as st 
import sqlite3
from apis.get_current_price import get_current_price

DATABASE_NAME = "stock_data.db"

st.set_page_config(page_title="Stock Data")
st.title("Real-Time Stock DashBoard")

ticker = st.text_input("Enter Ticker" , "AAPL")

date = st.date_input("Select Day (< 3 months prior)")


@st.cache_data
def get_stock_data(tickerSymbol):
    return get_current_price(tickerSymbol)
stock_row = get_stock_data(ticker)


st.title("Current Stock Metrics")
st.metric("Open", round(float(stock_row["Open"].iloc[0]),2))
st.metric("Low", round(float(stock_row["Low"].iloc[0]),2))
st.metric("High", round(float(stock_row["High"].iloc[0]),2))
st.metric("Close", round(float(stock_row["Close"].iloc[0]),2))



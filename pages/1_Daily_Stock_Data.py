import streamlit as st 
import sqlite3
from apis.get_current_price import get_current_price
from datetime import datetime

DATABASE_NAME = "stock_data.db"

st.set_page_config(page_title="Stock Data")
st.title("Real-Time Stock DashBoard")

ticker = st.text_input("Enter Ticker" , "AAPL")

date = st.date_input("Select Date (< 3 months prior)")

if date == datetime.now().date():
    @st.cache_data
    def get_stock_data(tickerSymbol):
        return get_current_price(tickerSymbol)
    stock_row = get_stock_data(ticker)


    st.title("Current Stock Metrics")
    col1,col2,col3,col4 = st.columns(4) 
    col1.metric("Open", round(float(stock_row["Open"].iloc[0]),2))
    col2.metric("Low", round(float(stock_row["Low"].iloc[0]),2))
    col3.metric("High", round(float(stock_row["High"].iloc[0]),2))
    col4.metric("Close", round(float(stock_row["Close"].iloc[0]),2))
else:
    st.write("Implement other logic")



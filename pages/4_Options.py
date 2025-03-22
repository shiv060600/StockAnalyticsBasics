import streamlit as st
import pandas as pd
import datetime
from apis.get_current_price import get_current_price

st.markdown("<h1 style = 'text-align : center;'> Put Call Parity </h1>",unsafe_allow_html=True)

use_real_data = st.sidebar.toggle("Use Realtime Stock Data",value= False)

st.sidebar.header("Options Parameters")
option_type = st.sidebar.radio("Option Type", ["Call", "Put"])


today = datetime.datetime.now().date()
expiry_date = st.sidebar.date_input("Expiration Date")

@st.cache_data
def get_current_price_data(ticker):
    return get_current_price(ticker)

if expiry_date < today:
    st.error("You cannot go back in time! Pick another date.")

if not use_real_data:
    K = st.sidebar.number_input("Strike Price")
    sigma = st.sidebar.slider("Volatility", min_value = 0.0, max_value = 1.0,step= 0.05)
    S = st.sidebar.number_input("Underlying Asset Price")
    r = st.sidebar.slider("Interest Rate", min_value = 0.01, max_value= 0.1,step=0.01)
    if option_type == "Call":
        st.write("call")
    elif option_type == "Put":
        st.write("Put")
else:
    ticker = st.sidebar.text_input("Enter Ticker","AAPL")
    current_prices = get_current_price_data(ticker)
    current_price_float = round(current_prices['Close'],3)
    K = st.sidebar.number_input("Strike Price")
    if option_type == "Call":
        st.write("call")
        st.write(f"curr price is {current_price_float}")
    elif option_type == "Put":
        st.write("Put")
        st.write(f"curr price is {current_price_float}")










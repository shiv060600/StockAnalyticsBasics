import pandas as pd
import yfinance
import streamlit as st

def get_historical_price(ticker , date1 ):
    try:
        df = yfinance.download(ticker, date = date1)
        df.reset_index(inplace=True)
        df.columns = ['date','open', 'high', 'low', 'close', 'volume']
        df.set_index('date',inplace= True)
        df["ticker"] = ticker
        return df
    except Exception as e:
        st.write(f"Exception: {e}")
        return None



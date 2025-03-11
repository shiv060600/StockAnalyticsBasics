import streamlit as st
from apis.news_api import get_news_data
import pandas as pd

st.set_page_config("Daily Stock News")

st.title("Stock News")
st.write("Daily stock news, articles over 70% relevancy are included.")
ticker = st.text_input("Enter Stock Ticker: ", "AAPL")

@st.cache_data
def get_news_df(tickerSymbol):
    return get_news_data(tickerSymbol)

news_df = get_news_df(ticker)

num_rows = news_df.shape[0]

for i in range(num_rows):
    row = news_df.iloc[i]
    title = row["title"]
    url = row["url"]
    summary = row["summary"]
    banner_image = row["banner_image"]
    st.image(banner_image, caption=title)
    st.write(f"**{title}**")
    st.write(f"Summary: {summary}")
    st.write(f"[Read more]({url})")
    st.write("---")







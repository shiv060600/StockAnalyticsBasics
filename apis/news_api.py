import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd
import streamlit as st

try:
    ALPHA_ADVANTAGE_API_KEY = st.secrets["ALPHA_ADVANTAGE_API_KEY"]
except Exception:
    # Fall back to environment variables if not in streamlit environment
    from dotenv import load_dotenv
    load_dotenv()
    ALPHA_ADVANTAGE_API_KEY = os.getenv("ALPHA_ADVANTAGE_API_KEY")
def get_news_data(stock_Symbol):
    try:
        news_list = []
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock_Symbol}&apikey={ALPHA_ADVANTAGE_API_KEY}"
        response = (requests.get(url)).json()
        print(response)
        feed_data = response["feed"]
        for article in feed_data:
            for ticker_sentiment in article["ticker_sentiment"]:
                if ticker_sentiment["ticker"] == stock_Symbol and float(ticker_sentiment["relevance_score"]) >= 0.70:
                    title = article["title"]
                    ticker_sentiment_score = ticker_sentiment["ticker_sentiment_score"]
                    time_published_str = article["time_published"]
                    date_published = datetime.strptime(time_published_str,"%Y%m%dT%H%M%S")
                    summary = article["summary"]
                    banner_image = article["banner_image"]
                    url = article["url"]
                    news_list.append(
                        {
                            "title" : title,
                            "ticker" : stock_Symbol,
                            "sentiment_score" : ticker_sentiment_score,
                            "date_published" : date_published.date,
                            "summary" : summary,
                            "banner_image" : banner_image,
                            "url" : url
                        }
                    )
        news_df = pd.DataFrame(news_list)
    except Exception as e:
        news_df = pd.DataFrame()
        print(f"Error fetching news: {e}")  
    return news_df

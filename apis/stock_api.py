
import requests 
#from get_time import get_time
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
ALPHA_ADVANTAGE_API_KEY = os.getenv("ALPHA_ADVANTAGE_API_KEY")
def get_stock_data(stock_Symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_Symbol}&apikey={ALPHA_ADVANTAGE_API_KEY}"
    response = (requests.get(url)).json()
    stock_data_df = pd.DataFrame.from_dict(response["Time Series (Daily)"], orient = "index")
    stock_data_df.index = pd.to_datetime(stock_data_df.index)
    stock_data_df.columns = ["open","high","low","close","volume"]
    stock_data_df["ticker"] = stock_Symbol
    return stock_data_df



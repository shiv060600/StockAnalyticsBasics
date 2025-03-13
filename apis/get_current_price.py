import requests 
import pandas as pd 
from datetime import datetime
from dotenv import load_dotenv
import yfinance
import os
import pytz
load_dotenv()
ALPHA_ADVANTAGE_API_KEY = os.getenv("ALPHA_ADVANTAGE_API_KEY")
def get_current_price(stockSymbol):
    eastern = pytz.timezone('US/Eastern')
    recent_data = yfinance.download(stockSymbol,period = "1d")
    #fallback_data = yfinance.download(stockSymbol,)
    #data = recent_data.loc[datetime.now(eastern).date().strftime("%Y-%m-%d")]
    data = recent_data.tail(1)
    return data



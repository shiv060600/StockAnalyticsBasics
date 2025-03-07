import requests 
import pandas as pd 
from datetime import datetime
from dotenv import load_dotenv
import yfinance
import os
load_dotenv()
ALPHA_ADVANTAGE_API_KEY = os.getenv("ALPHA_ADVANTAGE_API_KEY")
def get_current_price(stockSymbol):
    recent_data = yfinance.download(stockSymbol,period = "1d")
    return (recent_data.loc[datetime.now().date().strftime("%Y-%m-%d")])

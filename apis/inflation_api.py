import requests
from dotenv import load_dotenv
import pandas as pd
import os
load_dotenv()
ALPHA_ADVANTAGE_API_KEY = os.getenv("ALPHA_ADVANTAGE_API_KEY")

def get_inflation_data():
    url  = f"https://www.alphavantage.co/query?function=INFLATION&apikey={ALPHA_ADVANTAGE_API_KEY}"
    response = requests.get(url)
    inflation_data = (response.json())["data"]
    inflation_df = pd.DataFrame.from_dict(inflation_data)
    inflation_df = inflation_df.set_index("date")
    inflation_df.index = pd.to_datetime(inflation_df.index)
    return inflation_df


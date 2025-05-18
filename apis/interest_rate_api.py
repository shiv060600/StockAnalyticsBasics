import requests 
import os 
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
ALPHA_ADVANTAGE_API_KEY = os.getenv("ALPHA_ADVANTAGE_API_KEY")

def get_interest_rate_data():
    url = f"https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={ALPHA_ADVANTAGE_API_KEY}"
    response = (requests.get(url)).json()
    inflation_df = pd.DataFrame.from_dict(response["data"])
    inflation_df["value"] = pd.to_numeric(inflation_df["value"])
    inflation_df = inflation_df.rename(columns={"value":"interest rate"})
    inflation_df = inflation_df.set_index("date")
    inflation_df.index = pd.to_datetime(inflation_df.index)
    return inflation_df


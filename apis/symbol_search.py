import requests 
import os 
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
ALPHA_ADVANTAGE_API_KEY = os.getenv("ALPHA_ADVANTAGE_API_KEY")

def get_company_name(stock_symbol):
    response = requests.get(f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={stock_symbol}&apikey={ALPHA_ADVANTAGE_API_KEY}")
    response_json = response.json()
    data = response_json["bestMatches"]
    data_df = pd.DataFrame.from_dict(data)
    data_df.columns = ["symbol","name","type","region","marketOpen","marketClose","timezone","currency","matchScore"]
    condition = data_df["matchScore"] == 1
    result = data_df.loc[condition,["symbol","name"]]
    return result

import yfinance as yf
import pandas as pd
import datetime
import streamlit as st

def get_historical_price(ticker, date):
    try:
        date_str = date.strftime('%Y-%m-%d')
        start_date = date - datetime.timedelta(days=10)
        end_date = date 
        
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)

       
        
        if df.empty:
            st.warning(f"No data available for {ticker} around {date_str}")
            return {
                "Date": date,
                "Close": 0.0,
                "High": 0.0,
                "Low": 0.0,
                "Open": 0.0,
                "Volume": 0
            }
            
        if date_str not in df.index.strftime('%Y-%m-%d').tolist():
            valid_dates = df.index[df.index <= pd.Timestamp(date)]
            if not len(valid_dates):
                valid_dates = df.index
            closest_date = valid_dates[-1]
        else:
            closest_date = pd.Timestamp(date)
        row = df.loc[closest_date]
        price_data = {
            "Date": closest_date,
            "Close": float(row[("Close",ticker)]),
            "High": float(row[("High",ticker)]), 
            "Low": float(row[("Low",ticker)]),
            "Open": float(row[("Open",ticker)]),
            "Volume": int(row[("Volume",ticker)])
        }
        return price_data
    
    except Exception as e:
        st.error(f"Error fetching data for {ticker} on {date}: {e}")
        return {
            "Date": date,
            "Close": 0.0,
            "High": 0.0,
            "Low": 0.0,
            "Open": 0.0,
            "Volume": 0
        }

if __name__ == "__main__":
    print_df = get_historical_price("AAPL","2025-02-02")
    print()
    


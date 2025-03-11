import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker
from apis.get_stock_data_range import get_stock_data_range
import streamlit.components.v1 as components
import datetime
import mpld3

DATABASE_NAME = "stock_data.db"
load_dotenv()

# Page Configs
st.set_page_config(page_title="Stock Data By Range")
st.title("Stock Data By Range")

# User Inputs
ticker = st.text_input("Enter a ticker:", "AAPL")
date_range = date_range_picker("Choose a date range:", None, None)
start_date = date_range[0].strftime("%Y-%m-%d")
end_date = date_range[1].strftime("%Y-%m-%d")

# Define Stock DF function
@st.cache_data
def get_stock_data(stockTicker, start, end):
    return get_stock_data_range(stockTicker, start, end)

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM StockPrices WHERE date BETWEEN ? AND ? AND ticker = ?", (start_date, end_date, ticker))
    data = cursor.fetchall()
    if not data:
        stock_df = get_stock_data(ticker, start_date, end_date)
        if not stock_df.empty:
            stock_df.to_sql("StockPrices", conn, if_exists="append", index=True, index_label='date')
        else:
            st.write("No data fetched from the API.")
    else:
        st.write("Data found in the database.")
        stock_df = pd.DataFrame(data, columns=['date', 'ticker', 'open', 'high', 'low', 'volume', 'close'])
        stock_df['date'] = pd.to_datetime(stock_df['date'])
        stock_df.set_index('date', inplace=True)
        stock_df['open'] = pd.to_numeric(stock_df['open'])
        stock_df['close'] = pd.to_numeric(stock_df['close'])
        stock_df['average_price'] = (stock_df['open'] + stock_df['close']) / 2
        print(stock_df)
        
    if not stock_df.empty:
        # Calculate average prices
        
        
        # Plotting
        stock_plot = plt.figure(figsize=(15, 10))
        plt.plot(stock_df.index, stock_df['average_price'], label='Average Price' , color = "m")
        plt.xlabel('Date')
        plt.ylabel('Average Price')
        plt.title(f'Average Stock Prices for {ticker} from {start_date} to {end_date}')
        plt.legend()
        #plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
        st.pyplot(plt)
    else:
        st.write("No data available to plot.")

except Exception as e:
    st.write("Error:", e)
finally:
    conn.close()





import yfinance as yf
import streamlit as st
import datetime
def get_stock_data_range(ticker, start, end):
    try:
        res = yf.download(ticker, start=start, end=end, progress=True)
        print(res)
        res.reset_index(inplace= True)
        res.columns = ['date','open', 'high', 'low', 'close', 'volume']
        res.set_index("date", inplace= True)
        res["ticker"] = ticker
        return res
    except Exception as e:
        st.write(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    start_date = (datetime.datetime.now() - datetime.timedelta(days = 10)).strftime("%Y-%m-%d")
    end_date = (datetime.datetime.now()).strftime("%Y-%m-%d")

    result = get_stock_data_range("AAPL",start_date,end_date)
    print(result)



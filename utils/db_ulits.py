import sqlite3
from datetime import datetime


def stock_data_db_handler(db_name, stock_data_df):
    conn = sqlite3.connect(db_name)
    stock_data_df.to_sql("StocksPrices",conn,if_exists = "append", index = True)

def insert_stocks(db_name, stocks_df):
    conn = sqlite3.connect(db_name)
    stocks_df.to_sql("Stocks",conn,if_texts = "append", index = True)

def insert_news(db_name, news_df):
    conn = sqlite3.connect(db_name)
    news_df.tosql("News", conn, if_extists = "append", index = True)

def insert_interest_rate(db_name,interest_rate_df):
    conn = sqlite3.connect(db_name)
    interest_rate_df.tosql("InterestRate", conn, if_exists = "append", index = True)

def insert_inflation_data(db_name, inflation_df):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    current_year = datetime.now().year
    year_start = f"{current_year}-01-01"
    year_end = f"{current_year}-12-31"
    cursor.execute("""
    SELECT 1 FROM InflationRate WHERE date BETWEEN ? AND ?"
    """,(year_start,year_end))
    if cursor.fetchone() is None:
        cursor.execute("""""")
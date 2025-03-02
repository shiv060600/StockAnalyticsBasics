import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
from apis.stock_api import get_stock_data
from apis.news_api import get_news_data
from apis.inflation_api import get_inflation_data
from apis.interest_rate_api import get_interest_rate_data
from apis.symbol_search import get_company_name
import sqlitecloud
load_dotenv
DB_KEY = os.getenv("DB_KEY")
DATABASE_NAME = "stock_data.db"

def create_tables_if_not_exist(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Stocks (
                   ticker TEXT PRIMARY KEY,
                   company_name TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS StockPrices(
                   datetime TEXT,
                   ticker TEXT,
                   open REAL,
                   high REAL,
                   low REAL,
                   volume INTEGER,
                   PRIMARY KEY(date, ticker)
                   FOREIGN KEY (ticker) REFERENCES Stocks (ticker) 
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS News(
                   date TEXT
                   title TEXT,
                   ticker TEXT,
                   summary TEXT,
                   bannerimage TEXT,
                   PRIMARY KEY(summary,ticker)
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS InterestRate(
                date DATA,
                interestrate REAL
    )""")

def insert_stock_data(db_name, stock_data_df):
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

def db_load(stock_symbol): 
    #Load Dfs
    stock_data_df = get_stock_data(stock_symbol)
    news_data_df = get_news_data(stock_symbol)
    interest_rate_df = get_interest_rate_data(stock_symbol)
    stock_df = get_company_name(stock_symbol)

    #insert data into Sq3liteDb
    insert_stock_data(DATABASE_NAME,stock_data_df)
    insert_news(DATABASE_NAME,news_data_df)
    insert_interest_rate(DATABASE_NAME,interest_rate_df)
    insert_stocks(DATABASE_NAME,stock_df)














    

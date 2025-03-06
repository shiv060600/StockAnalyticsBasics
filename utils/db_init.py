import sqlite3
import pandas as pd
import os
from datetime import datetime
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
                   date TEXT,
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
                date TEXT,
                interestrate REAL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS InflationRate(
                   date TEXT,
                   inflation_rate REAL
    )""")


















    

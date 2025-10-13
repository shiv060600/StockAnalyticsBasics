import sqlite3
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
import sqlitecloud
load_dotenv()
DB_KEY = os.getenv("DB_KEY")
DATABASE_NAME = "stock_data.db"
#legacy
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
create_tables_if_not_exist(DATABASE_NAME)


















    

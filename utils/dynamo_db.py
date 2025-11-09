import boto3
import pandas as pd
import datetime
import os,sys
from dotenv import load_dotenv
from botocore.exceptions import ClientError, BotoCoreError
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.get_stock_data_range import get_stock_data_range
from decimal import Decimal
load_dotenv()


class DynamoDB:

    def __init__(self):
        self.AWS_PUBLIC_KEY = os.getenv("AWS_PUBLIC_KEY")
        self.AWS_PRIVATE_KEY = os.getenv("AWS_PRIVATE_KEY")
        self.AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
        self.dynamo_db_client: DynamoDBServiceResource = boto3.resource('dynamodb',region_name = self.AWS_DEFAULT_REGION,
                                            aws_secret_access_key = self.AWS_PRIVATE_KEY, aws_access_key_id = self.AWS_PUBLIC_KEY )
        self.table: Table = self.dynamo_db_client.Table('stock_prices')
        
    def get_data(self,start_date:datetime.datetime,end_date: datetime.datetime, ticker:str) -> pd.DataFrame:

        try:
            response = self.table.query(
                KeyConditionExpression =  Key('ticker').eq(ticker) & Key('date').between(start_date.strftime("%Y-%m-%d"),end_date.strftime("%Y-%m-%d"))
            )
        except BotoCoreError as bte:
            print(f"AWS connection error {bte}")
        except Exception as e:
            print(f"unexpected error occured {e}")


        if len(response['Items']) == 0:
            missing_dates = pd.date_range(start_date,end_date,freq='b').to_list()
            date_range = pd.date_range(start_date,end_date,freq='b').to_list()

            #need to fetch all data and insert it
            data_fetch = get_stock_data_range(ticker,start_date,end_date)
            for idx,row in data_fetch.iterrows():
                try:
                    insert = {
                        "ticker": ticker,
                        "date": idx.strftime("%Y-%m-%d"),  # idx is the date
                        "open": Decimal(str(row['open'])),
                        "high": Decimal(str(row['high'])),
                        "low": Decimal(str(row['low'])),
                        "close": Decimal(str(row['close'])),
                        "volume": int(row['volume'])
                    }
                    self._insert_item(item_to_insert = insert)
                except Exception as e:
                    print(f"failed to enter into dynamo{e}")

            return data_fetch

        if len(response['Items']) > 0:
            data = pd.DataFrame.from_records(response['Items'],index = 'date')

            date_range = pd.date_range(start_date,end_date,freq='b').to_list()
            existing_datetimes = [pd.to_datetime(x) for x in data.index.to_list()]

            #no missing dates means we don't need to fetch anything.
            missing_dates: list[datetime.datetime] = [date for date in date_range if date not in existing_datetimes]

            #If no missing dates return immediatly 
            if not missing_dates:
                return data
            else:
                data_fetch = get_stock_data_range(ticker,start_date,end_date)

                new_items = data_fetch[data_fetch.index.isin(missing_dates)]

                for idx,row in new_items.iterrows():
                    try:
                        insert =  {
                            "ticker": ticker,
                            "date": idx.strftime("%Y-%m-%d"),
                            "open": Decimal(str(row['open'])),
                            "high": Decimal(str(row['high'])),
                            "low": Decimal(str(row['low'])),
                            "close": Decimal(str(row['close'])),
                            "volume": int(row['volume'])
                        }
                        self._insert_item(item_to_insert = insert)

                    except Exception as e:
                        print(f"failed to enter into dynamo{e}")
            
            return_df = pd.concat([data,new_items])
            return return_df
        
    def _insert_item(self,item_to_insert:dict):
        try:
            self.table.put_item(Item = item_to_insert)
        except Exception as e:
            print(f"failed to insert item {e}")


        
    




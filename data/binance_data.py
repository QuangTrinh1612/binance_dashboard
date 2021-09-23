from binance.client import Client
import configparser
import pandas as pd
import datetime as dt

# Get API_KEY and SECRET_KEY from .ini file
config = configparser.ConfigParser()
config.read('keys.ini')
api_key = config['binance_api']['api_key']
secret_key = config['binance_api']['secret_key']

# Binance API Client
client = Client(api_key=api_key, api_secret=secret_key)

def get_historical_ohlc_data(symbol:str, start_str:str, end_str:str, interval:str) -> pd.DataFrame:
    '''
    Function: get_historical_ohlc_data

    Description:
        Returns historcal klines from past for given symbol and interval

    Parameters:
        symbol StringType
        start_str StringType
        end_str StringType
        interval StringType: Hardcode as 1 day 

    Returns:
        pandas.DataFrame: Price History Data (date as index and OHLC price) 
    '''
    price_df = pd.DataFrame(
        data = client.get_historical_klines(
            symbol = symbol
            , start_str = start_str
            , end_str = end_str
            , interval = interval
        )
        , columns = ['open_time','open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol','is_best_match']
    )
    price_df['open_date'] = [dt.date.fromtimestamp(x/1000) for x in price_df.open_time]
    price_df['symbol'] = symbol
    price_df = price_df.astype(
        {
            'symbol': str
            , 'volume': float
            , 'open': float
            , 'high': float
            , 'low': float
            , 'close': float
        }
    )
    return price_df[['symbol','open_date','open', 'high', 'low', 'close', 'volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol']]

def get_currency_pairs() -> list:
    '''
    Function: get_currency_pairs

    Description:
        Returns list of currency pairs which used in symbol slicer
    
    Returns:
        list: List of BNB Currency Pairs
    '''
    return list(
        map(
            lambda ticker: ticker['symbol']
            , filter(
                lambda ticker: ticker['symbol'].startswith('BNB')
                , client.get_all_tickers()
            )
        )
    )

def get_kline_intervals() -> dict:
    '''
    Function: get_kline_intervals

    Description:
        Returns list of kline intervals which used in interval slicer
    
    Returns:
        dict: Dictionray of posible kline intervals
    '''
    return [
        {'label': '12 Hours', 'value': '12h'}
        , {'label': '1 Day', 'value': '1d'}
        , {'label': '3 Days', 'value': '3d'}
        , {'label': '1 Week', 'value': '1w'}
        , {'label': '1 Month', 'value': '1M'}
    ]
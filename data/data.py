import yfinance as yf
import pandas as pd
from pandas_datareader import data as web
from functools import lru_cache

@lru_cache(maxsize=128)
def fetch_yfinance_data(symbol, start_date, end_date):
    """
    Fetch data from Yahoo Finance API using yfinance.
    Implements caching to reuse fetched data.
    """
    try:
        data = yf.download(symbol, start=start_date, end=end_date, interval='1d')
        return data
    except Exception as e:
        print(f"Error fetching data from Yahoo Finance API: {e}")
        return pd.DataFrame()

@lru_cache(maxsize=128)
def fetch_pandas_datareader_data(symbol, start_date, end_date):
    """
    Fetch data from Yahoo Finance API using pandas_datareader.
    Implements caching to reuse fetched data.
    """
    try:
        data = web.DataReader(symbol, 'yahoo', start_date, end_date)
        return data
    except Exception as e:
        print(f"Error fetching data from Pandas Datareader: {e}")
        return pd.DataFrame()

def get_live_data(symbol, start_date, end_date):
    """
    Fetch and combine data from multiple sources.
    Uses NumPy for efficient operations.
    """
    import numpy as np
    data_yf = fetch_yfinance_data(symbol, start_date, end_date)
    data_pdr = fetch_pandas_datareader_data(symbol, start_date, end_date)

    data = pd.concat([data_yf, data_pdr], axis=1, join='outer')
    data = data.ffill().bfill().dropna(subset=['Close'])

    # Convert to NumPy array for efficient operations
    data_np = data[['Open', 'High', 'Low', 'Close', 'Volume']].values.astype(np.float64)

    return data_np
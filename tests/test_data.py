import unittest
from data.data import fetch_yfinance_data, fetch_pandas_datareader_data, get_live_data

class TestDataModule(unittest.TestCase):
    def test_fetch_yfinance_data(self):
        # Test case for fetch_yfinance_data
        symbol = 'AAPL'
        start_date = '2022-01-01'
        end_date = '2022-12-31'
        data = fetch_yfinance_data(symbol, start_date, end_date)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)

    def test_fetch_pandas_datareader_data(self):
        # Test case for fetch_pandas_datareader_data
        symbol = 'AAPL'
        start_date = '2022-01-01'
        end_date = '2022-12-31'
        data = fetch_pandas_datareader_data(symbol, start_date, end_date)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)

    def test_get_live_data(self):
        # Test case for get_live_data
        symbol = 'AAPL'
        start_date = '2022-01-01'
        end_date = '2022-12-31'
        data = get_live_data(symbol, start_date, end_date)
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
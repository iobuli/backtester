import unittest
import backtrader as bt
from strategy.strategy import MyStrategy

class TestStrategyModule(unittest.TestCase):
    def test_my_strategy(self):
        # Test case for MyStrategy
        cerebro = bt.Cerebro()
        data = bt.feeds.YahooFinanceCSVData(dataname='path/to/data.csv')
        cerebro.adddata(data)
        cerebro.addstrategy(MyStrategy)
        cerebro.broker.setcash(100000)
        results = cerebro.run()
        self.assertIsNotNone(results)

if __name__ == '__main__':
    unittest.main()
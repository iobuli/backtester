import backtrader as bt
import numpy as np

class MyStrategy(bt.Strategy):
    params = (
        ('sma_period_short', 20),
        ('sma_period_long', 50),
        ('rr_ratio', 2),
        ('liquidity_sweep_window', 60),  # Time window in minutes to check for liquidity sweeps
        ('msb_window', 60),  # Time window in minutes to check for market sweep blocks
    )

    def __init__(self):
        self.data_close = self.datas[0].close
        self.sma_short = bt.indicators.SMA(self.data_close, period=self.params.sma_period_short)
        self.sma_long = bt.indicators.SMA(self.data_close, period=self.params.sma_period_long)
        self.signal = bt.indicators.CrossOver(self.sma_short, self.sma_long)
        self.order = None

    def next(self):
        if not self.position:
            if self.signal > 0:
                entry_price = self.data_close[0]
                stop_loss = self.find_swing_low(self.data_close, period=5)
                take_profit = entry_price + (entry_price - stop_loss) * self.params.rr_ratio
                self.order = self.buy(size=1, exectype=bt.Order.StopTrail, trailpercent=0.01,
                                      valid=bt.date2num(datetime.now() + timedelta(days=1)))
                self.order.addinfo(entry_price=entry_price, stop_loss=stop_loss, take_profit=take_profit)
        else:
            if self.order.executed.size > 0:
                entry_price = self.order.addinfo.entry_price
                stop_loss = self.order.addinfo.stop_loss
                take_profit = self.order.addinfo.take_profit
                data_low, data_high = self.data_low[0], self.data_high[0]
                if data_low <= stop_loss or data_high >= take_profit:
                    self.order = self.sell(size=self.position.size, exectype=bt.Order.Market)

    @staticmethod
    @np.vectorize
    def find_swing_low(data, period):
        """
        Vectorized implementation of find_swing_low function.
        """
        low = np.min(np.lib.stride_tricks.sliding_window_view(data, period)[:, ::period], axis=1)
        return low

    def notify_trade(self, trade):
        if trade.isclosed:
            dt = self.datas[0].datetime.date(trade.dtopen)
            print(f"{dt.strftime('%Y-%m-%d')}: OPERATION PROFIT {trade.pnl:.2f}, NET PROFIT {trade.pnlcomm:.2f}")

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Commission: {order.executed.comm:.2f}")
            elif order.issell():
                self.log(f"SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Commission: {order.executed.comm:.2f}")

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f"Order Canceled/Margin/Rejected: {order.status}")

        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.strftime('%Y-%m-%d')}: {txt}")
import backtrader as bt
from data.data import get_live_data
from strategy.strategy import MyStrategy
from analysis.analysis import analyze_market_events
from optimization.optimizer import optimize_strategy_params, optimize_strategy_params_optuna
from utils.logger import setup_logger
from utils.visualization import plot_equity_curve
from utils.performance import calculate_performance_metrics


def main():
    # Set up logger
    logger = setup_logger('backtesting_tool.log')

    # Fetch data
    symbol = 'AAPL'
    start_date = '2022-01-01'
    end_date = '2022-12-31'
    data = get_live_data(symbol, start_date, end_date)

    # Create a Cerebro entity
    cerebro = bt.Cerebro()

    # Add the data feed
    cerebro.adddata(data)

    # Add the strategy
    cerebro.addstrategy(MyStrategy)

    # Set initial capital
    initial_capital = 100000
    cerebro.broker.setcash(initial_capital)

    # Run the backtest
    logger.info('Running backtest...')
    results = cerebro.run()
    logger.info('Backtest completed.')

    # Analyze market events
    logger.info('Analyzing market events...')
    liquidity_sweeps, msb_events = analyze_market_events(data, 60, 60)
    logger.info(f'Liquidity sweeps: {liquidity_sweeps}')
    logger.info(f'Market sweep blocks: {msb_events}')

    # Optimize strategy parameters
    logger.info('Optimizing strategy parameters...')
    optimized_params_scipy = optimize_strategy_params(MyStrategy, data, initial_capital)
    logger.info(f'Optimized parameters (SciPy): {optimized_params_scipy}')

    optimized_params_optuna = optimize_strategy_params_optuna(MyStrategy, data, initial_capital)
    logger.info(f'Optimized parameters (Optuna): {optimized_params_optuna}')

    # Calculate performance metrics
    logger.info('Calculating performance metrics...')
    portfolio_value = cerebro.broker.getvalue()
    positions = results[0].tradelist
    performance_metrics = calculate_performance_metrics(positions, initial_capital)
    logger.info(f'Performance metrics: {performance_metrics}')

    # Plot equity curve
    logger.info('Plotting equity curve...')
    plot_equity_curve(positions)

if __name__ == '__main__':
    main()
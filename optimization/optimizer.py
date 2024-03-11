import scipy.optimize as optimize
import optuna

def optimize_strategy_params(strategy_class, data, initial_capital, population_size=100, iterations=100):
    """
    Optimize strategy parameters using SciPy's differential evolution algorithm.
    """
    bounds = [
        (10, 30),  # sma_period_short
        (40, 60),  # sma_period_long
        (1.5, 3.0),  # rr_ratio
        (30, 120),  # liquidity_sweep_window
        (30, 120),  # msb_window
    ]

    def fitness_function(params):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(strategy_class, sma_period_short=int(params[0]), sma_period_long=int(params[1]),
                            rr_ratio=params[2], liquidity_sweep_window=int(params[3]), msb_window=int(params[4]))
        cerebro.adddata(data)
        cerebro.broker.setcash(initial_capital)
        cerebro.addsizer(bt.sizers.FixedRizzer, stake=1)
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)
        results = cerebro.run()
        analyzer = results[0].analyzers.tradeanalyzer.get_analysis()
        return -analyzer.pnl.gross.sum()

    result = optimize.differential_evolution(fitness_function, bounds, popsize=population_size, maxiter=iterations)
    optimized_params = result.x
    return optimized_params

def optimize_strategy_params_optuna(strategy_class, data, initial_capital, n_trials=100):
    """
    Optimize strategy parameters using Optuna.
    """
    def objective(trial):
        sma_period_short = trial.suggest_int('sma_period_short', 10, 30)
        sma_period_long = trial.suggest_int('sma_period_long', 40, 60)
        rr_ratio = trial.suggest_float('rr_ratio', 1.5, 3.0)
        liquidity_sweep_window = trial.suggest_int('liquidity_sweep_window', 30, 120)
        msb_window = trial.suggest_int('msb_window', 30, 120)

        cerebro = bt.Cerebro()
        cerebro.addstrategy(strategy_class, sma_period_short=sma_period_short, sma_period_long=sma_period_long,
                            rr_ratio=rr_ratio, liquidity_sweep_window=liquidity_sweep_window, msb_window=msb_window)
        cerebro.adddata(data)
        cerebro.broker.setcash(initial_capital)
        cerebro.addsizer(bt.sizers.FixedRizzer, stake=1)
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)
        results = cerebro.run()
        analyzer = results[0].analyzers.tradeanalyzer.get_analysis()
        return -analyzer.pnl.gross.sum()

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=n_trials)
    optimized_params = study.best_params.values()
    return optimized_params
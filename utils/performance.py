import numpy as np

def calculate_performance_metrics(positions, initial_capital):
    """
    Calculate performance metrics based on the positions DataFrame.
    Uses NumPy for efficient computations.
    """
    profit_loss = positions['Profit_Loss'].values
    total_profit_loss = profit_loss.sum()
    win_count = np.count_nonzero(profit_loss > 0)
    loss_count = np.count_nonzero(profit_loss < 0)
    trade_count = len(positions)
    win_rate = win_count / trade_count if trade_count > 0 else 0
    max_drawdown = calculate_max_drawdown(positions, initial_capital)

    performance_metrics = {
        'Total Profit/Loss': total_profit_loss,
        'Win Count': win_count,
        'Loss Count': loss_count,
        'Trade Count': trade_count,
        'Win Rate': win_rate,
        'Maximum Drawdown': max_drawdown
    }

    return performance_metrics

def calculate_max_drawdown(positions, initial_capital):
    """
    Calculate the maximum drawdown based on the positions DataFrame.
    Uses NumPy for efficient computations.
    """
    equity = initial_capital
    max_equity = equity
    drawdown = 0
    max_drawdown = 0

    profit_loss = positions['Profit_Loss'].values
    equity_curve = np.cumprod(1 + profit_loss)
    max_equity = np.maximum.accumulate(equity_curve)
    drawdown = equity_curve / max_equity - 1
    max_drawdown = np.min(drawdown)

    return max_drawdown
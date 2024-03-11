import matplotlib.pyplot as plt

def plot_equity_curve(positions):
    """
    Plot the equity curve based on the positions DataFrame.
    """
    equity_curve = (1 + positions['Profit_Loss']).cumprod()
    plt.figure(figsize=(10, 6))
    plt.plot(equity_curve)
    plt.title('Equity Curve')
    plt.xlabel('Trade')
    plt.ylabel('Equity')
    plt.grid(True)
    plt.show()
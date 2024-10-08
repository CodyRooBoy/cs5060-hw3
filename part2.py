import numpy as np
import scipy.stats as stats

alpha = 9
beta = 10
shift = 0.35
volatility = 0.1704
drift = 0.03
days = 365
initial_stock_price = 100
num_simulations = 5000
risk_free_rate = 0.02

def simulate_price_paths(initial_price, alpha, beta, shift, volatility, drift, days, num_simulations):
    daily_returns = np.zeros((num_simulations, days))
    
    for i in range(num_simulations):
        for j in range(days):
            beta_return = stats.beta.rvs(alpha, beta) + shift
            daily_returns[i, j] = beta_return * (volatility / np.sqrt(252)) + (drift / 252)
    
    price_paths = np.zeros((num_simulations, days))
    price_paths[:, 0] = initial_price
    
    for i in range(num_simulations):
        for j in range(1, days):
            price_paths[i, j] = price_paths[i, j-1] * np.exp(daily_returns[i, j-1])
    
    return price_paths

price_paths = simulate_price_paths(initial_stock_price, alpha, beta, shift, volatility, drift, days, num_simulations)

K = 100
payoff = np.maximum(price_paths[:, -1] - K, 0)

option_price = np.exp(-risk_free_rate) * np.mean(payoff)

print(f"The estimated price of the European call option is: ${option_price:.2f}")

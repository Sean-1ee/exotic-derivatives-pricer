import numpy as np
import matplotlib.pyplot as plt

def simulate_gbm(S0, r, sigma, T, n_steps, n_simulations, seed=42):
    np.random.seed(seed)
    dt = T / n_steps
    Z = np.random.standard_normal((n_simulations, n_steps))
    returns = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    paths = np.zeros((n_simulations, n_steps + 1))
    paths[:, 0] = S0
    for t in range(1, n_steps + 1):
        paths[:, t] = paths[:, t-1] * np.exp(returns[:, t-1])
    return paths

def simulate_gbm_antithetic(S0, r, sigma, T, n_steps, n_simulations, seed=42):
    np.random.seed(seed)
    dt = T / n_steps
    half = n_simulations // 2
    Z = np.random.standard_normal((half, n_steps))
    Z_full = np.concatenate([Z, -Z], axis=0)
    returns = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z_full
    paths = np.zeros((n_simulations, n_steps + 1))
    paths[:, 0] = S0
    for t in range(1, n_steps + 1):
        paths[:, t] = paths[:, t-1] * np.exp(returns[:, t-1])
    return paths

def price_asian_call(paths, K, r, T):
    avg_prices = paths[:, 1:].mean(axis=1)
    payoffs = np.maximum(avg_prices - K, 0)
    discount = np.exp(-r * T)
    price = discount * payoffs.mean()
    std_error = discount * payoffs.std() / np.sqrt(len(payoffs))
    return price, std_error

if __name__ == "__main__":
    S0 = 100
    r = 0.05
    sigma = 0.2
    T = 1.0
    n_steps = 252
    n_sims = 1000
    K = 100

    paths = simulate_gbm(S0, r, sigma, T, n_steps, n_sims)

    print(f"Paths shape: {paths.shape}")
    print(f"Initial price: {paths[0, 0]:.2f}")
    print(f"Mean final price: {paths[:, -1].mean():.2f}")
    print(f"Std of final price: {paths[:, -1].std():.2f}")

    plt.figure(figsize=(12, 6))
    plt.plot(paths[:50].T, alpha=0.3, linewidth=0.8)
    plt.xlabel("Time Steps")
    plt.ylabel("Stock Price")
    plt.title("Simulated GBM Stock Price Paths")
    plt.savefig("paths.png", dpi=150)
    plt.close()
    print("Plot saved to paths.png")

    price, se = price_asian_call(paths, K, r, T)
    print(f"\nAsian Call Option Price: £{price:.4f}")
    print(f"Standard Error: £{se:.4f}")
    print(f"95% Confidence Interval: £{price - 1.96*se:.4f} to £{price + 1.96*se:.4f}")

    print("\nConvergence analysis:")
    print(f"{'Simulations':<15} {'Price':<10} {'Std Error':<12} {'CI Width'}")
    print("-" * 50)
    for n in [100, 500, 1000, 5000, 10000, 50000]:
        p = simulate_gbm(S0, r, sigma, T, n_steps, n, seed=42)
        price_n, se_n = price_asian_call(p, K, r, T)
        ci_width = 2 * 1.96 * se_n
        print(f"{n:<15} {price_n:<10.4f} {se_n:<12.4f} {ci_width:.4f}")

    print("\nVariance Reduction - Antithetic Variates:")
    print(f"{'Simulations':<15} {'Standard SE':<15} {'Antithetic SE':<15} {'Improvement'}")
    print("-" * 60)
    for n in [1000, 5000, 10000, 50000]:
        p_std = simulate_gbm(S0, r, sigma, T, n_steps, n, seed=42)
        _, se_std = price_asian_call(p_std, K, r, T)
        p_anti = simulate_gbm_antithetic(S0, r, sigma, T, n_steps, n, seed=42)
        _, se_anti = price_asian_call(p_anti, K, r, T)
        improvement = se_std / se_anti
        print(f"{n:<15} {se_std:<15.4f} {se_anti:<15.4f} {improvement:.2f}x")
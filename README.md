# Exotic Derivatives Pricing Engine

A Monte Carlo simulation framework for pricing exotic options and quantifying model risk, implemented in Python.

## Overview

This project implements a comprehensive pricing engine for exotic financial derivatives — options whose payoffs depend on complex conditions that make analytical solutions impossible. Monte Carlo simulation is used throughout, with a focus on variance reduction techniques and model risk analysis.

The project was motivated by a fascination with how mathematical uncertainty is priced in financial markets, complementing theoretical study of options through Akuna Capital's Options 101 course.

## Key Results

| Finding | Result |
|---------|--------|
| Monte Carlo convergence rate | Empirically verified 1/√N |
| Antithetic variates improvement | 0.96x — **ineffective** for path-dependent options |
| Control variates improvement | **36x** reduction in standard error |
| Model risk (Asian call) | +21.8% price difference GBM vs Jump Diffusion |
| Model risk (Knock-In call) | **+42.7%** price difference — largest effect |

## Options Implemented

### Asian Options
Payoff depends on the **average** stock price over the option's life rather than the final price. Used by companies hedging exposure to average commodity prices (e.g. airlines hedging fuel costs).

### Barrier Options
Option either activates (knock-in) or expires worthless (knock-out) if the stock price crosses a barrier level during the option's life. Cheaper than vanilla options due to the additional condition.

- **Up-and-Out Call:** Expires if price rises above barrier
- **Up-and-In Call:** Only activates if price rises above barrier
- Verified knock-in/knock-out parity numerically across all barrier levels

## Variance Reduction

A key limitation of Monte Carlo is slow 1/√N convergence. This project implements and compares two techniques:

**Antithetic Variates** — For every random path Z, simulate mirror path -Z. Found to be ineffective for Asian options because the path-dependent payoff is not monotone in the random shocks, so antithetic pairs lack sufficient negative correlation.

**Control Variates** — Uses the geometric average Asian option (which has a known analytical solution) as a control variate to correct the arithmetic average estimate. Achieves **36x improvement** in precision — equivalent to using 1,300x more simulations.

## Model Risk Analysis

Real stock prices exhibit fat tails and discontinuous jumps that standard Black-Scholes (GBM) cannot capture. This project compares pricing under:

- **GBM (Black-Scholes):** Continuous diffusion, log-normal returns
- **Merton Jump Diffusion:** Adds random Poisson-distributed jumps to GBM

Key finding: Model choice changes exotic option prices by **17% to 43%**, with opposite effects on different option types:
- Knock-out options are **cheaper** under jump diffusion (jumps more likely to trigger knock-out)
- Knock-in options are **more expensive** under jump diffusion (jumps more likely to activate option)
- Asian options are **more expensive** under jump diffusion (jumps increase path variability)

This quantifies the real-world risk of using the wrong model to price exotic derivatives.

## Project Structure
```
exotic-derivatives-pricer/
├── exotic_options_pricer.ipynb  # Main notebook with all analysis
├── gbm_simulation.png           # GBM path simulation and distribution
├── convergence.png              # Monte Carlo convergence analysis
├── variance_reduction.png       # Variance reduction comparison
├── barrier_options.png          # Barrier option prices and parity
├── model_comparison.png         # GBM vs jump diffusion distributions
└── model_risk.png               # Model risk quantification
```

## Setup
```bash
git clone https://github.com/Sean-1ee/exotic-derivatives-pricer.git
cd exotic-derivatives-pricer
pip install numpy scipy matplotlib jupyter
jupyter notebook exotic_options_pricer.ipynb
```

## Further Extensions
- Greeks calculation via finite differences (delta, gamma, vega)
- Stochastic volatility (Heston model)
- Calibration to real market option prices
- Importance sampling for deep out-of-the-money options

## Author
Sean Lee — MMathStat Mathematics and Statistics, University of Warwick  
[LinkedIn](https://linkedin.com/in/syseanlee) | [GitHub](https://github.com/Sean-1ee)
# Results Log

## 1. GBM Simulation
- 1000 paths simulated, daily steps over 1 year
- Starting price: £100, r=5%, sigma=20%
- Mean final price: £105.09 (expected ~£105 from drift)
- Std of final price: £20.77

## 2. Asian Call Option Pricing (K=100, T=1yr)
- Price estimate: £5.58
- Standard error: £0.25
- 95% CI: £5.10 to £6.07
- Note: cheaper than vanilla call (~£8-9) due to averaging smoothing volatility

## 3. Monte Carlo Convergence
| Simulations | Price  | Std Error | CI Width |
|-------------|--------|-----------|----------|
| 100         | 5.5604 | 0.7315    | 2.8673   |
| 500         | 5.9408 | 0.3589    | 1.4070   |
| 1000        | 5.5837 | 0.2466    | 0.9667   |
| 5000        | 5.6197 | 0.1107    | 0.4340   |
| 10000       | 5.6959 | 0.0789    | 0.3091   |
| 50000       | 5.7360 | 0.0356    | 0.1396   |

**Key insight:** Standard error halves when simulations quadruple — 
this is the 1/√n convergence rate. Motivates need for variance reduction.
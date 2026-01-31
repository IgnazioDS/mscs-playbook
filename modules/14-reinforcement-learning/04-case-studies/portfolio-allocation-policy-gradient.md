# Portfolio Allocation with Policy Gradient

## Problem and constraints
- Allocate portfolio weights across assets
- Manage risk and transaction costs
- Enforce leverage and drawdown limits

## MDP formulation (S, A, R, P, gamma)
- S: asset returns, volatility, and portfolio state
- A: continuous allocation weights
- R: risk-adjusted return minus transaction costs
- P: market dynamics with stochastic returns
- gamma: 0.95 for longer horizons

## Algorithm choice and why
- Policy gradient for continuous actions
- Actor-critic for variance reduction

## Training setup (env, reward, exploration)
- Market simulator with historical data
- Reward includes Sharpe ratio proxy
- Entropy regularization for exploration

## Evaluation plan
- Backtest on held-out periods
- Track Sharpe, drawdown, turnover
- Compare against benchmark portfolios

## Failure modes and mitigations
- Overfitting to historical data: use rolling validation
- Instability from high variance gradients: use baselines
- Excessive turnover: add transaction cost penalties

## What I would ship checklist
- [ ] Robust backtesting framework
- [ ] Risk constraints and monitoring
- [ ] Stress tests on market shocks
- [ ] Explainable policy reports
- [ ] Guardrails for maximum leverage

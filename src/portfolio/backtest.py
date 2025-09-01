import numpy as np
import pandas as pd

def long_top_quantile(prices_m: pd.DataFrame,
                      factor_scores: pd.DataFrame,
                      quantile: float = 0.8,
                      cost_bps: float = 5.0) -> pd.Series:
    """
    Monthly long-only top-quantile by factor. Equal-weight.
    prices_m: month-end prices (DataFrame)
    factor_scores: aligned with prices_m index/columns
    cost_bps: round-trip cost per rebalance (applied on weight turnover)
    Returns: portfolio equity curve (Series)
    """
    # Compute monthly returns
    rets = prices_m.pct_change().shift(-1)  # use next month returns after formation
    # Select top-quantile each month
    ranks = factor_scores.rank(axis=1, pct=True)
    picks = ranks >= quantile
    weights = picks.div(picks.sum(axis=1), axis=0).fillna(0.0)

    # Turnover & costs
    w_prev = weights.shift(1).fillna(0.0)
    turnover = (weights - w_prev).abs().sum(axis=1)
    tc = (cost_bps / 10000.0) * turnover  # linear costs

    # Portfolio returns (net of costs)
    port_rets = (weights * rets).sum(axis=1).fillna(0.0) - tc.fillna(0.0)
    equity = (1 + port_rets).cumprod()
    equity.name = "Portfolio"
    return equity

def summary_from_equity(equity: pd.Series) -> dict:
    r = equity.pct_change().dropna()
    ann_ret = (equity.iloc[-1] / equity.iloc[0]) ** (252*21/len(equity.index)) - 1 if len(equity)>2 else np.nan
    # For monthly equity, annualization factor ~12
    ann_ret = (1 + r.mean())**12 - 1
    ann_vol = r.std() * np.sqrt(12)
    sharpe = ann_ret / ann_vol if ann_vol and ann_vol > 0 else np.nan
    mdd = (equity / equity.cummax() - 1).min()
    return {"ann_return": ann_ret, "ann_vol": ann_vol, "sharpe": sharpe, "max_drawdown": mdd}

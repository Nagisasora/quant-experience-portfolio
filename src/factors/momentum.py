import pandas as pd
import numpy as np

def momentum_12_1(prices: pd.DataFrame, monthly=False) -> pd.DataFrame:
    """
    12-1 momentum: past 12 months excluding most recent month.
    If monthly=True, prices are already month-end; else assume daily.
    """
    if monthly:
        # shift by 1 month (exclude recent), 12 months window total
        return prices.shift(1) / prices.shift(12) - 1.0
    else:
        # daily approximation: 21 trading days ≈ 1 month, 252 ≈ 12 months
        return prices.shift(21) / prices.shift(252) - 1.0

def zscore(df, min_valid=5):
    # 1) how many non-NaN values per row (per date)
    cnt = df.notna().sum(axis=1)
    # 2) row-wise mean (cross-sectional mean each date), ignoring NaNs
    mu  = df.mean(axis=1, skipna=True)
    # 3) row-wise std, population (ddof=0) so it returns 0 when there's only 1 value
    #    then replace 0 with NaN so we never divide by zero
    sigma = df.std(axis=1, ddof=0, skipna=True).replace(0, np.nan)
    # 4) (x - mean) / std, broadcast across rows (axis=0 means align on index)
    z = df.sub(mu, axis=0).div(sigma, axis=0)
    # 5) if a row is too sparse (fewer than min_valid names), drop the whole row
    z[cnt < min_valid] = np.nan
    return z
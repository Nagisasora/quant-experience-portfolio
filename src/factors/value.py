import numpy as np
import pandas as pd
import yfinance as yf

def inverse_pe_snapshot(tickers):
    """
    Fetch trailing P/E via yfinance and return a Series of 1/PE as a simple value proxy.
    Note: fundamentals availability can be patchy on yfinance; handle gracefully.
    """
    vals = {}
    for t in tickers:
        try:
            info = yf.Ticker(t).fast_info  # fast_info has 'trailing_pe' in many cases
            pe = getattr(info, "trailing_pe", None)
            if pe is None:
                pe = yf.Ticker(t).info.get("trailingPE", None)  # fallback
            vals[t] = (1.0 / pe) if pe and pe > 0 else np.nan
        except Exception:
            vals[t] = np.nan
    return pd.Series(vals, name="inv_pe")
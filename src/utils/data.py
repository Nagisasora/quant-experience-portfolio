import pandas as pd
import yfinance as yf

def fetch_prices(tickers, start="2015-01-01", end=None, adj_close=True):
    """Download daily prices for a list of tickers from yfinance."""
    df = yf.download(tickers, start=start, end=end, auto_adjust=False, progress=False)["Adj Close" if adj_close else "Close"]
    # Ensure a 2D DataFrame even for single ticker
    if isinstance(df, pd.Series):
        df = df.to_frame()
    return df.dropna(how="all")

def to_month_end(prices: pd.DataFrame) -> pd.DataFrame:
    """Monthly sampling at month-end (last trading day)."""
    return prices.resample("M").last()

def pct_change(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change()


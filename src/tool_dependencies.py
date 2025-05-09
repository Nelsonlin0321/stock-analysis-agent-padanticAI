from typing import Optional
from src.schema import SymbolWithIncreasePercentage
from src.utils import exponential_retry
import yfinance as yf


@exponential_retry(retries=3)
def fetch_stock_percentage_increase(symbol)->Optional[SymbolWithIncreasePercentage]:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if not data.empty:
        open_price = data['Open'].iloc[0]
        close_price = data['Close'].iloc[0]
        percentage_increase = (
            (close_price - open_price) / open_price) * 100
        return SymbolWithIncreasePercentage(symbol=symbol, percentage=float(percentage_increase))

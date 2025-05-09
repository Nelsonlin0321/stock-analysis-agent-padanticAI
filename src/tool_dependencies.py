from src.utils import exponential_retry
import yfinance as yf


@exponential_retry(retries=3)
def fetch_stock_percentage_increase(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if not data.empty:
        open_price = data['Open'].iloc[0]
        close_price = data['Close'].iloc[0]
        percentage_increase = (
            (close_price - open_price) / open_price) * 100
        return {"symbol": symbol, "percentage_increase": float(percentage_increase)}


top_stock_with_percentage = max(
    stock_percentage_increase_list, key=lambda x: x['percentage_increase'])

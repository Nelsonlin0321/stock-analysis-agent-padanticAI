import pandas as pd
from tabulate import tabulate
from io import StringIO
import json
import random
from src.utils import multi_threading, logfire, exponential_retry
from typing import Optional
from src.schema import SymbolWithIncreasePercentage
import yfinance as yf


@exponential_retry(retries=3)
def fetch_stock_percentage_increase(symbol) -> Optional[SymbolWithIncreasePercentage]:
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if not data.empty:
        open_price = data['Open'].iloc[0]
        close_price = data['Close'].iloc[0]
        percentage_increase = (
            (close_price - open_price) / open_price) * 100
        return SymbolWithIncreasePercentage(symbol=symbol, percentage=float(percentage_increase))


def get_top_nasdaq_performance_stock() -> SymbolWithIncreasePercentage:
    """Get the top performance stock."""

    with open('./data/nasdaq_data.json', 'r') as f:
        nasdaq_data = json.load(f)
    nasdaq_data = random.sample(nasdaq_data, 100)  # Simulate a large dataset
    nasdaq_stock_symbols = [stock['Symbol'] for stock in nasdaq_data]
    stock_percentage_increase_list = multi_threading(function=fetch_stock_percentage_increase,
                                                     parameters=nasdaq_stock_symbols)
    stock_percentage_increase_list = [
        i for i in stock_percentage_increase_list if i]

    top_stock_with_increased_percentage = max(
        stock_percentage_increase_list, key=lambda x: x.percentage)
    logfire.info(
        f'Top performance stock: {top_stock_with_increased_percentage}')

    return top_stock_with_increased_percentage


def capture_df_info(df):
    """
    Captures the output of df.info() into a string.

    Parameters:
        df (pandas.DataFrame): The dataframe to capture info from.

    Returns:
        str: The captured info as a string.
    """
    buffer = StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()


def convert_to_markdown_table(dataframe):
    """
    Converts the top 5 rows of a DataFrame to a Markdown table.

    Args:
        dataframe (pd.DataFrame): The DataFrame to convert.

    Returns:
        str: The Markdown table as a string.
    """
    return tabulate(dataframe.head(), headers='keys', tablefmt='pipe', showindex=False)


def fetch_stock_data(symbol: str, number_of_days: int) -> pd.DataFrame:
    """
    Fetch stock data for a given symbol and number of days.

    Args:
        symbol (str): The stock symbol to fetch data for.
        number_of_days (int): The number of days of historical data to fetch.

    Returns:
        pd.DataFrame: A DataFrame containing the stock data.
    """
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=f"{number_of_days}d")
    df.reset_index(inplace=True)
    return df


if __name__ == "__main__":
    top_nasdaq_performance_stock = get_top_nasdaq_performance_stock()
    print(
        f"Top NASDAQ performance stock: {top_nasdaq_performance_stock.symbol} with percentage increase: {top_nasdaq_performance_stock.percentage}")
    # python -m src.tools

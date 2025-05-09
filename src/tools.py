from pydantic_ai import RunContext
from src.schema import Deps
from src.utils_stock import capture_df_info, convert_to_markdown_table, fetch_stock_data, get_top_nasdaq_performance_stock


async def get_top_nasdaq_performance_stock_data(
    ctx: RunContext[Deps]
) -> dict[str, float]:
    """Get the day's top NASDAQ gainer with symbol, percentage increase, sample data in markdown format, pandas dataframe info and csv data path for python code analysis.

    Args:
        ctx: The context.
    """
    top_nasdaq_performance_stock = get_top_nasdaq_performance_stock()
    symbol = top_nasdaq_performance_stock.symbol
    df = fetch_stock_data(
        symbol=symbol, number_of_days=ctx.deps.number_of_days)
    sample_data_in_markdown = convert_to_markdown_table(df)
    data_path = f"{symbol}_performance_in_the_past_{ctx.deps.number_of_days}.csv".lower()
    pandas_dataframe_info = capture_df_info(df)

    return {
        'symbol': top_nasdaq_performance_stock.symbol,
        'percentage': top_nasdaq_performance_stock.percentage,
        'sample_data_in_markdown': sample_data_in_markdown,
        'data_csv_path': data_path,
        "pandas_dataframe_info": pandas_dataframe_info,
    }

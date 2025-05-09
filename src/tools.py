import json
from pydantic_ai import RunContext
from schema import Deps, FlightDetails
from agents import extraction_agent
from src.tool_dependencies import fetch_stock_percentage_increase
from utils import logfire, multi_threading


async def extract_flights(ctx: RunContext[Deps]) -> list[FlightDetails]:
    """Get details of all flights."""
    # we pass the usage to the search agent so requests within this agent are counted
    result = await extraction_agent.run(ctx.deps.web_page_text, usage=ctx.usage)
    logfire.info('found {flight_count} flights',
                 flight_count=len(result.output))
    return result.output


def get_top_nasdaq_performance_stock(ctx: RunContext[Deps]) -> str:
    """Get the top performance stock."""

    with open('./data/nasdaq_data.json', 'r') as f:
        nasdaq_data = json.load(f)

    nasdaq_stock_symbols = [stock['Symbol'] for stock in nasdaq_data]
    stock_percentage_increase_list = multi_threading(function=fetch_stock_percentage_increase,
                                                     parameters=nasdaq_stock_symbols[:10])
    stock_percentage_increase_list = [
        i for i in stock_percentage_increase_list if i]

    return max(stock_percentage_increase_list, key=lambda x: x['percentage_increase'])

import asyncio
from anthropic import AsyncClient
from pydantic_ai import Agent
from src.models import deepseek
from src.schema import Deps
from devtools import debug
from src.tools import get_top_nasdaq_performance_stock_data

data_acquisition_agent = Agent(
    model=deepseek,
    system_prompt=(
        'You are a data acquisition agent. '
        'You task is to use the `get_top_nasdaq_performance_stock_data` tool to fetch top nasdaq performance stock_data for further analysis. '
        'You should use the tool to fetch the data and return it in a structured format. '
        'The data should include the stock symbol, percentage increase, sample data in markdown format, pandas dataframe info, and csv data path for python code analysis. '
    ),
    retries=3,
    instrument=True,
    tools=[get_top_nasdaq_performance_stock_data]
)


async def main():
    async with AsyncClient() as client:
        deps = Deps(
            client=client, number_of_days=5
        )
        result = await data_acquisition_agent.run(
            'Start', deps=deps
        )
        debug(result)
        print('Response:', result.output)

if __name__ == '__main__':
    asyncio.run(main())
    # python -m src.agents.data_acquisition_agent

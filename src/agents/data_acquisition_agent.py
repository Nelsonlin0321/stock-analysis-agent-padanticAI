from pydantic_ai import Agent
from src.models import deepseek

data_acquisition_agent = Agent(
    model=deepseek,
    system_prompt=(
        'Be concise, reply with one sentence. '
        'Use the `get_stock_data` tool to fetch stock data'
        'then identify the day\'s top NASDAQ gainer (symbol and percentage increase).'
    ),
    retries=3,
    instrument=True,
)

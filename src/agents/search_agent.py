from pydantic_ai import Agent
from schema import Deps, FlightDetails, NoFlightFound
from .search_agent_tools import extract_flights
from src.models import deepseek

search_agent = Agent[Deps, FlightDetails | NoFlightFound](
    model=deepseek,
    output_type=FlightDetails | NoFlightFound,  # type: ignore
    retries=4,
    system_prompt=(
        'Your job is to find the cheapest flight for the user on the given date. '
    ),
    instrument=True,
    tools=[extract_flights],
)

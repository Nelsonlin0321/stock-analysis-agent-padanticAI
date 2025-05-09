from pydantic_ai import Agent
from schema import Deps, FlightDetails, NoFlightFound
from src.models import deepseek
from src.tools import extract_flights

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

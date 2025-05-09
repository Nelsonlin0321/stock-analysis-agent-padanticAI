from pydantic_ai import RunContext
from schema import Deps, FlightDetails
from agents import extraction_agent
from utils import logfire


async def extract_flights(ctx: RunContext[Deps]) -> list[FlightDetails]:
    """Get details of all flights."""
    # we pass the usage to the search agent so requests within this agent are counted
    result = await extraction_agent.run(ctx.deps.web_page_text, usage=ctx.usage)
    logfire.info('found {flight_count} flights',
                 flight_count=len(result.output))
    return result.output

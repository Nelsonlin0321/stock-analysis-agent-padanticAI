from dataclasses import dataclass
from pydantic_ai import Agent
from src.schema import FlightDetails
from src.models import deepseek
from pydantic_ai.usage import Usage
from src.utils import logfire

extraction_agent = Agent(
    model=deepseek,
    output_type=list[FlightDetails],
    system_prompt='Extract all the flight details from the given text.',
)


if __name__ == '__main__':
    from pydantic_ai import RunContext

    @dataclass
    class Deps:
        web_page_text: str

    flights_web_page = """
    1. Flight SFO-AK123
    - Price: $350
    - Origin: San Francisco International Airport (SFO)
    - Destination: Ted Stevens Anchorage International Airport (ANC)
    - Date: January 10, 2025

    2. Flight SFO-AK456
    - Price: $370
    - Origin: San Francisco International Airport (SFO)
    - Destination: Fairbanks International Airport (FAI)
    - Date: January 10, 2025

    3. Flight SFO-AK789
    - Price: $400
    - Origin: San Francisco International Airport (SFO)
    - Destination: Juneau International Airport (JNU)
    - Date: January 20, 2025

    4. Flight NYC-LA101
    - Price: $250
    - Origin: San Francisco International Airport (SFO)
    - Destination: Ted Stevens Anchorage International Airport (ANC)
    - Date: January 10, 2025

    5. Flight CHI-MIA202
    - Price: $200
    - Origin: Chicago O'Hare International Airport (ORD)
    - Destination: Miami International Airport (MIA)
    - Date: January 12, 2025

    6. Flight BOS-SEA303
    - Price: $120
    - Origin: Boston Logan International Airport (BOS)
    - Destination: Ted Stevens Anchorage International Airport (ANC)
    - Date: January 12, 2025

    7. Flight DFW-DEN404
    - Price: $150
    - Origin: Dallas/Fort Worth International Airport (DFW)
    - Destination: Denver International Airport (DEN)
    - Date: January 10, 2025

    8. Flight ATL-HOU505
    - Price: $180
    - Origin: Hartsfield-Jackson Atlanta International Airport (ATL)
    - Destination: George Bush Intercontinental Airport (IAH)
    - Date: January 10, 2025
    """
    usage: Usage = Usage()
    ctx = RunContext(deps=Deps(web_page_text=flights_web_page),
                     model=deepseek, usage=usage, prompt="")
    result = extraction_agent.run_sync(ctx.deps.web_page_text, usage=ctx.usage)
    print(result.output)

    # python src/agents/extraction_agent.py

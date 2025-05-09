from pydantic_ai import Agent
from schema import Failed, FlightDetails, SeatPreference
from src.models import deepseek
from tools import extract_flights


seat_preference_agent = Agent[None, SeatPreference | Failed](
    model=deepseek,
    output_type=SeatPreference | Failed,  # type: ignore
    system_prompt=(
        "Extract the user's seat preference. "
        'Seats A and F are window seats. '
        'Row 1 is the front row and has extra leg room. '
        'Rows 14, and 20 also have extra leg room. '
    ),
    tools=[extract_flights],

)


extraction_agent = Agent(
    'openai:gpt-4o',
    output_type=list[FlightDetails],
    system_prompt='Extract all the flight details from the given text.',
)

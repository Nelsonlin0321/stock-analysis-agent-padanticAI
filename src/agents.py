from pydantic_ai import Agent
from schema import Failed, FlightDetails, SeatPreference


seat_preference_agent = Agent[None, SeatPreference | Failed](
    'openai:gpt-4o',
    output_type=SeatPreference | Failed,  # type: ignore
    system_prompt=(
        "Extract the user's seat preference. "
        'Seats A and F are window seats. '
        'Row 1 is the front row and has extra leg room. '
        'Rows 14, and 20 also have extra leg room. '
    ),
    tools=[]
)

extraction_agent = Agent(
    'openai:gpt-4o',
    output_type=list[FlightDetails],
    system_prompt='Extract all the flight details from the given text.',
)

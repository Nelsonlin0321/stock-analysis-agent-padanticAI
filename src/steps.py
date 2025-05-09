from rich.prompt import Prompt
from pydantic_ai.usage import Usage
from schema import FlightDetails, SeatPreference
from utils import usage_limits
from agents import seat_preference_agent
from pydantic_ai.messages import ModelMessage


async def find_seat(usage: Usage) -> SeatPreference:
    message_history: list[ModelMessage] | None = None
    while True:
        answer = Prompt.ask('What seat would you like?')

        result = await seat_preference_agent.run(
            answer,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )
        if isinstance(result.output, SeatPreference):
            return result.output
        else:
            print('Could not understand seat preference. Please try again.')
            message_history = result.all_messages()


async def buy_tickets(flight_details: FlightDetails, seat: SeatPreference):
    print(f'Purchasing flight {flight_details=!r} {seat=!r}...')

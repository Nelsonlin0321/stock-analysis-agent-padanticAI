from dataclasses import Field, dataclass
import datetime
from typing import Literal
from pydantic import BaseModel


class SeatPreference(BaseModel):
    row: int = Field(ge=1, le=30)
    seat: Literal['A', 'B', 'C', 'D', 'E', 'F']


class Failed(BaseModel):
    """Unable to extract a seat selection."""


class NoFlightFound(BaseModel):
    """When no valid flight is found."""


class FlightDetails(BaseModel):
    """Details of the most suitable flight."""

    flight_number: str
    price: int
    origin: str = Field(description='Three-letter airport code')
    destination: str = Field(description='Three-letter airport code')
    date: datetime.date


@dataclass
class Deps:
    web_page_text: str
    req_origin: str
    req_destination: str
    req_date: datetime.date

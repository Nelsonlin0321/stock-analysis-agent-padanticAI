from dataclasses import dataclass
from anthropic import AsyncClient
from pydantic import BaseModel


class SymbolWithIncreasePercentage(BaseModel):
    """Top performance stock with increased percentage."""
    symbol: str
    percentage: float


@dataclass
class Deps:
    client: AsyncClient
    number_of_days: int = 5

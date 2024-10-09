from dataclasses import dataclass

@dataclass
class RateResult:
    """Result of a rate."""
    name: str
    code: str
    unit: int
    rate: float

@dataclass
class RatesResult:
    """Result of a list of rates."""
    rates: list[RateResult]
    date: str
    provider: str


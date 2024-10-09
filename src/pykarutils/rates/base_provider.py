from abc import ABC, abstractmethod
from .structure.result import RateResult, RatesResult

class RateProvider(ABC):
    """Base class for rate providers."""

    @abstractmethod
    def get_rate(self,date: str, code: str) -> RateResult:
        """Get the rate for a given code."""
        pass

    @abstractmethod
    def get_rates(self, date: str) -> RatesResult:
        """Get all rates."""
        pass
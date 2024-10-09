from abc import ABC, abstractmethod
from typing import Optional, List

from .structure.result import RateResult, RatesResult


class RateProvider(ABC):
    """Base class for rate providers."""

    @abstractmethod
    def get_rate(self, date: str, code: str) -> RateResult:
        """
        Get the exchange rate for a given currency code on a specific date.

        Args:
            date (str): The date for which to retrieve the exchange rate in the format 'dd.mm.yyyy'.
            code (str): The currency code for which to retrieve the exchange rate.

        Returns:
            RateResult: A RateResult object containing the exchange rate information.
        """
        pass

    @abstractmethod
    def get_rates(self, date: str, currencies: Optional[List[str]] = None) -> RatesResult:
        """
        Get all exchange rates for a specific date and optionally filter by currency codes.

        Args:
            date (str): The date for which to retrieve the exchange rates in the format 'dd.mm.yyyy'.
            currencies (Optional[List[str]]): A list of currency codes to filter the rates. If not provided,
                                              all rates are returned.

        Returns:
            RatesResult: An object containing the exchange rates for the specified date and currencies.
        """
        pass

    def convert(self, date: str, amount: float, from_code: str, to_code: str) -> float:
        """
        Convert an amount from one currency to another.

        Args:
            date (str): The date for which to retrieve the exchange rates in the format 'dd.mm.yyyy'.
            amount (float): The amount of money to convert.
            from_code (str): The currency code of the currency to convert from.
            to_code (str): The currency code of the currency to convert to.

        Returns:
            float: The converted amount in the target currency.
        """
        pass
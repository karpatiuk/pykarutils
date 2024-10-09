from dataclasses import dataclass
from typing import Union,List,Dict


from dataclasses import dataclass
from typing import Union, List, Dict

@dataclass
class RateResult:
    """
    Represents the result of a single exchange rate.

    Attributes:
        name (str): The name of the currency.
        code (str): The currency code (e.g., 'USD', 'EUR').
        unit (int): The unit of the currency.
        rate (float): The exchange rate.
        base_currency (str): The base currency for the exchange rate (e.g., 'MDL').
        rate_text (str): A textual representation of the exchange rate.
    """
    name: str
    code: str
    unit: int
    rate: float
    base_currency: str
    rate_text: str

@dataclass
class RatesResult:
    """
    Represents the result of a list of exchange rates.

    Attributes:
        rates (Union[List[RateResult], Dict[str, RateResult]]): A list or dictionary of RateResult objects.
        date (str): The date for which the rates are applicable.
        provider (str): The provider of the exchange rates.
    """
    rates: Union[List[RateResult], Dict[str, RateResult]]
    date: str
    provider: str

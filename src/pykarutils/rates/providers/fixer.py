import requests
from datetime import datetime
from typing import List, Optional
from ..base_provider import BaseRateProvider
from ..structure.result import RateResult, RatesResult


class FixerProvider(BaseRateProvider):
    """Fixer rate provider."""

    PROVIDER_NAME = 'FIXER'
    LATEST_RATES_URL = "https://data.fixer.io/api/latest"
    HISTORICAL_RATES_URL = "https://data.fixer.io/api/"

    def __init__(self, api_key: str):
        """
        Initialize the FixerProvider.

        Args:
            api_key (str): The API key for the Fixer API.
        """
        self._api_key = api_key
        self._url = f"{self.LATEST_RATES_URL}"

        super().__init__()

    def get_rates(self, date: str = None, currencies: Optional[List[str]] = None) -> RatesResult:
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        else:
            self._url = f"{self.HISTORICAL_RATES_URL}{date}"

        if date in self._rates_cache:
            rates_dict = self._rates_cache[date]
        else:
            rates_data = self._get_api_rates(self._url,self._api_key)
            rates_dict = {}

            for currency, rate in rates_data.items():
                rates_dict[currency] = RateResult(
                    name=currency,
                    code=currency,
                    unit=1,
                    rate=rate,
                    base_currency='EUR',
                    rate_text=f"1 EUR = {rate} {currency}"
                )

            self._rates_cache[date] = rates_dict

        if currencies is not None:
            filtered_rates = {code: rate for code, rate in rates_dict.items() if code in currencies}
        else:
            filtered_rates = rates_dict

        # print(rates_data)
        return RatesResult(
            date=date,
            rates=filtered_rates,
            provider=self.PROVIDER_NAME
        )

    @staticmethod
    def _get_api_rates(url: str, api_key: str) -> list:
        """Get the rates from the API."""
        try:
            # Fetch the JSON data from the URL
            querystring = {
                # "base": "USD"
                "access_key": api_key
            }
            response = requests.get(url, params=querystring)
            response.raise_for_status()

            rates_response = response.json()

        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP Error: {http_err}")
        except requests.exceptions.ReadTimeout as timeout_err:
            raise Exception(f"Time out: {timeout_err}")
        except requests.exceptions.ConnectionError as conn_err:
            raise Exception(f"Connection error: {conn_err}")
        except requests.exceptions.RequestException as req_err:
            raise Exception(f"Exception request: {req_err}")
        except Exception as e:
            raise Exception(f"An error occurred while fetching rates data: {e}")

        return rates_response.get('rates')

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

        Raises:
            Exception: If the currency code is invalid or no rate is found for the currency code.
        """
        rates_result = self.get_rates(date, currencies=[from_code, to_code])
        rates = rates_result.rates
        from_rate = rates.get(from_code)
        to_rate = rates.get(to_code)

        if from_rate is None or to_rate is None:
            raise Exception('Invalid currency code or no rate found for the currency code')

        converted_amount = (to_rate.rate * amount) / from_rate.rate
        return converted_amount
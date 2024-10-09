import csv
import requests
from datetime import datetime
from io import StringIO
from typing import List, Optional
from ..base_provider import RateProvider
from ..structure.result import RateResult, RatesResult

RATES_URL = 'https://bnm.md/en/export-official-exchange-rates?date='


class BnmProvider(RateProvider):
    """BNM rate provider."""

    def __init__(self):
        self._rates_cache = {}

    def get_rate(self, date: str, code: str) -> RateResult | None:
        """
        Get the exchange rate for a given currency code on a specific date.

        Args:
            date (str): The date for which to retrieve the exchange rate in the format 'dd.mm.yyyy'.
            code (str): The currency code for which to retrieve the exchange rate.

        Returns:
            RateResult | None: A RateResult object containing the exchange rate information if found,
                               otherwise None.
        """
        rates_result = self.get_rates(date, currencies=[code])
        return rates_result.rates.get(code)

    def get_rates(self, date: str = None, currencies: Optional[List[str]] = None) -> RatesResult:
        """
        Get all exchange rates for a specific date and optionally filter by currency codes.

        Args:
            date (str, optional): The date for which to retrieve the exchange rates in the format 'dd.mm.yyyy'.
                                  If not provided, the current date is used.
            currencies (Optional[List[str]], optional): A list of currency codes to filter the rates. If not provided,
                                                        all rates are returned.

        Returns:
            RatesResult: An object containing the exchange rates for the specified date and currencies.
        """
        if date is None:
            date = datetime.now().strftime('%d.%m.%Y')

        if date in self._rates_cache:
            rates_dict = self._rates_cache[date]
        else:
            rates_data = self._get_api_rates(RATES_URL + date)
            rates_dict = {}
            for rate in rates_data:
                rates_dict[rate['Abbr']] = RateResult(
                    name=rate['Currency'],
                    code=rate['Abbr'],
                    unit=int(rate['Rate']),
                    rate=float(rate['Rates'].replace(',', '.')),
                    base_currency='MDL',
                    rate_text=f"{rate['Rate']} {rate['Abbr']} = {rate['Rates'].replace(',', '.')} MDL"
                )
            self._rates_cache[date] = rates_dict

        if currencies is not None:
            filtered_rates = {code: rate for code, rate in rates_dict.items() if code in currencies}
        else:
            filtered_rates = rates_dict

        return RatesResult(
            date=date,
            rates=filtered_rates,
            provider='BNM'
        )

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

        converted_amount = (from_rate.rate * to_rate.unit) / (from_rate.unit * to_rate.rate) * amount
        return converted_amount

    @staticmethod
    def _get_api_rates(url: str) -> list:
        """Get the rates from the API."""
        try:
            # Fetch the CSV data from the URL
            response = requests.get(url)
            response.raise_for_status()

            # Check if the request was successful
            if response.status_code == 200:
                response.raise_for_status()
                content = response.content.decode('utf-8')

                # Split the content into individual lines
                lines = content.splitlines()

                # Exclude the first 2 rows and the last 4 rows
                relevant_lines = lines[2:-4]

                # Use StringIO to convert the list of lines back into a file-like object
                csv_data = StringIO('\n'.join(relevant_lines))

                # Parse the CSV data
                reader = csv.DictReader(csv_data, delimiter=';')
                rates = list(reader)
                return rates
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

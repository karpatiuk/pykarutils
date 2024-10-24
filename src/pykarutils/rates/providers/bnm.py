import csv
import requests
from datetime import datetime
from io import StringIO
from typing import List, Optional
from ..base_provider import BaseRateProvider
from ..structure.result import RateResult, RatesResult


class BnmProvider(BaseRateProvider):
    """BNM rate provider."""

    PROVIDER_NAME = 'BNM'
    RATES_URL = 'https://bnm.md/en/export-official-exchange-rates?date='

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
            rates_data = self._get_api_rates(self.RATES_URL + date)
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
            date = date,
            rates = filtered_rates,
            provider = self.PROVIDER_NAME
        )

    @staticmethod
    def _get_api_rates(url: str) -> list:
        """Get the rates from the API."""
        try:
            # Fetch the CSV data from the URL
            response = requests.get(url)
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

        return rates

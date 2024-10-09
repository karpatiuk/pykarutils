import csv
import requests
from io import StringIO
from ..base_provider import RateProvider
from ..structure.result import RateResult, RatesResult

RATES_URL = 'https://bnm.md/en/export-official-exchange-rates?date='


class BnmProvider(RateProvider):
    """BNM rate provider."""

    def get_rate(self, date: str, code: str) -> RateResult | None:
        """Get the rate for a given code."""
        rates = self._get_api_rates(RATES_URL + date)

        for rate in rates:
            if rate['Abbr'] == code:
                return RateResult(
                    name=rate['Currency'],
                    code=rate['Abbr'],
                    unit=int(rate['Rate']),
                    rate=float(rate['Rates'].replace(',', '.'))
                )
        return None

    def get_rates(self, date: str) -> RatesResult:
        """Get all rates."""
        rates = self._get_api_rates(RATES_URL + date)
        return RatesResult(
            rates=[
                RateResult(
                    name=rate['Currency'],
                    code=rate['Abbr'],
                    unit=int(rate['Rate']),
                    rate=float(rate['Rates'].replace(',', '.'))
                )
                for rate in rates
            ],
            date=date,
            provider = 'BNM'
        )


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

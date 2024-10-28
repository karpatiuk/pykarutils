import unittest
from unittest.mock import patch, Mock
from src.pykarutils.rates.providers.fixer import FixerProvider
from src.pykarutils.rates.structure.result import RatesResult, RateResult

class MyTestCase(unittest.TestCase):
    TEST_DATA ={
      "success": True,
      "timestamp": 1729876562,
      "base": "EUR",
      "date": "2024-10-25",
      "rates": {
        "AED": 3.968009,
        "AFN": 71.899701,
        "ALL": 98.378943,
        "AMD": 418.354911,
        "ANG": 1.947019,
        "AOA": 982.067745,
        "ARS": 1063.852017,
        "AUD": 1.63487,
        "AWG": 1.94458,
        "AZN": 1.841327,
        "BAM": 1.951973,
        "BBD": 2.181244,
        "BDT": 129.098089,
        "BGN": 1.952995,
        "BHD": 0.407203,
        "BIF": 3137.406984,
        "BMD": 1.080322,
        "BND": 1.426729,
        "BOB": 7.465502,
        "BRL": 6.155995,
        "BSD": 1.080292,
        "BTC": 0.000015990091,
        "BTN": 90.827907,
        "BWP": 14.442951,
        "BYN": 3.535434,
        "BYR": 21174.310334,
        "BZD": 2.177571,
        "CAD": 1.50013,
        "CDF": 3078.918248,
        "CHF": 0.935987,
        "CLF": 0.037122,
        "CLP": 1024.296641,
        "CNY": 7.692546,
        "CNH": 7.691131,
        "COP": 4676.594911,
        "CRC": 556.419403,
        "CUC": 1.080322,
        "CUP": 28.628532,
        "CVE": 110.050258,
        "CZK": 25.270405,
        "DJF": 191.994665,
        "DKK": 7.461026,
        "DOP": 65.05246,
        "DZD": 144.279163,
        "EGP": 52.697674,
        "ERN": 16.204829,
        "ETB": 131.370072,
        "EUR": 1,
        "FJD": 2.427214,
        "FKP": 0.826629,
        "GBP": 0.832772,
        "GEL": 2.938439,
        "GGP": 0.826629,
        "GHS": 17.361283,
        "GIP": 0.826629,
        "GMD": 75.08081,
        "GNF": 9316.819986,
        "GTQ": 8.356693,
        "GYD": 226.021055,
        "HKD": 8.394696,
        "HNL": 27.234605,
        "HRK": 7.442371,
        "HTG": 142.22248,
        "HUF": 404.058801,
        "IDR": 16964.295672,
        "ILS": 4.092351,
        "IMP": 0.826629,
        "INR": 90.892942,
        "IQD": 1415.225355,
        "IRR": 45486.955522,
        "ISK": 149.10602,
        "JEP": 0.826629,
        "JMD": 171.13606,
        "JOD": 0.765839,
        "JPY": 164.468174,
        "KES": 139.358069,
        "KGS": 92.681756,
        "KHR": 4387.479276,
        "KMF": 491.492387,
        "KPW": 972.289517,
        "KRW": 1504.790974,
        "KWD": 0.330968,
        "KYD": 0.900252,
        "KZT": 525.499451,
        "LAK": 23730.913271,
        "LBP": 96743.319193,
        "LKR": 317.238033,
        "LRD": 207.427165,
        "LSL": 19.070511,
        "LTL": 3.18991,
        "LVL": 0.653476,
        "LYD": 5.203846,
        "MAD": 10.667385,
        "MDL": 19.392339,
        "MGA": 4978.331808,
        "MKD": 61.512051,
        "MMK": 3508.843572,
        "MNT": 3670.934036,
        "MOP": 8.646009,
        "MRU": 42.995704,
        "MUR": 49.81348,
        "MVR": 16.593391,
        "MWK": 1873.262023,
        "MXN": 21.57932,
        "MYR": 4.688411,
        "MZN": 69.043403,
        "NAD": 19.070511,
        "NGN": 1775.24981,
        "NIO": 39.752431,
        "NOK": 11.842943,
        "NPR": 145.324771,
        "NZD": 1.80639,
        "OMR": 0.415901,
        "PAB": 1.080302,
        "PEN": 4.056584,
        "PGK": 4.323563,
        "PHP": 63.189163,
        "PKR": 299.893239,
        "PLN": 4.347527,
        "PYG": 8646.048837,
        "QAR": 3.940012,
        "RON": 4.973371,
        "RSD": 117.044219,
        "RUB": 104.790235,
        "RWF": 1461.062537,
        "SAR": 4.05766,
        "SBD": 9.021832,
        "SCR": 14.283588,
        "SDG": 649.817265,
        "SEK": 11.463226,
        "SGD": 1.428132,
        "SHP": 0.826629,
        "SLE": 24.577273,
        "SLL": 22653.807797,
        "SOS": 617.400974,
        "SRD": 36.785498,
        "STD": 22360.483323,
        "SVC": 9.452555,
        "SYP": 2714.341613,
        "SZL": 19.063977,
        "THB": 36.402511,
        "TJS": 11.497371,
        "TMT": 3.781127,
        "TND": 3.351329,
        "TOP": 2.530227,
        "TRY": 37.04186,
        "TTD": 7.339746,
        "TWD": 34.659432,
        "TZS": 2943.880576,
        "UAH": 44.673528,
        "UGX": 3962.268382,
        "USD": 1.080322,
        "UYU": 44.962265,
        "UZS": 13844.856224,
        "VEF": 3913523.038957,
        "VES": 44.107181,
        "VND": 27407.768018,
        "VUV": 128.258025,
        "WST": 3.026181,
        "XAF": 654.685565,
        "XAG": 0.032027,
        "XAU": 0.000397,
        "XCD": 2.919624,
        "XDR": 0.81352,
        "XOF": 654.673468,
        "XPF": 119.331742,
        "YER": 270.458598,
        "ZAR": 19.09589,
        "ZMK": 9724.196821,
        "ZMW": 28.601454,
        "ZWL": 347.863229
      }
    }

    @patch('src.pykarutils.rates.providers.fixer.requests.get')
    def test_get_rates_valid_date(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.TEST_DATA
        mock_get.return_value = mock_response

        provider = FixerProvider(api_key="dummy_key")
        result = provider.get_rates('2024-10-25')

        self.assertIsInstance(result, RatesResult)
        self.assertEqual(result.date, '2024-10-25')
        self.assertIn('USD', result.rates)
        self.assertIn('GBP', result.rates)
        self.assertEqual(result.rates['USD'].rate, 1.080322)
        self.assertEqual(result.rates['GBP'].rate, 0.832772)

    @patch('src.pykarutils.rates.providers.fixer.requests.get')
    def test_get_rates_invalid_date(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        provider = FixerProvider(api_key="dummy_key")
        with self.assertRaises(Exception):
            provider.get_rates('invalid-date')

    @patch('src.pykarutils.rates.providers.fixer.requests.get')
    def test_get_rates_no_date_provided(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.TEST_DATA
        mock_get.return_value = mock_response

        provider = FixerProvider(api_key="dummy_key")
        result = provider.get_rates()

        self.assertIsInstance(result, RatesResult)
        self.assertIn('USD', result.rates)
        self.assertIn('GBP', result.rates)

    @patch('src.pykarutils.rates.providers.fixer.requests.get')
    def test_get_rates_specific_currencies(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = self.TEST_DATA
        mock_get.return_value = mock_response

        provider = FixerProvider(api_key="dummy_key")
        result = provider.get_rates('2024-10-25', currencies=['USD', 'GBP'])

        self.assertIsInstance(result, RatesResult)
        self.assertEqual(result.date, '2024-10-25')
        self.assertIn('USD', result.rates)
        self.assertIn('GBP', result.rates)
        self.assertNotIn('JPY', result.rates)

    @patch('src.pykarutils.rates.providers.fixer.requests.get')
    def test_get_rates_cache_hit(self, mock_get):
        provider = FixerProvider(api_key="dummy_key")
        provider._rates_cache = {'2024-10-25': {
            'USD': RateResult(rate=1.080322, unit=1, code='USD', name='US Dollar', base_currency='EUR',
                              rate_text='1 EUR = 1.080322 USD')}}
        result = provider.get_rates('2024-10-25')

        self.assertIsInstance(result, RatesResult)
        self.assertEqual(result.date, '2024-10-25')
        self.assertIn('USD', result.rates)
        self.assertEqual(result.rates['USD'].rate, 1.080322)

    @patch('src.pykarutils.rates.providers.fixer.requests.get')
    def test_convert_valid_conversion(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "timestamp": 1629876562,
            "base": "EUR",
            "date": "2024-10-25",
            "rates": {
                "USD": 1.080322,
                "GBP": 0.832772,
                "EUR": 1
            }
        }
        mock_get.return_value = mock_response

        provider = FixerProvider(api_key="dummy_key")
        result = provider.convert('2024-10-25', 100, 'EUR', 'USD')

        self.assertEqual(result, 108.0322)

    @patch('src.pykarutils.rates.providers.fixer.requests.get')
    def test_convert_invalid_currency(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "timestamp": 1629876562,
            "base": "EUR",
            "date": "2024-10-25",
            "rates": {
                "USD": 1.2
            }
        }
        mock_get.return_value = mock_response

        provider = FixerProvider(api_key="dummy_key")
        with self.assertRaises(Exception):
            provider.convert('2024-10-25', 100, 'EUR', 'INVALID')

if __name__ == '__main__':
    unittest.main()
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

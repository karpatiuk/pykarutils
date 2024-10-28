import unittest
from unittest.mock import patch, Mock
from src.pykarutils.rates.providers.bnm import BnmProvider
from src.pykarutils.rates.structure.result import RatesResult, RateResult

class TestBnmProvider(unittest.TestCase):
    TEST_DATA = (
        "\"Official exchange rate:\";02.10.2024;;;\n"
        ";;;;\n"
        "Currency;Code;Abbr;Rate;Rates\n"
        "\"Albanian lek\";008;ALL;10;1,9547\n"
        "\"Armenian Dram\";051;AMD;10;0,4499\n"
        "\"Australian Dollar\";036;AUD;1;12,0254\n"
        "\"Azerbaijanian Manat\";944;AZN;1;10,2495\n"
        "\"Belarussian Ruble\";933;BYN;1;5,4157\n"
        "\"Bulgarian Lev\";975;BGN;1;9,8783\n"
        "\"Canadian Dollar\";124;CAD;1;12,8821\n"
        "\"Chinese yuan renminbi\";156;CNY;1;2,4831\n"
        "\"Czech Koruna\";203;CZK;1;0,7644\n"
        "\"Danish Krone\";208;DKK;1;2,5906\n"
        "Euro;978;EUR;1;19,3192\n"
        "\"Georgian Lar\";981;GEL;1;6,3898\n"
        "\"Hong Kong dollar\";344;HKD;1;2,2418\n"
        "\"Hungarian Forint\";348;HUF;100;4,8596\n"
        "\"Iceland Krona\";352;ISK;10;1,2871\n"
        "\"Indian rupee\";356;INR;10;2,0792\n"
        "\"Japanese Yen\";392;JPY;100;12,1235\n"
        "\"Kazakhstan Tenge\";398;KZT;10;0,3624\n"
        "\"Kuwaiti Dinar\";414;KWD;1;57,0593\n"
        "\"Kyrgyzstan Som\";417;KGS;10;2,0730\n"
        "\"Macedonian denar\";807;MKD;10;3,1419\n"
        "\"Malaysian Ringgit\";458;MYR;1;4,1925\n"
        "\"New Zealand Dollar\";554;NZD;1;10,9972\n"
        "\"Norwegian Krone\";578;NOK;1;1,6440\n"
        "\"Polish Zloty\";985;PLN;1;4,5042\n"
        "\"Pound Sterling\";826;GBP;1;23,2206\n"
        "\"Romanian Leu\";946;RON;1;3,8827\n"
        "\"Russian Ruble\";643;RUB;1;0,1864\n"
        "\"Serbian Dinar\";941;RSD;100;16,5058\n"
        "\"Shekel Israelit\";376;ILS;1;4,6911\n"
        "\"South Korean won\";410;KRW;100;1,3198\n"
        "\"Special Drawing Rights\";960;XDR;1;23,5394\n"
        "\"Swedish Krona\";752;SEK;1;1,7068\n"
        "\"Swiss Franc\";756;CHF;1;20,5800\n"
        "\"Tajikistan Somoni\";972;TJS;1;1,6389\n"
        "\"Turkish Lira\";949;TRY;1;0,5096\n"
        "\"Turkmenistan Manat\";934;TMT;1;4,9795\n"
        "\"U.A.E. Dirham\";784;AED;1;4,7449\n"
        "\"US Dollar\";840;USD;1;17,4282\n"
        "\"Ukraine Hryvnia\";980;UAH;1;0,4219\n"
        "\"Uzbekistan Sum\";860;UZS;100;0,1369\n"
        "\n"
        "\"Data source:\";BNM\n"
        "Date:;02.10.2024\n"
        "Hour:;07:28\n"
    )

    @patch('src.pykarutils.rates.providers.bnm.requests.get')
    def test_get_rates_valid_date(self, mock_get):
        mock_response = Mock()
        mock_response.content.decode.return_value = self.TEST_DATA
        mock_get.return_value = mock_response

        provider = BnmProvider()
        result = provider.get_rates('02.10.2024')

        self.assertIsInstance(result, RatesResult)
        self.assertEqual(result.date, '02.10.2024')
        self.assertIn('USD', result.rates)
        self.assertIn('EUR', result.rates)
        self.assertEqual(result.rates['USD'].rate, 17.4282)
        self.assertEqual(result.rates['EUR'].rate, 19.3192)

    @patch('src.pykarutils.rates.providers.bnm.requests.get')
    def test_get_rates_invalid_date(self, mock_get):
        mock_response = Mock()
        mock_response.content.decode.return_value = ""
        mock_get.return_value = mock_response

        provider = BnmProvider()
        with self.assertRaises(Exception):
            provider.get_rates('invalid-date')

    @patch('src.pykarutils.rates.providers.bnm.requests.get')
    def test_get_rates_no_date_provided(self, mock_get):
        mock_response = Mock()
        mock_response.content.decode.return_value = self.TEST_DATA
        mock_get.return_value = mock_response

        provider = BnmProvider()
        result = provider.get_rates()

        self.assertIsInstance(result, RatesResult)
        self.assertIn('USD', result.rates)
        self.assertIn('EUR', result.rates)

    @patch('src.pykarutils.rates.providers.bnm.requests.get')
    def test_get_rates_specific_currencies(self, mock_get):
        mock_response = Mock()
        mock_response.content.decode.return_value = self.TEST_DATA
        mock_get.return_value = mock_response

        provider = BnmProvider()
        result = provider.get_rates('02.10.2024', currencies=['USD', 'EUR'])

        self.assertIsInstance(result, RatesResult)
        self.assertEqual(result.date, '02.10.2024')
        self.assertIn('USD', result.rates)
        self.assertIn('EUR', result.rates)
        self.assertNotIn('GBP', result.rates)

    @patch('src.pykarutils.rates.providers.bnm.requests.get')
    def test_get_rates_cache_hit(self, mock_get):
        provider = BnmProvider()
        provider._rates_cache = {'02.10.2024': {'USD': RateResult(rate=17.4282, unit=1, code='USD', name='US Dollar', base_currency='MDL', rate_text='1 USD = 17.4282 MDL')}}
        result = provider.get_rates('02.10.2024')

        self.assertIsInstance(result, RatesResult)
        self.assertEqual(result.date, '02.10.2024')
        self.assertIn('USD', result.rates)
        self.assertEqual(result.rates['USD'].rate, 17.4282)


    @patch('src.pykarutils.rates.providers.bnm.requests.get')
    def test_convert_valid_currencies(self, mock_get):
        mock_response = Mock()
        mock_response.content.decode.return_value = self.TEST_DATA
        mock_get.return_value = mock_response

        provider = BnmProvider()
        result = provider.convert('02.10.2024', 100, 'USD', 'EUR')

        self.assertEqual(result, 100 * 17.4282 / 19.3192 )

    @patch('src.pykarutils.rates.providers.bnm.requests.get')
    def test_convert_invalid_currencies(self, mock_get):
        mock_response = Mock()
        mock_response.content.decode.return_value = self.TEST_DATA
        mock_get.return_value = mock_response

        provider = BnmProvider()
        with self.assertRaises(Exception):
            provider.convert('02.10.2024', 100, 'USD', 'INVALID')

if __name__ == '__main__':
    unittest.main()
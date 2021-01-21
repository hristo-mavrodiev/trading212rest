import unittest
import os
from trading212rest.api import Trading212
from trading212rest.logger import logging, logger
logger = logging.getLogger(__name__)


USERNAME = os.getenv("TRADING212_USERNAME")
PASSWORD = os.getenv("TRADING212_PASSWORD")

api = Trading212(USERNAME, PASSWORD, DEMO_MODE = True)

class TestMethods(unittest.TestCase):
    def test_000_zero(self):
        """
        000. Zero test
        """
        logger.debug("Sample test to test the testings :)")
        self.assertEqual(":)", ":)")

    
    def test_001_start(self):
        """
        001.Start Chrome + chromedriver
        """
        self.assertTrue(api.start() is None)

    def test_002_login(self):
        """
        002.Check login
        """
        api.login()
        api.set_session()
        self.assertTrue(USERNAME is not None)
        self.assertTrue(PASSWORD is not None)
        self.assertTrue(api.cookies is not None)
        self.assertTrue(api.headers is not None)

    def test_003_check_funds(self):
        """
        003.Check funds of the Demo Investing account
        """
        
        result = api.get_funds()
        logger.debug(f'funds json  - {result}')

        self.assertTrue(result is not None)

    def test_004_order_history(self):
        """
        004.Check orders of the Demo Investing account
        """
        result = api.get_order_history()
        logger.debug(f'orders json  - {result}')
        self.assertTrue(result is not None)

    def test_005_order_history_date(self):
        """
        005.Check orders by timeframe  of the Demo Investing account
        """
        result = api.get_order_history("2020-01-01","2020-12-31")
        logger.debug(f'orders json  - {result}')
        self.assertTrue(result is not None)

    def test_006_dividends_history(self):
        """
        006.Check dividends of the Demo Investing account
        """
        result = api.get_dividend_history("2020-01-01","2020-12-31")
        logger.debug(f'dividends json  - {result}')
        self.assertTrue(result is not None)

    def test_007_market_buy(self):
        """
        007.Test Market Buy order 1 TSLA
        """
        result = api.submit_buy_order("TSLA_US_EQ", 1, 'market')
        logger.debug(f'buying 1 TSLA  - {result}')
        self.assertTrue(result is not None)

    def test_008_market_sell(self):
        """
        008.Test Market Sell order 1 TSLA
        """
        result = api.submit_sell_order("TSLA_US_EQ", 1, 'market')
        logger.debug(f'selling 1 TSLA  - {result}')
        self.assertTrue(result is not None)

    def test_009_limit_buy(self):
        """
        009.Test Limit Buy order 1 TSLA
        """
        result = api.submit_buy_order("TSLA_US_EQ", 1, 'limit', 700)
        logger.debug(f'limit buying 1 TSLA  - {result}')
        self.assertTrue(result is not None)

    def test_010_limit_buy(self):
        """
        010.Test Limit Buy order 4GLD
        """
        result = api.submit_buy_order("4GLDd_EQ", 1, 'limit', 40)
        logger.debug(f'limit buying 1 4GLD  - {result}')
        self.assertTrue(result is not None)

    def test_011_limit_sell(self):
        """
        011.Test Limit sell order 4GLD
        """
        result = api.submit_sell_order("4GLDd_EQ", 1, 'limit', 60)
        logger.debug(f'limit selling 1 4GLD  - {result}')
        self.assertTrue(result is not None)

    def test_012_stop_limit_sell(self):
        """
        012.Test Limit sell order 4GLD - take profit 60, stoploss 40
        """
        result = api.submit_sell_order("4GLDd_EQ", 1, 'STOP_LIMIT', 60, 40)
        logger.debug(f'limit selling 1 4GLD limit 60, stoploss 40 - {result}')
        self.assertTrue(result is not None)
    
    def test_099_shutdown(self):
        """099.Check shutdown"""
        self.assertTrue(api.shutdown() is None)
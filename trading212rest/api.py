import requests
from time import sleep
import json

from trading212rest.logger import logger, logging
from trading212rest.funcs import get_request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as firefox_options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class Trading212():
    def __init__(self, USERNAME, PASSWORD, DEMO_MODE = True, browser="Chrome"):
        self.__driver = None
        self.__USERNAME = USERNAME
        self.__PASSWORD = PASSWORD
        self.__DEMO_MODE = DEMO_MODE
        self.browser = browser
        self.cookies = None
        self.headers = None

        if (DEMO_MODE): 
            self.base_url = "https://demo.trading212.com"
        else:
            self.base_url = "https://live.trading212.com"

    def start(self):
        """
        Choose a browser and start the webdriver
        """
        if self.browser == 'Chrome':
            browser_options = chrome_options()
            browser_options.add_argument("--headless")
            browser_options.add_argument('--no-sandbox')
            self.__driver = webdriver.Chrome(options=browser_options)
        elif self.browser == 'Firefox':
            browser_options = firefox_options()
            browser_options.add_argument("--headless")
            browser_options.add_argument('--no-sandbox')
            self.__driver = webdriver.Firefox(options=browser_options)
        else:
            raise Exception('Please set browser to browser=Firefox or Chrome.')
        logger.info(f'Using {self.browser}')
        sleep(1)
        logger.debug('Webdriver Started')

    def login(self):
        """
        Login on trading212
        """
        logger.debug('Webdriver logging in......')
        try:
            self.__driver.get("https://www.trading212.com/en/login")

            email_el = self.__driver.find_element(By.ID, "username-real")
            pass_el = self.__driver.find_element(By.ID, "pass-real")

            email_el.send_keys(self.__USERNAME)
            pass_el.send_keys(self.__PASSWORD)

            WebDriverWait(self.__driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "button-login")))
            login_el = self.__driver.find_element(By.CLASS_NAME, "button-login")
            login_el.click()
            # logger.debug(f'Webdriver logging in......{self.__USERNAME}')
            WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "account-menu-button")))

            # resume = self.__driver.find_element(By.CLASS_NAME, "btn btn-primary")
            # if (resume):
            #     resume.click()

        except Exception as exe:
            logger.warning("Error while waiting for login to finish")

    def get_trading_cookie(self):
        """
        Switch to Investing acount and catch the cookie
        """

        cookie = None
        try:
            logger.debug('Webdriver capturing the cookie......')
            self.__driver.get(self.base_url)

            acc_panel = WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "account-menu-button")))
            acc_panel.click()

            invest_mode = WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.ID, "equitySwitchButton")))
            invest_mode.click()

            cookie = self.__driver.get_cookies()
            # data = ""
            # cookies = (self.__driver.get_cookies())
            # for cookie in cookies:
            #     new_key = str(cookie['name']) + "=" + str(cookie['value']) +"; "
            #     data += new_key
            #     self.__cookie = data
            logger.debug("success capturing the cookie")
        except Exception as exe:
            logger.warning(f'Unable to get the cookie.{exe}')
        return cookie

    def set_session(self):
        """
        Transfer the cookie from selenium to requests session object
        https://stackoverflow.com/questions/32639014/is-it-possible-to-transfer-a-session-between-selenium-webdriver-and-requests-s
        """
        logger.debug('Webdriver preparing requests headers and cookies......')
        s = requests.Session()
        headers = {'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'application/json'}
        s.headers.update(headers)

        s.cookies.update( {c['name'] : c['value'] for c in self.get_trading_cookie()} )
        self.cookies = s.cookies
        self.headers = s.headers
        return s.headers


    def shutdown(self):
        try:
            self.__driver.close()
            logger.info('Session has finished.Quit.')
        except Exception as exe:
            logger.warning(f'Unable to stop the driver.{exe}')

    def get_funds(self):
        """
        
        URL: https://demo.trading212.com/rest/customer/accounts/funds
        
        Response:
        {
            "11111111": {
                "accountId": 11111111,
                "tradingType": "EQUITY",
                "currency": "EUR",
                "freeForWithdraw": 50000.00,
                "freeForCfdTransfer": 50000.00,
                "total": 50000.00,
                "lockedCash": {
                    "totalLockedCash": 0,
                    "lockedCash": []
                    }
           }
        }

        """
        logger.debug('Requests GET user funds......')
        try:
            url = f"{self.base_url}/rest/customer/accounts/funds"
            result = get_request(url, self.headers, self.cookies)
            return result
        except Exception as exe:
            logger.warning(f'Unable to get funds.{exe}')
            return None



    def get_ticker_info(self, ticker):
        """
        url = "https://demo.trading212.com/rest/v2/account/instruments/settings"

        payload="[\"TSLA_US_EQ\"]"

        response = requests.request("POST", url, headers=headers, data=payload)
        {
            "code": "TSLA_US_EQ",
            "maxBuy": 69.3119,
            "maxSell": 0E-8,
            "maxOpenBuy": 50000000.00000000,
            "maxOpenSell": 50000000.00000000,
            "suspended": false,
        "minTrade": 0.0010000000
        }
        -----------------------------------------------------------------------
        https://demo.trading212.com/rest/v1/equity/value-order/min-max?instrumentCode=AMZN_US_EQ
        {
            "minBuy": 1.00,
            "maxBuy": 43603.55,
            "minSell": 1.00,
            "maxSell": 0.00,
            "sellThreshold": 0.00,
            "maxSellQuantity": 0E-8
        }
        """
        pass

    def submit_buy_order(self, ticker, quantity, type, limit_price=None):
        """
        request - POST
        https://demo.trading212.com/rest/public/v2/equity/order 
        MARKET FRACTIONAL: {"instrumentCode":"AMZN_US_EQ","quantity":0.08,"orderType":"MARKET"}

        LIMIT BUY - {"instrumentCode":"AAPL_US_EQ","orderType":"LIMIT","stopPrice":null,
                    "limitPrice":111,"quantity":3,"timeValidity":"GOOD_TILL_CANCEL"}
            {"limitPrice":111,"quantity":2,"timeValidity":"GOOD_TILL_CANCEL",
            "orderType":"LIMIT","instrumentCode":"TSLA_US_EQ"}    
        """
        url = f"{self.base_url}/rest/public/v2/equity/order"
        if type == "market":
            payload = f'{{"instrumentCode":"{ticker}","quantity":{quantity},"orderType":"MARKET"}}'
            logger.debug(f'Submiting a market order{ticker} - {quantity}')
        elif type == "limit" and limit_price != None:
            # Fractional shares limit and STOP_LIMIT orders are rejected by Trading212
            if quantity < 1:
                return "{INCORRECT ORDER PARAMETERS}"
            payload = f'{{"instrumentCode":"{ticker}","orderType":"LIMIT","stopPrice":null, \
            "limitPrice":{limit_price},"quantity":{quantity},"timeValidity":"GOOD_TILL_CANCEL"}}'
            logger.debug(f'Submiting a limit order{ticker} - {quantity} at price {limit_price}')
        else:
            return "{INCORRECT ORDER PARAMETERS}"

        response = requests.request("POST", url, headers=self.headers, cookies=self.cookies, data=payload)
        logger.debug(response.text)
        return response.text

    def submit_sell_order(self, ticker, quantity, type, limit_price=None, stop_loss = None):
        """
        request - POST
        SELL ORDER -Negative quantity
        LIMIT SELL - {"instrumentCode":"T_US_EQ","orderType":"LIMIT","stopPrice":null,
                      "limitPrice":34,"quantity":-8,"timeValidity":"GOOD_TILL_CANCEL"}
        """
        url = f"{self.base_url}/rest/public/v2/equity/order"
        if type == "market":
            payload = f'{{"instrumentCode":"{ticker}","quantity":-{quantity},"orderType":"MARKET"}}'
            logger.debug(f'Submiting a sell market order{ticker} - {quantity}')
        elif type == "limit" and limit_price != None and stop_loss == None:
            # Fractional shares limit and STOP_LIMIT orders are rejected by Trading212
            if quantity < 1:
                return "{INCORRECT ORDER PARAMETERS}"
            payload = f'{{"instrumentCode":"{ticker}","orderType":"LIMIT","stopPrice":null, \
            "limitPrice":{limit_price},"quantity":-{quantity},"timeValidity":"GOOD_TILL_CANCEL"}}'
            logger.debug(f'Submiting a sell limit order{ticker} - {quantity} at price {limit_price}')
        elif type == "STOP_LIMIT" and limit_price != None and stop_loss != None:
            if quantity < 1:
                return "{INCORRECT ORDER PARAMETERS}"
            payload = f'{{"instrumentCode":"{ticker}","orderType":"STOP_LIMIT","stopPrice":{stop_loss}, \
            "limitPrice":{limit_price},"quantity":-{quantity},"timeValidity":"GOOD_TILL_CANCEL"}}'
            logger.debug(f'Submiting a sell STOP_LIMIT order{ticker} - {quantity} at price {limit_price}')
        else:
            return "{INCORRECT ORDER PARAMETERS}"

        response = requests.request("POST", url, headers=self.headers, cookies=self.cookies, data=payload)
        logger.debug(response.text)
        return response.text

    def submit_cancel_order(self, orderid):
        """
        request - DELETE
        url = "https://demo.trading212.com/rest/public/v2/equity/order/699602058"

        payload={}
        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text)
        """
        url = f"{self.base_url}/rest/public/v2/equity/order{orderid}"
        payload = {}
        response = requests.request("DELETE", url, headers=self.headers, cookies=self.cookies, data=payload)
        logger.debug(response.text)
        return response.text


    def get_order_history(self, start_date = '', end_date = ''):
        """
        request - GET
        https://demo.trading212.com/rest/history/orders?olderThan=&newerThan=&frontend=WC4&filtered=false
        """
        if (start_date == "" and end_date == ""):
            filtered = "false"
        else:
            start_date += "T00%3A00%3A00.000Z"
            end_date += "T23%3A59%3A59.000Z"
            filtered = 'true'
        url = f"{self.base_url}/rest/history/orders?olderThan={end_date}&newerThan={start_date}&frontend=WC4&filtered={filtered}"
        logger.debug(url)
        try:
            return get_request(url, self.headers, self.cookies)
        except Exception as exe:
            logger.warning(f'Unable to get order history {exe}')
            return None


    def get_dividend_history(self, start_date = '', end_date = ''):
        """
        request - GET
        https://demo.trading212.com/rest/history/dividends?olderThan=&newerThan=&frontend=WC4&filtered=false
        https://demo.trading212.com/rest/history/dividends?olderThan=2020-12-31T23%3A59%3A59.000Z
        &newerThan=2020-01-01T00%3A00%3A00.000Z&frontend=WC4&filtered=true
        """
        if (start_date == "" and end_date == ""):
            filtered = "false"
        else:
            start_date += "T00%3A00%3A00.000Z"
            end_date += "T23%3A59%3A59.000Z"
            filtered = 'true'
        url = f"{self.base_url}/rest/history/dividends?olderThan={end_date}&newerThan={start_date}&frontend=WC4&filtered={filtered}"
        try:
            return get_request(url, self.headers, self.cookies)
        except Exception as exe:
            logger.warning(f'Unable to get order history {exe}')
            return None


if __name__ == "__main__":
    pass
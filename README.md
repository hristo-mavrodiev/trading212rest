# trading212rest
Non official API for Trading 212
==========

[![Python version](https://img.shields.io/badge/python-3.6+-blue.svg?style=flat)](https://github.com/hristo-mavrodiev/trading212rest)
[![Travis-CI build status](https://travis-ci.com/hristo-mavrodiev/trading212rest.svg?branch=dev)](https://travis-ci.com/github/hristo-mavrodiev/trading212rest/builds)
[![Star this repo](https://img.shields.io/github/stars/hristo-mavrodiev/trading212rest)](https://github.com/hristo-mavrodiev/trading212rest)


------------------------------------------------------------------------


Quick start
-----------
```
api = Trading212(USERNAME, PASSWORD, DEMO_MODE = True)
api.login()
api.set_session()

# Acount funds
api.get_funds()

# Market buy order
api.submit_buy_order("TSLA_US_EQ", 1, 'market')

# Limit buy order
api.submit_buy_order("TSLA_US_EQ", 1, 'limit', 700)

# Market sell order
api.submit_sell_order("TSLA_US_EQ", 1, 'market')

# Limit sell order
api.submit_sell_order("TSLA_US_EQ", 1, 'limit', 900)

# Sell order Take profit with Stop loss
api.submit_sell_order("TSLA_US_EQ", 1, 'STOP_LIMIT', 60, 40)

# Order History
api.get_order_history("2020-01-01","2020-12-31")

# Dividend History
api.get_dividend_history("2020-01-01","2020-12-31")
```


Sample of the json response after a new order is submited:

```
{
    "account": {
        "dealer": "AVUSUK",
        "positions": [
            {
                "positionId": "0bbba95a-ea0f-4bfc-b0bf-a69fd3969647",
                "humanId": "679433666",
                "created": "2021-01-06T10:00:06.000+02:00",
                "averagePrice": 51.01200000,
                "averagePriceConverted": 51.01200000,
                "currentPrice": 49.527,
                "value": 2476.35,
                "investment": 2550.60,
                "code": "4GLDd_EQ",
                "margin": 2476.35,
                "ppl": -74.25,
                "quantity": 50.0000000000,
                "maxBuy": 837.567,
                "maxSell": 50.00000000,
                "maxOpenBuy": 49999950.00000000,
                "maxOpenSell": 50000000.00000000,
                "frontend": "WC4",
                "autoInvestQuantity": 0E-10
            },
            {
                "positionId": "04d45642-229b-482e-b0b8-7c82e26f4631",
                "humanId": "679726666",
                "created": "2021-01-20T20:41:38.558+02:00",
                "averagePrice": 773.34666667,
                "averagePriceConverted": 630.65500000,
                "currentPrice": 853.90,
                "value": 4232.01,
                "investment": 3783.93,
                "code": "TSLA_US_EQ",
                "margin": 4232.01,
                "ppl": 448.08,
                "quantity": 6.0000000000,
                "maxBuy": 58.8412,
                "maxSell": 6.00000000,
                "maxOpenBuy": 49999994.00000000,
                "maxOpenSell": 50000000.00000000,
                "frontend": "WC4",
                "autoInvestQuantity": 0E-10,
                "fxPpl": 48.793778249591
            }
        ],
        "cash": {
            "free": 43665.47,
            "total": 50373.83,
            "interest": 0.00,
            "indicator": 0,
            "commission": 0.00,
            "cash": 50000.00,
            "ppl": 373.83,
            "result": 0.00,
            "spreadBack": 0.00,
            "nonRefundable": 0.00,
            "dividend": 0.00,
            "stockInvestment": 6334.53,
            "freeForStocks": 43665.47,
            "totalCashForWithdraw": 43665.47,
            "blockedForStocks": 0.00,
            "pieCash": 0
        },
        "limitStop": [],
        "oco": [],
        "ifThen": [],
        "equityOrders": [
            {
                "orderId": "699615641",
                "type": "LIMIT",
                "code": "TSLA_US_EQ",
                "quantity": -1,
                "filledQuantity": 0,
                "status": "NEW",
                "limitPrice": 900,
                "created": "2021-01-20T21:25:55.759+02:00",
                "frontend": "WC4"
            },
            {
                "orderId": "699613640",
                "type": "LIMIT",
                "code": "AMZN_US_EQ",
                "quantity": 1,
                "filledQuantity": 0,
                "status": "NEW",
                "limitPrice": 3000,
                "created": "2021-01-20T21:22:12.076+02:00",
                "frontend": "WC4"
            }
        ],
        "equityValueOrders": [],
        "id": 88888888,
        "timestamp": 1611170755000
    }
}
```

Install system requirements
---------------------------

### On Windows:

  -   Firefox with geckodriver in PATH
  -   Chrome with chrome-driver in PATH

### On Linux:

For Chrome -please check version compatability chrome-driver

``` bash
sudo apt-get update
sudo apt-get install chromium chromium-driver
```

For Firefox -
<https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html>

``` bash
sudo apt-get update
sudo apt-get install wget libgtk-3-0 libdbus-glib-1-2 libxt6

FIREFOX_VERSION=62.0.2 
wget -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2
rm -rf /opt/firefox 
tar -C /opt -xvjf /tmp/firefox.tar.bz2 
rm /tmp/firefox.tar.bz2 
mv /opt/firefox /opt/firefox-$FIREFOX_VERSION 
sudo ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

GECKO_VERSION=0.26.0
wget https://github.com/mozilla/geckodriver/releases/download/v$GECKO_VERSION/geckodriver-v$GECKO_VERSION-linux64.tar.gz  
tar -xvzf geckodriver-v$GECKO_VERSION-linux64.tar.gz   
sudo cp geckodriver /usr/local/bin/
sudo chmod a+x /usr/local/bin/geckodriver
```

Install python requirements on venv
-----------------------------------

### On Windows:

``` bash
python -m venv env
env/Scripts/activate.bat
pip install -r requirements.txt
pip install git+https://github.com/hristo-mavrodiev/trading212rest.git@dev
```

### On Linux:

``` bash
alias python=python3
python -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install git+https://github.com/hristo-mavrodiev/trading212rest.git@dev
```

Python Requirements
-------------------

-   requests&gt;=2.21.0
-   urllib3==1.25.9
-   selenium==3.141.0

License
-------

This project is licensed under the MIT License - see the
[LICENSE.txt](LICENSE.txt)

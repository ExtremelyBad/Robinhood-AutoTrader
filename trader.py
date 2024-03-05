import config

import robin_stocks.robinhood as rh
import datetime as dt
import time
import csv


def login(days):
    time_logged_in = 60*60*24*days
    rh.authentication.login(username=config.USERNAME, password=config.PASSWORD, expiresIn=time_logged_in,
                            scope='internal', by_sms=True, store_session=True, mfa_code=None, pickle_name='')


def logout():
    rh.authentication.logout()


def get_stock():
    # Specify the file path
    file_path = 'tickers.csv'
    stocks = list()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stocks.append(row['TICKER'])

    return stocks


def market_is_open():
    market = False
    time_now = dt.datetime.now().time()

    market_open = dt.time(8,30,0)
    market_close = dt.time(14,59,0)
    if market_open < time_now < market_close:
        market = True
    else:
        print("MARKET IS CLOSED")

    return market


if __name__ == "__main__":
    login(days=7)

    stocks = get_stock()
    print(stocks)

    while market_is_open():
        prices = rh.stocks.get_latest_price(stocks)

        for i, stock in enumerate(stocks):
            price = float(prices[i])
            print("{} = ${}".format(stock, price))

        time.sleep(15)

    logout()





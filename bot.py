import requests
import time
import yfinance as yf
base_url = 'https://api.telegram.org/bot1301051793:AAGUAMh8DMsv5bFtJnCKMrwfSP59zZ_5Rtg/'
def get_updates():
    answ = requests.get(base_url + 'getUpdates')
    return answ.json()
def last_update():
    updates = get_updates()
    return updates['result'][-1]
def get_chat_id(update):
    return update['message']['chat']['id']
def send_message(chat,text):
    par = {'chat_id' : chat,'text' : text}
    return requests.post(base_url + 'sendMessage', data = par)

def get_ask(stock):
    return stock['ask']
def get_bid(stock):
    return stock['bid']
def is_strange_activity(stock,last_price):
    current_price = get_ask(stock)
    delta = current_price - last_price
    is_up = delta > 0
    return delta , is_up, current_price
def make_alert_if_needed(stock, last_price,chat_id):
    delt, direction, price = is_strange_activity(stock,last_price)
    if abs(delt) > 0.0005*price:
        text = '🌊Attention!!!!!!!!!!!!\n Stock {0} ({1}) is in unusual activity.'.format(stock['longName'],stock['symbol'])
        text += '💵Low price : {0}, High: {1}, Current - {2}'.format(stock['dayLow'],stock['dayHigh'],price)
        text += '\n Move on {0}$ to {1}$'.format(delt,price)        
        send_message(chat_id,text)
    return price
def see_all(stock_list,chat_id,last_prices):
    current = 0
    tickers = yf.Tickers(stock_list).tickers
    new_prices = []
    for t in tickers:    
        stock = t.get_info()
        new_prices.append(make_alert_if_needed(stock,last_prices[current],chat_id))
        current += 1
    return new_prices
def get_prices(stocks):
    tickers = yf.Tickers(stocks).tickers
    new_prices = []
    for s in tickers:
        new_prices.append(get_bid(s.get_info()))
    return new_prices

def main():
    stocks = 'NVDA AMD AAPL'
    chat_id = get_chat_id(last_update())
    prices = get_prices(stocks)
    while True:
        prices = see_all(stocks,chat_id, prices)
        time.sleep(40)
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    
    
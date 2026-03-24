import yfinance as yf

stock = fy.Ticker("APPL")
info = stock.info
print(type(info))

print(info.keys())
print(len(info))

print(info['city'])
#info['city'][0] = 'c'
info['city'] = "Wellesley"
print(info['city'])

tickers = ['APPL', 'NVDA', 'META', 'GOOG']
stocks = {} #{'NVDA': open, currentPrice, volume]}

for t in tickers:
    prices[t] = yf.Ticker(t).info['currentPrice'], info['currentPrice'], yf.Ticket(t).info['volume']
print(prices)
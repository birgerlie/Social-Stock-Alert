import pymongo 
import ystockquote
import json
import datetime, time

from pymongo import Connection
from TimeSeriesRecorder import TimeSeriesRecorder

class StockCollector:
 def __init__(self):
  self.stocks = ['ATVI', 'ADBE', 'ALTR', 'AMZN', 'APCC', 'AMGN', 'APOL', 'AAPL', 'AMAT', 'ATYT', 'ADSK', 'BEAS', 'BBBY', 'BIIB', 'BMET', 'BRCM', 'CDNS', 'CDWC', 'CELG', 'CHRW', 'CHKP', 'CKFR', 'CHIR', 'CTAS', 'CSCO', 'CTXS', 'CTSH', 'CMCSA', 'CMVT', 'COST', 'DELL', 'XRAY', 'DISCA', 'EBAY', 'DISH', 'ERTS', 'EXPE', 'EXPD', 'ESRX', 'FAST', 'FISV', 'FLEX', 'GRMN', 'GENZ', 'GILD', 'GOOG', 'IACI', 'INTC', 'INTU', 'JDSU', 'JNPR', 'KLAC', 'LRCX', 'LAMR', 'LBTYA', 'LNCR', 'LLTC', 'ERICY', 'MRVL', 'MXIM', 'MCIP', 'MEDI', 'MERQ', 'MCHP', 'MSFT', 'MNST', 'NTAP', 'NIHD', 'NVLS', 'NTLI', 'NVDA', 'ORCL', 'PCAR', 'PDCO', 'PTEN', 'PAYX', 'PETM', 'PIXR', 'QCOM', 'RHAT', 'RIMM', 'ROST', 'SNDK', 'SHLD', 'SEPR', 'SEPR', 'SIRI', 'SPLS', 'SBUX', 'SUNW', 'SYMC', 'TLAB', 'TEVA', 'URBN', 'VRSN', 'WFMI', 'WYNN', 'XLNX', 'XMSR', 'YHOO', 'MMM', 'AA', 'AXP', 'BAC', 'BA', 'CAT', 'CVX', 'CSCO', 'KO', 'DD', 'XOM', 'GE', 'HPQ', 'HD', 'INTC', 'IBM', 'JNJ', 'JPM', 'KFT', 'MCD', 'MRK', 'MSFT', 'PFE', 'PG', 'TRV', 'UTX', 'VZ', 'WMT', 'DIS']
  self.db = Connection('localhost',27017).production
  self.ts_volume = TimeSeriesRecorder('stock_volume')
  self.ts_price = TimeSeriesRecorder('stock_price')

 def fetch_stock_data(self):
  times = 1

  while times == 1:
   for ticker in self.stocks:
    data = ystockquote.get_all(ticker)
    data['ticker'] = ticker
    data['time_stamp'] = datetime.datetime.now()   
    self.save_stock_data(data)
	
    if data['volume'].isdigit() and data['price'].isdigit():    
     self.ts_volume.onSample(ticker, int( data['volume']))
     self.ts_price.onSample(ticker,float(data['price']))
    print('.'),
   print ''
   time.sleep(60)
 
 def save_stock_data(self, data):
  self.db.stocks.save(data)


collector =  StockCollector()
collector.fetch_stock_data()
    

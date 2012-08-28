import datetime, pymongo, config, re
from datetime import datetime, timedelta
from pymongo import Connection



class TickerStats:
  def __init__(self):
    self.db = Connection(config.db_host, config.db_port).production
    self.exp = re.compile('\\$[A-Z]+')    
    self.tickers = [ticker[1:] for ticker in self.exp.findall(open('stock.txt', 'r').read())]
    self.duration = timedelta(minutes=5)
  
  def build_timeseries(self,start,end):
    for ticker in self.tickers:
      ticker_data = [v for v in  self.db.stocks.find({'time_stamp':{'$gte':start, "$lt":end},'ticker':ticker})]
      start_time  = start
      print 'ticker: ', ticker	      
      while(start_time  < end):
	 span = start_time + self.duration
	 points = [[d['volume'],d['price']] for d in ticker_data if d['time_stamp'] >= start_time and  d['time_stamp'] < span and d['volume'] != 'N/A']
	 count = len( points)
	 volume = 0
	 price = 0
	 print '.',
	 if count > 0 :
	   #print points
	   volume = sum([float(pv[0]) for pv in points ])/count
	   price  = sum([float(pp[1]) for pp in points])/count
	 data = {}
         data['_id']= ticker +'--'+ span.isoformat() 	 
         data['ticker'] = ticker
    	 data['ts'] = span
	 data['vol']= volume
 	 data['prc']= price	 
	 data['dt'] = self.duration.seconds
	 self.db.stock_ts.save(data)
		
         start_time += self.duration 
         
				     
      	    	
  


ts = TickerStats()
ts.build_timeseries(datetime(2012,7,27,12),datetime(2012,8,28))

	  
       #create avg pr durationi
       	 

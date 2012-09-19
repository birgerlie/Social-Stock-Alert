import pymongo,config,datetime, re

from pymongo import Connection
from datetime import datetime, timedelta

class TwitterStats:
 def __init__(self):
	self.db = Connection(config.db_host, config.db_port).production
	self.exp = re.compile('\\$[A-Z]+')
	self.tickers = [ticker[1:] for ticker in self.exp.findall(open('stock.txt', 'r').read())]
 	self.duration = timedelta(minutes=5)

 def ticker_volume(self,start):
	averages =  dict.fromkeys(self.tickers, 0)
	end = start + self.duration	
        for tweet in self.db.tweets.find({'time_stamp':{'$gte':start, "$lt":end}}):
          for ticker in tweet['tickers']:
           if averages.has_key(ticker): 
	     averages[ticker] +=1
        #print averages
        return averages
 
 def build_data(self,start):
	
	delta_start = start - self.duration
	previous = self.ticker_volume(delta_start)
	current = self.ticker_volume(start)
	
	delta = {}
	for ticker in current.keys():	
	 delta[ticker] = current[ticker] - previous[ticker]
 	return current,delta	

 
 def build_stats(self,start):
	current_time = start
	while datetime.now() > current_time:
	  current, delta = self.build_data(current_time)
	  for ticker in current.keys():	 
	    ticker_data = {'ticker':ticker}
	    ticker_data['_id']= ticker +'--'+ current_time.isoformat() 	
	    ticker_data['v'] = current[ticker] 
	    ticker_data['dv']= delta[ticker]	
            ticker_data['ts']= current_time
	    ticker_data['dt']= self.duration.seconds	
	    self.db.stats.save(ticker_data)		
	  current_time += self.duration
	
 def ticker_stats(self,from_dt,to_dt, ticker):
   data = []		
   for ticker_stat in self.db.stats.find({'ts':{'$gt':from_dt, "$lt":to_dt},'ticker':ticker }):	
     data.append(ticker_stat)	  	
   return data

	
#4925 7858 3087 0218   /    02/13   / 0218    989		
#loop over each time delta and calculate the averages and store them
stat = TwitterStats()
stat.build_stats(datetime(2012,8,28))
#print [[ticker['dv'],ticker['v']]  for ticker in stat.ticker_stats(datetime(2012,7,28),datetime(2012,7,29), 'AMZN')]


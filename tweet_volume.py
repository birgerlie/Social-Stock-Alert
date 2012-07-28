import pymongo,config,datetime, re

from pymongo import Connection
from datetime import datetime, timedelta

class TwitterStats:
 def __init__(self):
	self.db = Connection(config.db_host, config.db_port).production.tweets
	self.exp = re.compile('\\$[A-Z]+')
	self.tickers = [ticker[1:] for ticker in self.exp.findall(open('stock.txt', 'r').read())]
 
 def build_stat(self,start, duration):
	averages =  dict.fromkeys(self.tickers, 0)
	end = start + duration	
        for tweet in self.db.find({'time_stamp':{'$gt':start, "$lt":end}}):
          for ticker in tweet['tickers']:
           if averages.has_key(ticker): 
	     averages[ticker] +=1
        #print averages
        return averages
 
 def build_delta(self,start,duration):
	
	delta_start = start - duration
	previous = self.build_stat(delta_start, duration)
	current = self.build_stat(start, duration)
	
	delta = {}
	for ticker in current.keys():	
	 delta[ticker] = current[ticker] - previous[ticker]
 	return delta	

#4925 7858 3087 0218   /    02/13   / 0218    989		
#loop over each time delta and calculate the averages and store them
stat = TwitterStats()
#stat.build_stat( datetime(2012,7,28),timedelta(minutes=5)
print  stat.build_delta(datetime(2012,7,28),timedelta(minutes=10))

import pymongo,config,datetime, re

from pymongo import Connection, ASCENDING
from datetime import datetime, timedelta


class TimeSeriesRecorder: 
 def __init__(self,name ):
  self.db = Connection(config.db_host, config.db_port).production
  self.name = name
  self.metric = {'month':self.month_key,'week':self.week_key,'day':self.day_key,'hour':self.hour_key } 	  

  for resolution in self.metric: 	
   self.db['_'.join([self.name,resolution])].ensure_index( [('event', ASCENDING), ('ts', ASCENDING)] )  
   	
  
	
 def onSample(self,event, count, ts = datetime.now()):
  sample = {"$inc":{"count":count},"$set":{'event':event}}
  for m in self.metric:
   key_ts=  self.metric[m](event,ts)
   sample['$set']['ts']= key_ts[1]	
   dbname ='_'.join([self.name,m])
   self.db[dbname].update({'_id': key_ts[0]}, sample, True)  		

 def month_key(self, event, ts):
  return (":".join([event,self.year(ts),self.month(ts)]), datetime(ts.year,ts.month,1)) 

 def week_key(self,event,ts):
  return ":".join([event,self.year(ts),self.week(ts)]),ts.isocalendar()
 
 def day_key(self,event, ts):
  return ":".join([event,self.year(ts),self.month(ts),self.day(ts)]),datetime(ts.year,ts.month,ts.day) 
 
 def hour_key(self,event,ts):
  return ":".join([event,self.year(ts),self.month(ts),self.day(ts),self.hour(ts)]), datetime(ts.year,ts.month,ts.day,ts.hour) 

 def week(self, ts): 
  return str(ts.isocalendar()[1])  
 def year(self,ts):
  return str(ts.year)
 def month(self,ts):
  return str(ts.month)
 def day(self, ts):
  return str(ts.day)
 def hour(self,ts):
  return str(ts.hour)

 def update_old_tweets(self):
  ts = datetime.now()
  for tweet in self.db.tweets.find({'time_stamp':{'$lt':ts}}):	
   for ticker in tweet['tickers']:
     self.onSample(ticker,1, tweet['time_stamp'])   	
     print '.',

if __name__ == "__main__":
  ts = TimeSeriesRecorder('twitter_volume')
  ts.update_old_tweets()		


import pymongo,config,datetime, re

from pymongo import Connection, ASCENDING
from datetime import datetime, timedelta

class TimeSeries: 
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
  return (":".join([event,self.year(),self.month()]), datetime(ts.year,ts.month,1)) 

 def week_key(self,event,ts):
  print event
  r =  ":".join([event,self.year(),self.week()]),ts.isocalendar()
  print r  
  return r
 
 def day_key(self,event, ts):
  return ":".join([event,self.year(),self.month(),self.day()]),datetime(ts.year,ts.month,ts.day) 
 
 def hour_key(self,event,ts):
  return ":".join([event,self.year(),self.month(),self.day(),self.hour()]), datetime(ts.year,ts.month,ts.day,ts.hour) 

 def week(self): 
  return str(datetime.now().isocalendar()[1])  
 def year(self):
  return str(datetime.now().year)
 def month(self):
  return str(datetime.now().month)
 def day(self):
  return str(datetime.now().day)
 def hour(self):
  return str(datetime.now().hour)




if __name__ == "__main__":
  ts = TimeSeries('test')
  ts.onSample('goog',1)
		

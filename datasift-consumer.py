#!/usr/bin/python
import datasift, config, sys, pymongo, datetime, time,re,TimeSeriesRecorder
from pymongo import Connection
from TimeSeriesRecorder import TimeSeriesRecorder	 
class EventHandler(datasift.StreamConsumerEventHandler):	   
 def __init__(self):
  self.db = Connection(config.db_host, config.db_port).production
  self.exp = re.compile('\\$[A-Z]+')
  print TimeSeriesRecorder
  self.timeseries = TimeSeriesRecorder('twitter_volume') 
     
 def on_connect(self, consumer):
  print 'Connected'
  print ' '

 def on_interaction(self, consumer, interaction, hash):
  print '.',
  interaction['_id'] = interaction['interaction']['id']
  interaction['time_stamp'] = datetime.datetime.now()
  interaction['tickers'] = [ticker[1:] for ticker in self.exp.findall(interaction['interaction']['content'])] 
  self.db.tweets.save(interaction)
  for ticker in interaction['tickers']:
    self.timeseries.onSample(ticker,interaction['time_stamp'])
 
 def on_deleted(self, consumer, interaction, hash):
  sys.stdout.write('X')

 def on_warning(self, consumer, message):
  print
  print 'WARN: %s' % (message)

 def on_error(self, consumer, message):
  print
  print 'ERR: %s' % (message)
	
 def on_disconnect(self, consumer):
  print
  print 'Disconnected'

dsl = open('stock.txt', 'r').read()
usr = datasift.User(config.username, config.api_key)
definition = usr.create_definition(dsl)
consumer = definition.get_consumer(EventHandler(), 'http')
consumer.consume()
consumer.run_forever()






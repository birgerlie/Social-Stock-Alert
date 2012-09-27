import pymongo,config,datetime, re
from pymongo import Connection
import json
from datetime import datetime, timedelta
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import re
import config
from TimeSeriesRecorder import TimeSeriesRecorder	 
from datetime import datetime


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
    	print 'new connection'
    	self.write_message("Hello World")
      
    def on_message(self, message):
    	print 'message received %s' % message

    def on_close(self):
      print 'connection closed'

class TwitterHandler(tornado.web.RequestHandler):
  
 def get(self):
  data = {'ticker':'$MSFT'}
  ticker = self.get_argument('ticker', default='GOOG', strip=True)	
  n = datetime.now()
  data = twitter_data.fetch_ts(ticker.upper(),datetime(n.year,n.month,n.day -14), n)
  self.set_header("Content-Type", "application/json; charset=UTF-8")
  self.write(json.dumps( data))


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', TwitterHandler)
])

twitter_data = TimeSeriesRecorder('twitter_volume')
db = Connection(config.db_host, config.db_port).production

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8889)
    tornado.ioloop.IOLoop.instance().start()


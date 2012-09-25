import pymongo,config,datetime, re
from pymongo import Connection
from datetime import datetime, timedelta
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import re
import config

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
  self.write(ticker)

 def load_twitter_volume(self,ticker):
   

tickers = [ticker[1:] for ticker in re.compile('\\$[A-Z]+').findall(open('stock.txt', 'r').read())]
application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', TwitterHandler)
])

db = Connection(config.db_host, config.db_port).production

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


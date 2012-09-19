import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import pymongo,config,datetime, re

from pymongo import Connection

from tornado.options import define, options

define("port", default=8880, help="run on the given port", type=int)

class Application(tornado.web.Application):
 def __init__(self):
   handlers = [
    (r"/", MainHandler),
    (r"/twitter-volume", TwitterVolumeHandler)
    ]


   settings = dict(
 	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__),"static"),
	xsrf_cookies=True,
	autoescape=None,
	)
   tornado.web.Application.__init__(self,handlers, **settings)

class MongoHandler(tornado.web.RequestHandler):
  def __init__(self):
   self.db = Connection(config.db_host, config.db_port).production
   self.tickers = [ticker[1:] for ticker in self.exp.findall(open('stock.txt', 'r').read())]

class MainHandler(MongoHandler):
  def get(self):
    self.content_type = 'application/text' 	   
    self.write("helo world")

class TwitterVolumeHandler(MongoHandler):
  def get(self):
   self.write("hello")


	
def main():
 tornado.options.parse_command_line()
 http_server = tornado.httpserver.HTTPServer(Application())
 http_server.listen(options.port)
 tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
   main()



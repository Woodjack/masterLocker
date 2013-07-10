import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import rest
#This is used to produce a properly formated json-array,
from bson.json_util import dumps


port = int(os.environ.get('PORT', '8080'))


htmlDocument = '"<HTML>  hello world \n</HTML>"'

#port options for webServer
from tornado.options import define, options
define("port", default=port, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", RequestHandler)]
        tornado.web.Application.__init__(self, handlers, debug=True)


class RequestHandler(tornado.web.RequestHandler):
    def get(self, urlInput):
    	urlInput = str(urlInput)
        if urlInput == "home":
        	self.write(htmlDocument)
        elif urlInput == "get":
        	self.write( rest.getMONGO() )
        else:
            self.set_status(404)
            self.write({"error": "word not found"})


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




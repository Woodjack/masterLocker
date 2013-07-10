## 
##
## http service that runs continously, and serves up a json-array of results from a mongoDB
## see the readme for more information
##
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo

#This is used to produce a properly formated json-array,
from bson.json_util import dumps

port = int(os.environ.get('PORT', '8080'))


htmlDocument = '"<HTML>  hello world \n</HTML>"'


#port options for webServer
from tornado.options import define, options
define("port", default=port, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        	(r"/rest/(\w+)", RequestHandler),
        	(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
        	(r"/", indexhtmlhandler)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)


def getMONGO():
    connection = pymongo.Connection( 'mongodb://pull:pull@dharma.mongohq.com:10014/app16815592' )
    db = connection.app16815592
    coll = db.location
    query = {}
    mongoResults = coll.find()
    if mongoResults:
    	results = dumps(mongoResults)
        return(results)
    else:
        return("No Results")

class indexhtmlhandler(tornado.web.RequestHandler):
	def get(self):
		self.render("static/index.html")

class RequestHandler(tornado.web.RequestHandler):
    def get(self, urlInput):
    	urlInput = str(urlInput)
        if urlInput == "home":
        	self.write(htmlDocument)
        elif urlInput == "get":
            self.write( getMONGO() )
        else:
            self.set_status(404)
            self.write({"error": "word not found"})


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




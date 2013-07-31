import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import rest
import datetime
import cookies
from bson.json_util import dumps  ##This is used to produce a properly formated json-array,

import pprint

import ast
port = int(os.environ.get('PORT', '8080'))



from tornado.options import define, options
define("port", default=port, help="run on the given port", type=int) #port options for webServer


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/rest/post", postRequestHandler),
            (r"/rest/get", getRequestHandler),
            (r"/rest/get/live", getLiveRequestHandler),
            (r"/rest/get/current", getCurrentRequestHandler),
            (r"/rest/get/tails", getCurrentRequestHandler),
            (r"/admin/rest/dumpallpoints", dumpallpointsHandler),
            (r"/user", User),
        	(r"/(.+)", tornado.web.StaticFileHandler, {"path": "static"}),
        	(r"/", indexhtmlhandler)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)


class indexhtmlhandler(tornado.web.RequestHandler):
	def get(self):
		self.render("static/index.html")

class getRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.getMONGO() )

class getLiveRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Cache-control", "no-cache")
        self.write( rest.getLiveMONGO() )

class getCurrentRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.getCurrentMONGO() )

class getTailsRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.getTailsMONGO() )

class postRequestHandler(tornado.web.RequestHandler):
    def get(self):
        data={}
        cookieName = "wheresjack"
        if not self.get_cookie( cookieName ):
            self.set_cookie( cookieName , cookies.bakeCookie() )
            self.write("Cookie is now set")
        else:
            self.write("Cookie is " + cookieName)
            data['cookie'] = self.get_cookie(cookieName)
        data['name'] = self.get_argument('name')
        data['loc'] = {}
        data['loc']['x'] = self.get_argument('x')
        data['loc']['y'] = self.get_argument('y')
        results = rest.postLocation(data)
        self.write(results)

class dumpallpointsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.dumpallpoints() )

class User(tornado.web.RequestHandler):
    def get(self):
        cookieName = "wheresjack"
        if not self.get_cookie( cookieName ):
            self.set_cookie( cookieName , cookies.bakeCookie() )
            self.write("Cookie is now set")
        else:
            cookieValue = self.get_cookie(cookieName, default=None)
            self.write("Cookie name is:   " + cookieName)
            self.write("Cookie value is:  " + cookieValue)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




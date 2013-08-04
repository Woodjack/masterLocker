import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import rest
import datetime
from cookies import bakeCookie
from bson.json_util import dumps  ##This is used to produce a properly formated json-array,

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
            (r"/admin/rest/dumpallpoints", dumpallpointsHandler),
            (r"/cookie", cookieRequestHandler),
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
        self.write( rest.getLiveMONGO() )

class getCurrentRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.getCurrentMONGO() )

class postRequestHandler(tornado.web.RequestHandler):
    def get(self):
        data={}
        data['date'] = datetime.datetime.utcnow()
        if self.get_argument('cookie'):
            data['cookie'] = self.get_argument('cookie')
        if self.get_argument('name'):
            data['name'] = self.get_argument('name')
        if self.get_argument('x') and self.get_argument('y'):
            data['loc'] = {}
            data['loc']['x'] = float(self.get_argument('x'))
            data['loc']['y'] = float(self.get_argument('y'))
        results = rest.postLocation(data)
        self.write(results)

class cookieRequestHandler(tornado.web.RequestHandler):
    def get(self):
        cookieName = str('wheresjack')
        cookieValue = cookies.bakeCookie()
        data = {}
        data['cookie'] = cookieValue
        newUser['date'] = datetime.datetime.utcnow()
        if self.get_argument('name'):
            data['name'] = self.get_argument('name')
        if self.get_argument('x') and self.get_argument('y'):
            data['loc'] = {}
            data['loc']['x'] = float(self.get_argument('x'))
            data['loc']['y'] = float(self.get_argument('y'))
        results = rest.postNewUser(data)


class dumpallpointsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.dumpallpoints() )


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




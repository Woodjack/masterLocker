import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import rest
import datetime
import cookies
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
            (r"/rest/get/live", getLiveRequestHandler),
            (r"/rest/get/current", getCurrentRequestHandler),
            (r"/admin/rest/dumpallpoints", dumpallpointsHandler),
            (r"/cookie", cookieRequestHandler),
            (r"/updatename", updateNameRequestHandler),
        	(r"/(.+)", tornado.web.StaticFileHandler, {"path": "static"}),
        	(r"/", indexhtmlhandler)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)

class indexhtmlhandler(tornado.web.RequestHandler):
	def get(self):
		self.render("static/index.html")

class getLiveRequestHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie('id'):
            self.write( rest.getLive(self.get_cookie('id')) )
        else:
            print('getLive  did not find a cookie')

class getCurrentRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.getCurrentMONGO() )

class postRequestHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            data={}
            data['date'] = datetime.datetime.utcnow()
            data['cookie'] = self.get_cookie('id')
            data['name'] = self.get_cookie('name')
            data['loc'] = {}
            data['loc']['x'] = float(self.get_argument('x'))
            data['loc']['y'] = float(self.get_argument('y'))
            rest.postLocation(data)
            self.write('postRequest worked!!')
        except:
            self.write('postRequest failed amigo, try again')

class cookieRequestHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie( 'id' ):
            data = {}
            data['cookie'] = cookies.bakeCookie()
            data['date'] = datetime.datetime.utcnow()
            data['name'] = self.get_argument('name')
            print('cookie baked!!  Username: ' + str(data['name'] ))
            self.set_cookie( 'id' , str(data['cookie']) ,expires_days=14 )
            self.set_cookie( 'name' , str(data['name']) ,expires_days=14 )
            rest.postNewUser(data)
            self.write('New Cookies generated successfully')
        else:
            self.write('Cookie already there')

class updateNameRequestHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            id_cookieValue = cookies.bakeCookie()
            data = {}
            data['cookie'] = id_cookieValue
            data['date'] = datetime.datetime.utcnow()
            data['name'] = self.get_argument('name')
            self.write('cookie updated!!')
            self.set_cookie( 'id' , str(id_cookieValue) ,expires_days=14 )
            self.set_cookie( 'name' , str(data['name']) ,expires_days=14 )
            rest.updateUserName(data)
        except:
            self.write('no cookie found')

class dumpallpointsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.dumpallpoints() )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




import os
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import rest
import datetime
import cookies
from cookies import bakeCookie
import json
import ast

port = int(os.environ.get('PORT', '8080'))

from tornado.options import define, options
define("port", default=port, help="run on the given port", type=int) #port options for webServer

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/rest/get/current", getCurrentRequestHandler),
            (r"/admin/rest/dumpallpoints", dumpallpointsHandler),
            (r"/cookie", cookieRequestHandler),
            (r"/updatename", updateNameRequestHandler),
            (r"/ws", WSHandler),
        	(r"/(.+)", tornado.web.StaticFileHandler, {"path": "static"}),
        	(r"/", indexhtmlhandler)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)

class indexhtmlhandler(tornado.web.RequestHandler):
	def get(self):
		self.render("static/index.html")

class getCurrentRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.getCurrentMONGO() )

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

class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def open(self):
        self.clients.append(self)
        self.id = cookies.bakeCookie()
        print 'new connection id=', self.id
        self.write_message("connection acknowledged")

    def on_message(self, message):
        print self.clients

        clientdata = json.loads(message)

        print 'clientdata', repr(clientdata)
        
        action = clientdata['action']

        if action == 'updatelocation':
            data = {}
            data['date'] = datetime.datetime.utcnow()
            data['cookie'] = self.id
            data['name'] = self.name
            data['loc'] = clientdata['data']
            rest.postLocation(data)

            livedata = {}
            livedata['action'] = 'liveclients'
            livedata['data'] = rest.getLive()

            for client in self.clients:
                client.write_message(livedata)
        elif action == 'setname':
            self.name = clientdata['data']


    def on_close(self):
        self.clients.remove(self)
        print 'closed connection'



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




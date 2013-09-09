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

port = int(os.environ.get('PORT', 80))

from tornado.options import define, options
define("port", default=port, help="run on the given port", type=int) #port options for webServer

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/admin/rest/dumpallpoints", dumpallpointsHandler),
            (r"/ws", WSHandler),
        	(r"/(.+)", tornado.web.StaticFileHandler, {"path": "static"}),
        	(r"/", indexhtmlhandler)
        ]
        tornado.web.Application.__init__(self, handlers, debug=True)

class indexhtmlhandler(tornado.web.RequestHandler):
	def get(self):
		self.render("static/index.html")

class dumpallpointsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write( rest.dumpallpoints() )



class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def open(self):
        self.clients.append(self)
        self.id = cookies.bakeCookie()
        print 'new connection id=', self.id
        livedata = {}
        livedata['action'] = 'liveclients'
        livedata['data'] = rest.getLive()
        self.write_message(livedata)
        self.write_message("connection acknowledged")

    def on_message(self, message):
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

            queryList = []
            for client in self.clients:
                queryList.append(client.id)


            livedata['data'] = rest.getLive( queryList )
            
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
    print port
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()




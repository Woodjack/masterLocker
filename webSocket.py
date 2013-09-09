import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.options
import tornado.web
import os
port = int(os.environ.get('PORT', '8080'))


from tornado.options import define, options
define("port", default=port, help="run on the given port", type=int) #port options for webServer








class WSHandler(tornado.websocket.WebSocketHandler):
    clients = []

    def open(self):
        self.clients.append(self)
        print 'new connection'
        self.write_message("Hello World")

    def on_message(self, message):
        print 'message received %s' % message

    def on_close(self):
        self.clients.remove(self)
        print 'closed connection'









application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()


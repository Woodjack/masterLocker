import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

# server info
port = int(os.environ.get('PORT', '8080'))

if __name__ == "__main__":
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

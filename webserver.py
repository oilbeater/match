import tornado.ioloop
import tornado.web
import simplejson as json
import pika
import ConfigParser


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        print(self.__dict__)

    def post(self):
        x = json.loads(self.request.body)
        print(self.request.body)
application = tornado.web.Application([(r"/", MainHandler), ])

if __name__ == "__main__":

    application.listen(80)
    tornado.ioloop.IOLoop.current().start()

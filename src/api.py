import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define

from db import Lab


define("port", default=8080, help="run on the given the port", type=int)


class LabHandler(tornado.web.RequestHandler):
    def get(self):
        args = self.get_query_arguments('fields')
        print "recdv args in get handler"
        print args
        print Lab.getAllLabs()
        self.finish({'labs': Lab.getAllLabs()})


def make_app():
    return tornado.web.Application([
        tornado.web.url(r'/labs', LabHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

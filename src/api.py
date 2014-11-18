import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define

from db import Lab


define("port", default=8080, help="run on the given the port", type=int)


class LabHandler(tornado.web.RequestHandler):
    # executes when GET method is recvd
    def get(self):
        # get the fields attributes from query string
        fields = self.get_query_argument('fields').split(',')
        try:
            self.finish({'labs': Lab.getAllLabs(fields)})
        except:
            self.set_status(400)
            self.finish("Invalid Field attribute")


def make_app():
    return tornado.web.Application([
        tornado.web.url(r'/labs', LabHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

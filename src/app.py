# -*- coding: utf-8 -*-

from mongoengine import connect
import tornado.web
import tornado.ioloop

connection = connect('labs-info')

import api


def make_app():
    return tornado.web.Application([
        tornado.web.url(r'/labs/?', api.LabHandler),
        tornado.web.url(r'/labs/discipline/([a-z]*)', api.DisciplineHandler),
        tornado.web.url(r'/labs/institute/(\w+)/?discipline/?(\w+)?',
                        api.InstituteHandler),
        tornado.web.url(r'/labs/([0-9a-z]*)/?(\w+)?', api.LabIdHandler)
    ])

app = make_app()

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

# -*- coding: utf-8 -*-

from mongoengine import connect
import tornado.web
import tornado.ioloop

connection = connect('test-labs-info')

from api import make_app

app = make_app()

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

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
	
    def get(self, word):
        coll = Lab._get_collection()       
	word_doc = coll.find_one({"lab_id": word})
        if word_doc:
            word_doc["_id"] = str(word_doc["_id"])
	    self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})



def make_app():
    return tornado.web.Application([
        tornado.web.url(r'/labs', LabHandler),
        tornado.web.url(r'/labs/(\w+)', LabHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

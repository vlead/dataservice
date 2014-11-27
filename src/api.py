import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define
from bson.objectid import ObjectId
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
            self.finish({'error': 'Invalid field attribute'})

    # POST Method for /labs
    # Create a new lab
    def post(self):
        err = None
        if not self.get_body_argument('lab_name'):
            err = 'Field lab_name cannot be empty'

        if not self.get_body_argument('institute_name'):
            err = 'Field institute_name cannot be empty'

        if not self.get_body_argument('discipline_name'):
            err = 'Field discipline_name cannot be empty'

        if not self.get_body_argument('repo_url'):
            err = 'Field repo_url cannot be empty'

        if err:
            self.set_status(400)
            self.finish({"error": err})

        args = {}
        for field in self.request.arguments:
            args[field] = self.get_body_argument(field)

        new_lab = Lab(**args)
        new_lab.save()
        self.finish(new_lab.to_client())

    # PUT method for /labs
    # Update an existing lab identified by lab_id
    def put(self, lab_id):
        #lab = Lab.objects(__raw__={"_id": ObjectId(lab_id)})[0]
        lab = Lab.getLabById(lab_id)
        #print(self.request.arguments)
        for field in self.request.arguments:
            lab[field] = self.get_body_argument(field)

        print 'updated lab ' + lab_id
        print lab.to_dict()

        lab.save()
        self.finish({'updated_lab': lab.to_client()})


class LabIdHandler(tornado.web.RequestHandler):
    def get(self, word):
        coll = Lab._get_collection()
        word_doc = coll.find_one({"_id": ObjectId(word)})
        if word_doc:
            word_doc["_id"] = str(word_doc["_id"])
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})


class DisciplineHandler(tornado.web.RequestHandler):
    def get(self, word):
        word_doc = Lab.objects(discipline_name=word).to_json()
        if word_doc:
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})


def make_app():
    return tornado.web.Application([
        tornado.web.url(r'/labs', LabHandler),
        tornado.web.url(r'/labs/([0-9a-z]*)', LabHandler),
        tornado.web.url(r'/labs/([0-9a-z]*)', LabIdHandler),
        tornado.web.url(r'/labs/disciplines/([a-z]*)', DisciplineHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

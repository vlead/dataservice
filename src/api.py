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

    def post(self):
        if not self.get_body_argument('lab_name'):
	    self.set_status(400)
	    self.write({"error":"lab name required"})

	if not self.get_body_argument('institute_name'):
            self.set_status(400)
            self.write({"error":"institute name required"})

	if not self.get_body_argument('discipline_name'):
            self.set_status(400)
            self.write({"error":"discipline name required"})
	
	if not self.get_body_argument('repo_url'):
	    self.set_status(400)
            self.write({"error": "repo url not found"})

	

        new_lab = Lab(lab_id = self.get_body_argument('lab_id'),
                      institute_name = self.get_body_argument('institute_name'),
                      lab_name = self.get_body_argument('lab_name'),
		      discipline_name = self.get_body_argument('discipline_name'),
		      developers = self.get_body_argument('developer'),
                      repo_url = self.get_body_argument('repo_url'),
                      sources_available = self.get_body_argument('sources_available'),
                      hosted_url = self.get_body_argument('hosted_url'),
                      lab_deployed = self.get_body_argument('lab_deployed'),
                      numb_of_exps = self.get_body_argument('number_of_experiments'),
                      content = self.get_body_argument('content'),
                      simulation  = self.get_body_argument('simulation'),
                      web_2_compliance = self.get_body_argument('web_2_compliance'),
                      type_of_lab = self.get_body_argument('type_of_lab'),
                      auto_hostable = self.get_body_argument('auto_hostable'),
                      remarks = self.get_body_argument('remarks'),
                      integration_level = self.get_body_argument('integration_level'),
                      status = self.get_body_argument('status')
                     )

	new_lab.save()
	self.finish(new_lab.to_json())
        

def make_app():
    return tornado.web.Application([
        tornado.web.url(r'/labs', LabHandler),
        tornado.web.url(r'/labs/(\w+)', LabHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

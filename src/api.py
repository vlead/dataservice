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


    def get(self, lab_id, param):
        lab = Lab.getLabById(lab_id)        
        
        try:
            self.finish({param: lab[param]})
        except:
            self.set_status(400)
            self.finish({'error': 'Invalid Field Name'})



    def post(self):
        if not self.get_body_argument('lab_name'):
	    self.set_status(400)
	    self.write({"error": "lab name required"})

	if not self.get_body_argument('institute_name'):
            self.set_status(400)
            self.write({"error": "institute name required"})

	if not self.get_body_argument('discipline_name'):
            self.set_status(400)
            self.write({"error": "discipline name required"})

	if not self.get_body_argument('repo_url'):
	    self.set_status(400)
            self.write({"error": "repo url required"})


        new_lab = Lab(**self.request.arguments)
        #new_lab = Lab(lab_id = self.get_body_argument('lab_id'),
        #              institute_name = self.get_body_argument('institute_name'),
        #              lab_name = self.get_body_argument('lab_name'),
	#	      discipline_name = self.get_body_argument('discipline_name'),
	#	      developers = self.get_body_argument('developer'),
        #              repo_url = self.get_body_argument('repo_url'),
        #              sources_available = self.get_body_argument('sources_available'),
        #              hosted_url = self.get_body_argument('hosted_url'),
        #              lab_deployed = self.get_body_argument('lab_deployed'),
        #              numb_of_exps = self.get_body_argument('number_of_experiments'),
        #              content = self.get_body_argument('content'),
        #              simulation  = self.get_body_argument('simulation'),
        #              web_2_compliance = self.get_body_argument('web_2_compliance'),
        #              type_of_lab = self.get_body_argument('type_of_lab'),
        #              auto_hostable = self.get_body_argument('auto_hostable'),
        #              remarks = self.get_body_argument('remarks'),
        #              integration_level = self.get_body_argument('integration_level'),
        #              status = self.get_body_argument('status')
        #             )

	new_lab.save()
	self.finish(new_lab.to_client())

    def put(self, lab_id):
        #lab = Lab.objects(__raw__={"_id": ObjectId(lab_id)})[0]
        lab = Lab.getLabById(lab_id)

        #print(self.request.arguments)

        for field in self.request.arguments:
            lab[field] = self.get_body_argument(field)

        print 'updated lab ' + lab_id
        print lab.to_dict()

        #instt_name = self.get_body_argument('institute_name', default="")
        #if instt_name:
        #    lab['institute_name'] = instt_name

        #l_name = self.get_body_argument('lab_name', default = "")
        #if l_name:
        #    lab['lab_name'] = l_name

	#disc_name = self.get_body_argument('discipline_name', default = "")
        #if disc_name:
        #    lab['discipline_name'] = disc_name

        #dev = self.get_body_argument('developer', default = "")
	#if dev:
	#    lab['developer'] = dev

        #repo = self.get_body_argument('repo_url', default = "")
	#if repo:
	#    lab['repo_url'] = repo

        #sources = self.get_body_argument('sources_url', default = "")
        #if sources:
        #    lab['sources_available'] = sources

        #hosted = self.get_body_argument('hosted_url', default = "")
	#if hosted:
	#    lab['hosted_url'] = hosted

        #l_deployed = self.get_body_argument('lab_deployed', default = "")
        #if l_deployed:
        #    lab['lab_deployed'] = l_deployed

	#num_of_exp = self.get_body_argument('number_of_experiment', default = "")
	#if num_of_exp:
	#    lab['number_of_experiments'] = num_of_exp

        #cont = self.get_body_argument('content', default = "")
	#if cont:
	#    lab['content'] = cont

        #sim = self.get_body_argument('simulation', default = "")
	#if sim:
	#    lab['simulation'] = sim

        #web_2_comp = self.get_body_argument('web_2_compliance', default = "")
	#if web_2_comp:
        #    lab['web_2_compliance'] = web_2_comp

        #type_of_l = self.get_body_argument('type_of_lab', default = "")
        #if type_of_l:
        #    lab['type_of_lab'] = type_of_l

        #auto = self.get_body_argument('autohostable', default = "")
	#if auto:
	#    lab['autohostable'] = auto

        #rem = self.get_body_argument('remarks', default = "")
	#if rem:
	#    lab['remarks'] = rem

        #int_level = self.get_body_argument('integration_level', default = "")
	#if int_level:
	#    lab['integration_level'] = int_level

        #stat = self.get_body_argument('status', default = "")
	#if stat:
        #    lab['status'] = stat

	lab.save()
        self.finish({'updated_lab': lab.to_client()})

class LabIdHandler(tornado.web.RequestHandler):
    def get(self, unique_id):
        coll = Lab._get_collection()
        sub_coll = coll.find_one({"_id":ObjectId(unique_id)})
        if sub_coll:
            sub_coll["_id"] = str(sub_coll["_id"])
            self.write(sub_coll)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})
            
class DisciplineHandler(tornado.web.RequestHandler):
    def get(self, disciplinename):
        sub_coll = Lab.objects(discipline_name = disciplinename).to_json()
        if sub_coll:
            self.write(sub_coll)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})


def make_app():
    return tornado.web.Application([
        tornado.web.url(r'/labs', LabHandler),
	tornado.web.url(r'/labs/([0-9a-z]*)/([0-9a-z_]*)', LabHandler),
        tornado.web.url(r'/labs/([0-9a-z]*)', LabIdHandler),
	tornado.web.url(r'/labs/disciplines/([a-z]*)', DisciplineHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

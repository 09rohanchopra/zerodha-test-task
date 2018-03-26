import os
import cherrypy
import redis
from jinja2 import Environment, FileSystemLoader
import operator


env = Environment(loader=FileSystemLoader('media'))

class HomePage:

	@cherrypy.expose
	def index(self, search=""):
		tmpl = env.get_template('index.html')


		self.loosers = []
		for key in r.scan_iter("loose:*"):
			code = r.get(key)
			self.loosers.append(r.hgetall(code).copy())
			
		self.loosers.sort(key=operator.itemgetter('PERCENTAGE'))


		self.gainers = []
		for key in r.scan_iter("gain:*"):
			code = r.get(key)
			self.gainers.append(r.hgetall(code).copy())

		self.gainers.sort(key=operator.itemgetter('PERCENTAGE'), reverse = True)


		self.searchItems = []
		if search != "":
			search = search.upper()
			for key in r.scan_iter("equity:"+search+"*"):
				code = r.get(key)
				self.searchItems.append(r.hgetall(code).copy())


		
		return tmpl.render(loosers = self.loosers, gainers = self.gainers, search = self.searchItems) + search





root = HomePage()



tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')
r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

if __name__ == '__main__':

	cherrypy.quickstart(root, config=tutconf)
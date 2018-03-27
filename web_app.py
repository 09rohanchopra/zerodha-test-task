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


		self.last_updated = r.get("latest")
		return tmpl.render(loosers = self.loosers, gainers = self.gainers, search = self.searchItems, last_updated = self.last_updated)





root = HomePage()


cherrypy.config.update({'server.socket_host': '0.0.0.0',})
cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
cherrypy.config.update({
            '/favicon.ico':
            {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': 'favicon.ico'
            }
        })


r = redis.from_url(os.environ.get("REDIS_URL"), charset="utf-8", decode_responses=True)

if __name__ == '__main__':

	cherrypy.quickstart(root)
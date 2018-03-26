import os
import cherrypy
import redis


class HomePage:

	@cherrypy.expose
	def index(self):
		return '''
			<p>Hi, this is the home page! Check out the other
			fun stuff on this site:</p>
			<form method="post" action="/search/">
			  <input type="text" name="search" />
			  <button type="submit">Search</button>
			</form>
			<ul>
				<li><a href="/gain/">Top 10 Gainers</a></li>
				<li><a href="/loose/">Top 10 Loosers</a></li>
			</ul>'''


class GainPage:

	@cherrypy.expose
	def index(self):
		page_start = '''
			<p>"Top 10 gainers: "</p>
			<ul>
			'''
		page_end = '''
		</ul>
			<p>[<a href="../">Return</a>]</p>'''
		page_mid=''

		self.getGainers()
		#for gainer in getGainers:
		#	page_mid = page_mid + '''
		#                <li>Top 10 Gainers</li>'''

		return page_start + page_mid + page_end


	def getGainers(self):
		keys = r.get('*')
		
		print(keys)
		print()



class LoosePage:

	@cherrypy.expose
	def index(self):
		return '''
			<p>"Top 10 loosers: "</p>
			<p>[<a href="../">Return</a>]</p>'''

class SearchPage:

	@cherrypy.expose()
	def index(self, search=""):
		search = search.upper()
		

		return '''%s''' % (search)




# Of course we can also mount request handler objects right here!
root = HomePage()
root.gain = GainPage()
root.loose = LoosePage()
root.search = SearchPage()

# Remember, we don't need to mount ExtraLinksPage here, because
# LinksPage does that itself on initialization. In fact, there is
# no reason why you shouldn't let your root object take care of
# creating all contained request handler objects.


tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')
r = redis.Redis(host='localhost', port=6379, db=0)

if __name__ == '__main__':
	# CherryPy always starts with app.root when trying to map request URIs
	# to objects, so we need to mount a request handler root. A request
	# to '/' will be mapped to HelloWorld().index().

	cherrypy.quickstart(root, config=tutconf)
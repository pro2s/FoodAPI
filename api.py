import webapp2

import ReSTify

class LandingPage(webapp2.RequestHandler):
	""" Landing Page """

	def get(self):
		self.response.write("Dummy Food API")

application = webapp2.WSGIApplication(
    [
        ('/api/.*', ReSTify.ReST),
        ('/',LandingPage),
        ],
    debug=True)
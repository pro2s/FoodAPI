from google.appengine.ext import ndb

import webapp2
import datetime 
import ReSTify


class LandingPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Dummy Food API")

        

        
class MondayGenerator(webapp2.RequestHandler):
    def get(self):
        day = datetime.date.today() + datetime.timedelta(days = 1)
        day_of_week = day.weekday()

        to_beginning_of_week = datetime.timedelta(days=day_of_week)
        monday = day - to_beginning_of_week
        
        for num in range(0,8):
            ud = ReSTify.model.UserDay()
            ud.date = monday + datetime.timedelta(days = num)
            ud.userid = -1
            ud.selectid = -1
            ud.put()
            
        self.response.write("OK")    

application = webapp2.WSGIApplication(
    [
        ('/api/.*', ReSTify.ReST),
        ('/',LandingPage),
        ('/monday',MondayGenerator),
        ],
    debug=True)
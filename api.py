# -*- encoding: utf8 -*- 
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

from HTMLParser import HTMLParser

import webapp2
import datetime 
import ReSTify
import re

def clone_entity(e, **extra_args):
  _class = e.__class__
  props = dict((v._code_name, v.__get__(e, _class)) for v in _class._properties.itervalues() if type(v) is not ndb.ComputedProperty)
  props.update(extra_args)
  return _class(**props)
  
class LandingPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Dummy Food API")

class MenuParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []
        self.items = []
        self.day = 0
        self.mondaymenu = []
        day = datetime.date.today()
        day_of_week = day.weekday()
        to_beginning_of_week = datetime.timedelta(days=day_of_week)
        self.monday = day - to_beginning_of_week + datetime.timedelta(days=7)
        
    def handle_starttag(self, tag, attrs):
        
        if tag not in ('ul', 'li'):
            return
        
        if self.recording:
            self.recording += 1
            return
            
        for name, value in attrs:
            if name == 'id' and value == 'issues':
                break
        else:
            return
        self.recording = 1

    def handle_endtag(self, tag):
        if self.recording and tag == 'ul':
            self.recording -= 1
        if self.recording and tag == 'li':
            self.recording -= 1
            if self.day < 5:
                date = (self.monday + datetime.timedelta(days=self.day)).strftime("%Y-%m-%d")
                # TODO: get date from template type = 10 
                menu = ReSTify.model.Menu()    
                menu.name = u"Полный обед"
                menu.items = self.items
                menu.price = 35000
                menu.onDate = date
                menu.put()
                if self.day == 0:
                    self.mondaymenu.append(menu)
                
                self.items.pop(1)
                # TODO: get date from template type = 11 
                menu = ReSTify.model.Menu()    
                menu.name = u"Без первого"
                menu.items = self.items
                menu.price = 30000
                menu.onDate = date
                menu.put()
                if self.day == 0:
                    self.mondaymenu.append(menu)
                
                self.day += 1                
                self.items = []
            

    def handle_data(self, data):
        if self.recording:
            str = unicode(data, 'utf8')
            items =  re.match(u'(.*?),(.*?)гр', str)
            if items is not None:
                item = ReSTify.model.Item()
                item.name = items.group(1)
                item.weight = items.group(2)
                self.items.append(item)

class MenuGenerator(webapp2.RequestHandler):
    def get(self):
        url = "http://chudo-pechka.by/"
        menu = urlfetch.fetch(url)
        p = MenuParser()
        p.feed(menu.content)
        # TODO: replace userday select for types 8 on new added menu (p.mondaymenu)
        self.response.write("OK")    
 
application = webapp2.WSGIApplication(
    [
        ('/api/.*', ReSTify.ReST),
        ('/',LandingPage),
        ('/getmenu',MenuGenerator),
        ],
    debug=True)
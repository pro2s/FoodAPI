# Define your database model over here
import datetime
import logging

from google.appengine.api import users
from google.appengine.ext import ndb


class JsonIntegerProperty(ndb.IntegerProperty):
  def _validate(self, value):
    pass

  def _to_base_type(self, value):
    return int(value) 

  def _from_base_type(self, value):
    return value  

class JsonDateProperty(ndb.DateProperty):
    def _set_value(self, entity, value):
        fmt ='%Y-%m-%d'
        try:
            value = datetime.datetime.strptime(value, fmt)
        except ValueError, v:
            ulr = len(v.args[0].partition('unconverted data remains: ')[2])
            if ulr:
                value = datetime.datetime.strptime(value[:-ulr], fmt)
            else:
                value = None
        ndb.DateProperty._set_value(self, entity, value)

    
class Item(ndb.Model):
    name = ndb.StringProperty()
    parts = ndb.StringProperty()
    weight = ndb.StringProperty()

class Menu(ndb.Model):    
    name = ndb.StringProperty()
    items = ndb.StructuredProperty(Item, repeated=True) 
    price = JsonIntegerProperty(default = 0)
    onDate = JsonDateProperty()
    type = JsonIntegerProperty(default = 0)
    
    @classmethod
    def GetQuery(self, request):
        
        day = datetime.date.today()
        to_beginning_of_week = datetime.timedelta(days = day.weekday())
        monday = day - to_beginning_of_week
        
        qry = self.query(Menu.onDate >= monday, Menu.type == 0)
        
        system = request.get("system","")
        if (system == "none"):
            qry = self.query(Menu.type == -1)
        elif (system == "all"):
            qry = self.query(Menu.type !=  0)
        
        return qry
    
class User(ndb.Model):    
    name = ndb.StringProperty()
    bill = ndb.IntegerProperty()

class UserDay(ndb.Model):   
    userid = ndb.IntegerProperty() 
    date = ndb.DateProperty(auto_now_add=True)
    selectid = ndb.IntegerProperty() 
    
'''
public class UserDay
   {
       public int Id { get; set; }
       public int UserId { get; set; }
       public DateTime Date { get; set; }
       public Menu select { get; set; }
   }
'''
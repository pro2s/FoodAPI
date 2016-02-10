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
            if ulr and value is not None:
                value = datetime.datetime.strptime(value[:-ulr], fmt)
            else:
                value = None
        except TypeError:
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
        elif (system == "global"):
            qry = self.query(Menu.type >  0)
        
        return qry
    
class User(ndb.Model):    
    name = ndb.StringProperty()
    bill = ndb.IntegerProperty()
    email = ndb.StringProperty()
    roles = ndb.StringProperty()
    userName = ndb.StringProperty()
    
    
class Payment(ndb.Model):    
    userid = ndb.IntegerProperty() 
    date = JsonDateProperty(auto_now_add = True)
    sum = ndb.IntegerProperty()

    def before_put(self):
        pass

    def after_put(self):
        user = User.get_by_id(self.userid)
        user.bill = user.bill + self.sum
        user.put()
        

    def put(self, **kwargs):
        self.before_put()
        result = super(Payment, self).put(**kwargs)
        self.after_put()
        return result

    def save(self, **kwargs):
        self.before_put()
        result = super(Payment, self).save(**kwargs)
        self.after_put()
        return result
        
class UserDay(ndb.Model):   
    userid = ndb.IntegerProperty() 
    date = JsonDateProperty()
    selectid = ndb.IntegerProperty() 
    confirm = ndb.BooleanProperty(default = False)
    
    @classmethod
    def GetQuery(self, request):
        qry = self.query()
        userid = int(request.get("userid","-1"))
        if ( userid > 0 ):
            qry = self.query(UserDay.userid == userid)
        return qry
        
    def before_put(self):
        if self.key is not None:
            userday = UserDay.get_by_id(self.key.id())
            
            if (userday.confirm and userday.selectid != self.selectid):
                self.selectid = userday.selectid
                return
            
            if (userday.confirm and not self.confirm):
                user = User.get_by_id(self.userid)
                menu = Menu.get_by_id(userday.selectid)
                user.bill = user.bill + menu.price
                user.put()
                
            if (not userday.confirm and self.confirm):
                user = User.get_by_id(self.userid)
                menu = Menu.get_by_id(self.selectid)
                user.bill = user.bill - menu.price
                user.put()

    def after_put(self):
        pass
        
    def put(self, **kwargs):
        self.before_put()
        result = super(UserDay, self).put(**kwargs)
        self.after_put()
        return result

    def save(self, **kwargs):
        self.before_put()
        result = super(UserDay, self).save(**kwargs)
        self.after_put()
        return result

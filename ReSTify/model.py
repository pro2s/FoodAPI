# Define your database model over here

from google.appengine.api import users
from google.appengine.ext import ndb

class HashStore(ndb.Model):
    """Sample Model
    Models an individual HashStore entry with hastag, tile, and date.
    """
    author = ndb.UserProperty()
    title = ndb.StringProperty(indexed=False)
    hashtag = ndb.StringProperty(indexed=True, default="")
    viewDate = ndb.DateTimeProperty(auto_now_add=True)

class Item(ndb.Model):
    name = ndb.StringProperty()
    parts = ndb.StringProperty()
    weight = ndb.StringProperty()

class Menu(ndb.Model):    
    name = ndb.StringProperty()
    items = ndb.StructuredProperty(Item, repeated=True) 
    price = ndb.StringProperty()
    onDate = ndb.StringProperty()
    
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
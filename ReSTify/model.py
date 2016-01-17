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
    Id = ndb.IntegerProperty()
    Name = ndb.StringProperty(indexed=False)
    Parts = ndb.StringProperty(indexed=False)
    Weigth = ndb.StringProperty(indexed=False)

class Menu(ndb.Model):    
    Id = ndb.IntegerProperty()
    Name = ndb.StringProperty(indexed=False)
    Items = ndb.StructuredProperty(Item, repeated=True)
    Price = ndb.IntegerProperty()
    OnDate = ndb.DateTimeProperty(auto_now_add=True)
    

'''
public class Item
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Parts { get; set; }
        public string Weight { get; set; }
    }

public class Menu
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public virtual List<Item> Items { get; set; }
        public int Price { get; set; }
        public DateTime? OnDate { get; set; }
    }
public class UserDay
   {
       public int Id { get; set; }
       public int UserId { get; set; }
       public DateTime Date { get; set; }
       public Menu select { get; set; }
   }
public class FoodUser
   {
       public int Id { get; set; }
       public string Name { get; set; }
       public int Bill { get; set; }
   }
'''
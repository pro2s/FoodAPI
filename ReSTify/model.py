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

    
class MenuItemsProperty(ndb.IntegerProperty):
    def _validate(self, value):
        print "_validate"
        pass
        #if not isinstance(value, (int, long)):
        #raise TypeError('expected an integer, got %s' % repr(value))

    def _to_base_type(self, value):
        print "to"
        # return count of items
        pass

    def _from_base_type(self, value):
        print "from"
        # return items
        dataList=[]
        qry = User.query()
        if qry:
            for temp in qry:
                dataObject=temp.to_dict()
                dataObject["id"] = temp.key.id()
                dataList.append(dataObject)
        return dataList
        
class Menu(ndb.Model):    
    name = ndb.StringProperty()
    #items = ndb.StructuredProperty(Item, repeated=True) 
    items = MenuItemsProperty(default = 0)
    price = ndb.StringProperty()
    onDate = ndb.StringProperty()
    type = ndb.IntegerProperty(default = 0)
    
    
    @classmethod
    def GetQuery(self, request):
        print "GetQuery"
        type = request.get("type",0)
        print type
        return self.filter("type>=", type).query()
    
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
from google.appengine.ext import ndb

class Sporocilo(ndb.Model):
    vnos = ndb.StringProperty()
    datum = ndb.DateTimeProperty(auto_now_add=True)
    poslal= ndb.StringProperty()
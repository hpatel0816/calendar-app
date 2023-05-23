import pymongo
from security.secrets import databaseURI

#Setup for monogo database
client = pymongo.MongoClient(databaseURI)
db = client.get_database("flask-app-db")

#Creating the collections
users = pymongo.collection.Collection(db, 'users')
groups = pymongo.collection.Collection(db, 'groups')
events = pymongo.collection.Collection(db, 'events')
    
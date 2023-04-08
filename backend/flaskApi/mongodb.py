from flask_pymongo import pymongo
from security.secrets import databaseURI

#Setup for monogo database
client = pymongo.MongoClient(databaseURI)
db = client.get_database("flask-app-db")
#Creating the collections
users = pymongo.collection.Collection(db, 'users')
#from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from security.secrets import databaseURI

#Setup for monogo database
# client = pymongo.MongoClient(databaseURI)
# db = client.get_database("flask-app-db")
# #Creating the collections
# #users = pymongo.collection.Collection(db, 'users')
# users = db.get_collection('users')

client = MongoClient(databaseURI)
db = client.flaskApp
print(db)


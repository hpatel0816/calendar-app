#from flask_pymongo import PyMongo
# from pymongo.mongo_client import MongoClient
from security.secrets import databaseURI
from flask import current_app, session, g
from gridfs import Database
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
import logging
from pymongo.errors import DuplicateKeyError, OperationFailure
from typing import TypedDict
from pymongo.collection import Collection
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
import pymongo


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = MongoClient(current_app.config["MONGO_URI"])
        #db = g._database = PyMongo(current_app).db

    return db

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)
print(db)

def getDb():
    return db["flaskApp"]

def usersColl():
    collection: Collection = getDb()["users"]
    return collection


def insertUser(user):
    Collection = usersColl()

    try:
        Collection.insert_one(document=user)
    except pymongo.errors.DuplicateKeyError as e:
        print(e)

def getUser(field):

    Collection = usersColl()

    return Collection.find_one({f"field": field})
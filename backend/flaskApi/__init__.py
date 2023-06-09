from flask import Flask, request
from security.secrets import secretKey, databaseURI
from .mongodb import db

#Initializing the app
app = Flask(__name__)
app.config["SECRET_KEY"] = secretKey
app.config["MONGO_URI"] = databaseURI

# Import routes at the end to avoid circular imports
from flaskApi import routes

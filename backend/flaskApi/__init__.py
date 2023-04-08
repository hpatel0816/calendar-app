from flask import Flask, request
from security.secrets import secretKey
from .mongodb import db

#Initializing the app
app = Flask(__name__)
app.config["SECRET_KEY"] = secretKey

# Import routes at the end to avoid circular imports
from flaskApi import routes

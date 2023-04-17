from flaskApi import app
from .mongodb import db
from flask import request
from security.auth import token_required, generateToken
from helpers.httpResp import success, error
import jsonify


@app.route("/")
def home():
    return "Hello World!"


@token_required
@app.route("/db")
def database():
    return "This is the db page!"


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json["data"]
    userExists = db.getUser({"email": data["email"]})
    if userExists:
        error_resp = error(409, "An account with that email already exists.")
        return jsonify(error_resp)
    else:
        user = {
            "firstname": data["firstName"],
            "lastname": data["lastName"],
            "email": data["email"],
            "password": data["password"]
        }
        try:
            #userId = db.users.insert_one(user)
            userId = db.insertUser(user)
            return jsonify(success(201, "Account created successfully!"))
        except:
            error_resp = error(500, "Unable to create account.")
            return jsonify(error_resp)


@app.route("/add-user", methods=["POST"])
def addUser():
    data = request.json["data"]
    user = {
            "firstname": data["firstName"],
            "lastname": data["lastName"],
            "email": data["email"],
            "password": data["password"]
    }

    try:
        result = db.insertUser(user)
        #return f"New user added successfully! (ID:{result.inserted_id})"
        return jsonify(success(201, f"New user added successfully! (ID:{result.inserted_id}"))
    except Exception as e:
        print("Error inserting document:", e)
        return "Error - unable to add user."

from flaskApi import app
from .mongodb import db, users, events, groups
from flask import request
from security.auth import token_required, generateToken
from security.secrets import databaseURI
import bcrypt
from bson.objectid import ObjectId


@app.route("/")
def home():
    return "Hello World!"


@app.route("/db", methods=["GET"])
@token_required
def database(currUser):
    return "This is the db page!"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.json["data"]
        userExists = users.find_one({"email": data["email"]})
        if userExists:
            return {"data": "An account with that email already exists."}, 409
        else:
            hashedPass = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
            user = {
                "firstname": data["firstName"],
                "lastname": data["lastName"],
                "email": data["email"],
                "password": hashedPass,
            }
            try:
                users.insert_one(user)
                return {"data": "Account created successfully!"}, 201
            except:
                return {"data": "Unable to create account."}, 500
    else:
        return "Sign-up page."


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = request.json["data"]

        try:
            user = users.find_one({"email": data["email"]})
        except:
            return {"data": "Unable to find user."}, 500

        user = users.find_one({"email": data["email"]})
        if user is None:
            return {"data": "Sorry, that account doesn't exist."}, 401

        passwordMatch = bcrypt.checkpw(data["password"].encode('utf-8'), user["password"])
        if passwordMatch:
            resp = generateToken(user["_id"])
            if resp[0] == "Success":
                return {"token": resp[1], "data": "Login successful!"}, 200
            else:
                return {"data": resp}, 500
        else:
            return {"data": "Password is incorrect. Try again."}, 401

    else:
        return "Login page."


# @app.route("/home", methods=["GET", "POST"])
# @token_required
# def home(currUser):



@app.route("/createEvent", methods=["GET", "POST"])
@token_required
def createEvent(currUser):
    if request.method == "POST":
        data = request.json["data"]
        event = {
            "title": data["title"],
            "creator": f"{currUser['firstname']} {currUser['lastname']}",
            "group": data["group"],
            "date": data["date"],
            "startTime": data["start"],
            "endTime": data["end"],
            "location": data["location"],
            "description": data["description"],
            "category": data["category"],
            "optedIn": [f"{currUser['_id']}"]
        }

        try:
            events.insert_one(event)
            return {"data": "Event created successfully."}, 200
        except:
            return {"data": "Unable to create account."}, 500


# @app.route("/group/<grpName>", methods=["PUT"])
# @token_required
# def groupPage(currUser):
#     if request.method == "PUT":
#         data = request.json["data"]

#         events.update_one(
#             {"_id": ObjectId(event_id)},
#             {"$push": {"optIn": name}}
        # )


@app.route("/<eventId>/optIn", methods=["PUT"])
@token_required
def optIn(currUser, eventId):
    if request.method == "PUT":
        try:
            event = events.find_one({"_id": ObjectId(eventId)})
            if str(currUser["_id"]) in event["optedIn"]:
                return {"data": "You are already opted in."}, 200
        except:
            return {"data": "The event doesn't exist."}, 403

        try:
            events.update_one(
                {"_id": ObjectId(eventId)},
                {"$push": {"optedIn": str(currUser["_id"])}}
            )
            return {"data": "Added to event successfully."}, 200
        except Exception as e:
            print(e)
            return {"data": "Unable to opt in. Try again."}, 500


@app.route("/<eventId>/optOut", methods=["PUT"])
@token_required
def optIn(currUser, eventId):
    if request.method == "PUT":
        try:
            event = events.find_one({"_id": ObjectId(eventId)})
            if str(currUser["_id"]) not in event["optedIn"]:
                return {"data": "You are already opted out."}, 200
        except:
            return {"data": "The event doesn't exist."}, 403

        try:
            events.update_one(
                {"_id": ObjectId(eventId)},
                {"$pull": {"optedIn": str(currUser["_id"])}}
            )
            return {"data": "Removed from event successfully."}, 200
        except Exception as e:
            print(e)
            return {"data": "Unable to opt out. Try again."}, 500
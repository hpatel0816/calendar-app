from flask import request, abort, current_app 
from flaskApi import app, db
from functools import wraps
from helpers.httpResp import success, error
import jwt
import jsonify
import datetime

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        #Get the token from authorization field
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split("")[1]
        #Exit if token not found
        if not token:
            error_resp = error(401, "Authorization token is missing.")
            return jsonify(error_resp)
        else:
            resp = validate_token(token)
            #Token validated
            if resp["code"] == 200:
                currUser = db.users.find_one({"_id": resp["message"]})
                if currUser is not None:
                    #User access granted
                    return f(currUser,  *args, **kwargs)
                else:
                    error_resp = error(401, "You do not have permission to access this resource.")
                    return jsonify(error_resp)
            else:
                return jsonify(resp)
        
    return decorated


def generateToken(userId):
    """
    Generates a JWT token for authentication

    iss: Issuer of token (calender-app)
    sub: Subject (set to user ID)
    iat: Issued at time
    exp: Expiry of token (90 mins)
    """
    try:
        payload = {
            #"iss": https://calender-app.com
            "sub": userId,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=90)
        }
        return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    except Exception as e:
        error_rep = error(500, "Unable to generate JWT token for user.")
        return jsonify(error_rep)


def validate_token(token):
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithm="HS256")
        return success(200, payload["sub"])
    except jwt.exceptions.ExpiredSignatureError:
        return error(403, "Token has expired.")
    except jwt.exceptions.InvalidTokenError:
        return error(401, "Invalid token.")
    except Exception:
        return error(500, "Cannot validate provided token.")
from flaskApi import app, db

@app.route("/")
def home():
    return "Hello World!"


@app.route("/db")
def database():
    return "This is the db page!"


@app.route("/add-user", methods=["POST"])
def addUser():
    user = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "johndoe@email.com",
        "password": "password"
    }

    try:
        result = db.users.insert_one(user)
        return f"New user added successfully! (ID:{result.inserted_id})"
    except:
        return "Error - unable to add user."
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from flask_session import Session
from functools import wraps

# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///journal.db")

# Main Page the user see both login and the register
@app.route("/")
def index():
    "Prompt the user to login or Register"
    return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    "The home page where users do the journalling"

    data = []

    if request.method == "POST":

        input_data = request.form.get("user-input")

        db.execute("INSERT INTO data (user_id, info) VALUES(?, ?)", session["user_id"], input_data)

        return redirect("/home")

    else:

        rows = db.execute("SELECT * FROM data WHERE user_id = ?", session["user_id"])

        i = 1
        for row in rows:

            dictionary = {
            "no": 0,
            "date": "",
            "journal": ""
        }

            dictionary["no"] = i
            dictionary["date"] = row["date"]
            dictionary["journal"] = row["info"]

            i += 1

            data.append(dictionary)

        return render_template("home.html", DATA=data)

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # if the method is posst
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Checking if the inputs are empty
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("error.html", ERROR="Invalid Username Or Password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return render_template("error.html", ERROR="Invalid Username or Password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/home")
    else:
        # if the request is get
        return render_template("login.html")


# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    # If the request is post
    if request.method == "POST":

        # Checking if the inputs are empty
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return render_template("error.html", ERROR="Invalid Username Or Password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        # check if there is a username and is it in the database
        if not request.form.get("username") or not len(rows) != 1:
            return render_template("error.html", ERROR="Username Already Exist")

        # hash the password
        hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        if password == confirm:
            # Inserting data to the database
            db.execute("INSERT INTO users (username, password) VALUES(?, ?)", username, hashed)
        else:
            # If the passwords are different redirect to the error page
            return render_template("error.html", ERROR="Different Password")

        return redirect("/login")

    else:
        # If the method is get
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

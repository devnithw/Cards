from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from flask_session import Session 
import sqlite3
from helpers import login_required

# Configure the application
app = Flask(__name__)

#Ensure templates are reloaded automatically
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Cofigure session to use the file system
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure sqlite3 library
connection = sqlite3.connect('tasks.db')
db = connection.cursor()

# INDEX ROUTE---------------------------------------------------------------------------------------
@app.route('/')
@login_required
def index():
    return 'Hello, World!'


# LOGIN ROUTE --------------------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username or password")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# LOGOUT ROUTE ---------------------------------------------------------------------------------------------------------------
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



# REGISTER ROUTE -------------------------------------------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect("/register")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # check if the username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 0:
            return apology("username already exists", 400)

        # generate password hash
        hashed = generate_password_hash(request.form.get("password"))

        # Query database to insert row
        userID = db.execute("INSERT INTO users (username,hash) VALUES(?,?)", request.form.get("username"), hashed)

        # Remember which user has logged in
        session["user_id"] = userID

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
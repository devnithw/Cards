from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from flask_session import Session 
import sqlite3
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Configure the application
app = Flask(__name__)

#Ensure templates are reloaded automatically
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Cofigure session to use the file system
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# INDEX ROUTE---------------------------------------------------------------------------------------
@app.route('/')
@login_required
def index():

    return 'Hello World'


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

        username = request.form.get("username")
        

        # Configure sqlite3 library
        connection = sqlite3.connect('tasks.db')
        db = connection.cursor()

        # Query database for username
        db.execute("SELECT id,hash FROM users WHERE username = ?", username)
        rows = db.fetchall()

        connection.close()

        # Ensure username exists and password is correct
        if len(rows) == 1 and check_password_hash(rows[0][1], request.form.get("password")):

            # Remember which user has logged in
            session["user_id"] = rows[0][0]

            # Redirect user to home page
            flash("logged in")
            return redirect("/")
        else:      
            flash("Invalid username or password")
            return redirect("/login")
        
        

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
        
        # Ensure name is submitted
        if not request.form.get("name"):
            flash("Must provide name")
            return redirect("/register")


        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect("/register")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            flash("Must confirm password")
            return redirect("/register")

        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match")
            return redirect("/register")

        # Configure sqlite3 library
        connection = sqlite3.connect('tasks.db')
        db = connection.cursor()

        # check if the username already exists
        db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        rows = db.fetchall()

        if len(rows) != 0:
            flash("Username is taken")
            return redirect("/register")

        # generate password hash
        hashed = generate_password_hash(request.form.get("password"))

        # Query database to insert row
        username = request.form.get("username")
        name = request.form.get("username")

        db.execute("INSERT INTO users (name,username,hash) VALUES(?,?,?)", (name, username, hashed))
        db.execute("SELECT id FROM users WHERE username = ?", username)
        userID = db.fetchone()

        # Close the database
        connection.commit()
        connection.close()

        # Remember which user has logged in
        session["user_id"] = userID[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
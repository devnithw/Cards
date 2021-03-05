# Taskly - CS50 Final Project by Devnith Wijesinghe
# A simple task and schedule managing web application created using Python with Flask, SQLite and Bootstrap 

# ----------------------------------------------------------------------------------------------------------------------------

from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from flask_session import Session 
import sqlite3
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Configure the application
app = Flask(__name__)

#Ensure templates are reloaded automatically
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Cofigure session to use the file system
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# INDEX ROUTE----------------------------------------------------------------------------------------------------------------
@app.route('/')
@login_required
def index():
    return redirect("/dashboard")


# LOGIN ROUTE ---------------------------------------------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Forget any user_id
        session.clear()

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
            session["user_id"] = int(rows[0][0])

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

    # Forget any user_id
    session.clear()

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
        name = request.form.get("name")

        db.execute("INSERT INTO users (name,username,hash) VALUES(?,?,?)", (name, username, hashed))
        db.execute("SELECT id FROM users WHERE username = ?", username)
        userID = db.fetchone()

        # Close the database
        connection.commit()
        connection.close()

        # Remember which user has logged in
        session["user_id"] = int(userID[0])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


# DASHBOARD ROUTE
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():

    if request.method == "GET":

        # Start a connection to the database
        connection = sqlite3.connect('tasks.db')
        db = connection.cursor()
        userID = session["user_id"]

        # Query the database for name and points
        db.execute("SELECT name,points FROM users WHERE id = (?)", (userID,))
        row = db.fetchone()

        # Set name and point variables
        name = row[0]
        points = row[1]

        #Query the database for stasks and crate a list of data rows
        db.execute("SELECT title,date,description FROM stasks WHERE user_id = (?)", (userID,))
        stasks = db.fetchall()

        #Query the database for books and crate a list of data rows
        db.execute("SELECT id,title,totalPages,currentPage FROM books WHERE user_id = (?)", (userID,))
        books = db.fetchall()

        #Query the database for mtasks and crate a list of data rows
        db.execute("SELECT id,title,date FROM mtasks WHERE user_id = (?)", (1,))
        items = db.fetchall()
        mtasks= list()

        # Iterate over each mtask in mtasks list 
        for item in items:
            
            # The mtask item is a tuple // Convert it to a list 
            item = list(item)
            
            # Query the database for the relavant subtasks
            db.execute("SELECT title FROM subtasks WHERE mtask_id = (?)", (item[0],))
            subtasks = db.fetchall()
            
            # Recreate a list containing the subtasks
            temp = list()
            for task in subtasks:
                temp.append(task[0])

            # Put the temporary list of subtasks in the bigger mtask list
            item.append(temp)
            mtasks.append(item)


        
        return render_template("dashboard.html", name=name, points=points, stasks=stasks, books=books, mtasks=mtasks)

    if request.method == "POST":

        # Start a connection to the database
        connection = sqlite3.connect('tasks.db')
        db = connection.cursor()
        userID = session["user_id"]

        # Deleting Stask from database
        if request.form.get("deleteStask"):
            title = request.form.get("deleteStask")

            # Delete the row from the database
            db.execute("DELETE FROM stasks WHERE title = (?)", (title,))

            # Close the database connection
            connection.commit()
            connection.close()

            flash("Task removed")
            print(title + "is deleted")

        # Updating currentPage of books
        if request.form.get("setPage"):
            bookID = request.form.get("setPage")

            if not request.form.get("currentPage"):
                flash("Please provide valid page number")
                return redirect("/dashboard")

            currentPage = int(request.form.get("currentPage"))

            if currentPage < 1 :
                flash("Choose a valid number of page")
                return redirect("/dashboard")                


            # Delete the row from the database
            db.execute("UPDATE books SET currentPage = (?) WHERE id = (?)", (currentPage,bookID))

            # Add score if user read the book completely
            db.execute("SELECT totalPages FROM books WHERE id = (?)", (bookID,))
            totalPages = db.fetchone()

            if currentPage == totalPages[0]:

                db.execute("SELECT points FROM users WHERE id = (?)", (userID,))
                points = db.fetchone()

                # Update points variable
                newpoints = points[0] + totalPages[0]

                # Update points column in database
                db.execute("UPDATE users SET points = (?) WHERE id = (?)", (newpoints, userID))
                flash("You have earned points!")

            # Close the database connection
            connection.commit()
            connection.close()

            print("updated")

        # Deleting book from database
        if request.form.get("deleteBook"):
            bookID = request.form.get("deleteBook")

            db.execute("DELETE FROM books WHERE id = (?)", (bookID,))

            # Close the database connection
            connection.commit()
            connection.close()

            print(bookID + "is deleted")
            flash("Book removed")

        # Deleting Mtask from database
        if request.form.get("deleteMtask"):
            mtask_id = request.form.get("deleteMtask")

            # Delete all related subtasks
            db.execute("DELETE FROM subtasks WHERE mtask_id = (?)", (mtask_id,))



            # Delete the row from the database
            db.execute("DELETE FROM mtasks WHERE id = (?)", (mtask_id,))

            # Close the database connection
            connection.commit()
            connection.close()

            flash("Big Task removed")
            print("Mtask is deleted")





        return redirect("/dashboard")
        



    



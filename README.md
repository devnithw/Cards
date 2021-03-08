# Cards
#### Video Demo:  https://www.youtube.com/watch?v=lPQKE0sFiUU
#### Description:
Cards is a customizable task management web application with a scoring system created using Python with Flask, SQL and Bootstrap. In this application the user can create a personal account for storing their data 
and manage, plan and schedule their daily tasks using customized features. It offers the user various forms of tasking methods such as QuickTasks, BigTasks and Books. When the user completes
tasks the application awards the user with points as entertainment. The information about the user's tasks are displayed as cards on their user dashboard.

### QuickTasks
The user can store their short tasks as QuickTasks which displays the due date and a small description of what the task will be about.

### BigTasks
For bigger tasks that can be divided into subtasks, the user can store them in a way that the user dashboard depicts the title of the bigger task and it's steps to be completed

### Books
The user can enter details about a book they are reading and update the current page to keep track of their readings. Book cards display the user's progress as a graph and awards the user points according to the number of pages the book has

### How to use
Before using the web application you will need an account. On the front page click on register and enter relevant details to continue.
Now you will be redirected to the user dashboard and you will be greeted by your name as well as display 5 initial points to start off with.
To add a task click on the "New" button on the top navigation bar. Choose a form of task that you will like to add and fill out the relevant details.
After you submit the form you will be redirected to the dashboard and your task will be shown there. 
When you complete a task click on "Complete" to delete the task and get points


### Under the hood
The web application uses the following list of programs and frameworks,
- Python as the backend of the application using the Flask framework
- SQLite3 as database management using the Python sqlite3 module 
- HTML and CSS on top of Bootstrap to create webpage templates
- Fonts Awesome icons for HTML
- Pacifica font from Google fonts

### Project files in detail
The guide to the project folder is as follows,
- **application.py** - This is the main python file with the core backend logic of the application. It includes the route definitions and utilizes some functions written in
helpers.py
- **helpers.py** - This file inlcudes some logical functions to be called abstractly in the main python file
- **tasks.db** - This is the SQL database file which includes five tables; users, stasks, mtasks, subtasks and books. The tables are related to each other using foreign keys
- **templates** - This folder includes a couple of HTML documents. The layout.html file is the basic template on which the other HTML templates are rendered with
- **requirements.txt** - This text file consists of all the python modules used in the project which were installed using pip

### Development
The web application was created in the following environment,
- A Python virtual environment with pip
- Visual Studio Code as the Integrated Development Environment
- Git as the version control software
- Google Chrome as the web browser for viewing web pages

### Obstacles faced during development
Beacuse this project was not developed using the CS50 IDE there were some issues that I ran into during building some elements. Even though CS50 offers SQL database handling Python functions in the CS50 library, I could not use it outside of the IDE. Therefore I had to use another Python module called _sqlite3_. I had to refer to it's documentation every so often and also search Google or Stackoverflow. Soon I was familiar with the new module and its functionality.

### Resources used in developing this application
- [Bootstrap official documentation](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
- [sqlite3 python module documentation](https://docs.python.org/3/library/sqlite3.html)
- Stackoverflow

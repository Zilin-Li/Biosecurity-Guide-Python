# contain all of our views
from app import app 
from flask import  render_template
from flask import request
from flask import redirect
from flask import url_for
import re
import mysql.connector
from mysql.connector import FieldType
from .. import connect  
from flask_hashing import Hashing
from flask import session
from datetime import date


# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
hashing = Hashing(app)  #create an instance of hashing


dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    # Establishing a database connection
    connection = mysql.connector.connect(
        user=connect.dbuser,
        password=connect.dbpass,
        host=connect.dbhost,
        database=connect.dbname,
        autocommit=True
    )
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("public/home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
     # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists using MySQL
        query = """
        SELECT 
            u.id, 
            u.username, 
            u.hashed_password, 
            u.salt, 
            u.role_id 
        FROM 
            User u
        WHERE username = %s;
            """ 
        cursor = getCursor()
        cursor.execute(query, (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            password = account[2]
            if hashing.check_value(password, user_password, salt=account[3]):
            # If account exists in accounts table 
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['roleid'] = account[4]
                # if account[4] == 1:
                #     return redirect( url_for('admin_dashboard'))                  
                # elif account[4] == 2:   
                #     return redirect( url_for('staff_dashboard'))
                # elif account[4] == 3:   
                return redirect( url_for('public_dashboard'))
                          
            else:
                 #password incorrect
                msg = 'Incorrect password!'             
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)   
    return render_template('public/login.html', msg=msg)

@app.route("/register", methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        query = """
        SELECT 
            u.username, 
            u.email
        FROM 
            User u
        WHERE username = %s;
            """ 
        cursor = getCursor()
        cursor.execute(query, (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            salt1='abcd'
            first_name = "test1"
            last_name = "OMG"
            phone = "123456"
            join_date =date.today()
            role_id = 3
            status = 1
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt=salt1)
            cursor.execute('INSERT INTO user VALUES (NULL,%s,%s, %s, %s, %s, %s,%s, %s, %s, %s)', (username, hashed, salt1, first_name, last_name, email, phone, join_date, role_id, status))
            connection.commit()
            msg = 'You have successfully registered!'
            return redirect( url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template("public/register.html")
  
    

@app.route("/dashboard")
def public_dashboard():
    # account='12345'
    print(session['id'])
    return render_template('public/public_dashboard.html')


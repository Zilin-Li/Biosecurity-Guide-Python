# contain all of our views
from app import app 
from flask import  render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
import re
from mysql.connector import FieldType
from .. import get_db_connection
from flask_hashing import Hashing
from flask import session
from datetime import datetime, date
import secrets
import random

app.secret_key = 'your secret key'
hashing = Hashing(app) 


@app.route("/admin/dashboard")
def admin_dashboard():
    
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    if roleid != 1:
        return redirect( url_for('home'))
    return render_template("admin/dashboard.html",isLogin=isLogin,username=username,roleid=roleid)

@app.route('/admin/user/add', methods=['GET', 'POST'])
def add_user():
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')   
    msg=''
    if isLogin:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'confirmPassword'in request.form:
            newusername = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirmPassword']
            email = request.form['email']
               # Check if account exists using MySQL
            query = """
            SELECT 
                u.username, 
                u.email
            FROM 
                User u
            WHERE username = %s
                OR u.email = %s;;
                """ 
            connection, cursor = get_db_connection()
            try:
                cursor.execute(query, (newusername,email,))
                account = cursor.fetchone()
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
            # If account exists show error and validation checks
            if account:
                if account[0]== newusername:
                    msg = 'Account already exists!'
                elif account[1] == email:
                    msg = 'Email already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'^[A-Za-z0-9]+$', username):
                msg = 'Username must contain only characters and numbers!'
            elif password !=confirm_password:
                msg = 'Password confirmation failed.!'
            elif not username or not password or not confirm_password or not email :
                msg = 'Please fill out the form!'
            else:
                #Automatic salt generation
                random_text = secrets.token_hex(16)
                # Set default user profile
                first_name = request.form.get('firstName')
                last_name = request.form.get('lastName')
                phone = request.form.get('phone')
                address = request.form.get('address')
                join_date =datetime.now()
                user_role_id = 3
                status = 1
                # Automatically generate a user id
                horticulturalist_id = generate_user_num('HORT')
                print(horticulturalist_id, '~~~~~~~~~')
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                hashed = hashing.hash_value(password, salt=random_text)
                connection, cursor = get_db_connection()
                try:
                    cursor.execute('INSERT INTO user VALUES (NULL,%s,%s, %s, %s, %s, %s,%s, %s, %s, %s)', (newusername, hashed, random_text, first_name, last_name, email, phone, join_date, user_role_id, status))
                    new_user_id = cursor.lastrowid
                    print(new_user_id, '!!!!!')
                    cursor.execute('''
                        INSERT INTO Horticulturalist (user_id, horticulturalist_id,address) 
                            VALUES (%s, %s,%s)
                        ''', (new_user_id, horticulturalist_id,address))
                    connection.commit()
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    cursor.close()
                    connection.close()
                msg = 'You have successfully registered!'
                # msg =horticulturalist_id
                # return redirect( url_for('login'))
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        return render_template("admin/userAdd.html",isLogin=isLogin,username=username,roleid=roleid, msg=msg)
    else:
        return redirect(url_for('login'))
def generate_user_num(roleName):
    # Gets the year, month, day, hour, second of the current time
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # Generate a 5-digit random number
    random_number = random.randint(10000, 99999)
    # Creat user id
    user_id = f"{roleName}{timestamp}{random_number}"
    return user_id

@app.route('/admin/user/edit', methods=['GET', 'POST'])
def edit_user():
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')   
    msg=''
    user_info = [1]
    
    return render_template("admin/userEdit.html",isLogin=isLogin,username=username,roleid=roleid, msg=msg,user_info=user_info)
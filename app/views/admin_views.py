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
                user u
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
                
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                hashed = hashing.hash_value(password, salt=random_text)
                connection, cursor = get_db_connection()
                try:
                    cursor.execute('INSERT INTO user VALUES (NULL,%s,%s, %s, %s, %s, %s,%s, %s, %s, %s)', (newusername, hashed, random_text, first_name, last_name, email, phone, join_date, user_role_id, status))
                    new_user_id = cursor.lastrowid
                   
                    cursor.execute('''
                        INSERT INTO horticulturalist (user_id, horticulturalist_id,address) 
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

@app.route('/admin/user/edit/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')   
    msg=''
    if isLogin:   
        query = """
        SELECT 
            u.id, 
            u.username, 
            u.first_name, 
            u.last_name,
            u.email,
            u.phone,
            DATE_FORMAT(u.join_date, '%Y-%m-%d') AS formatted_join_date, 
            u.status, 
            h.horticulturalist_id,
            h.address
        FROM 
            user u
        JOIN 
            horticulturalist h ON u.id = h.user_id
        WHERE u.id = %s;
            """
        connection, cursor = get_db_connection()
        try:
            cursor.execute(query, (user_id,))
            user_info = cursor.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
        return render_template('admin/userEdit.html',isLogin=isLogin,username=username,roleid=roleid,msg=msg,user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/admin/user/update/<int:user_id>', methods=['POST'])
def edit_user_submit(user_id): 
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')   
    msg=''
    if isLogin:
        first_name=request.form.get('firstName')
        last_name=request.form.get('lastName')     
        phone=request.form.get('phone')
        address=request.form.get('address')
        hortid=request.form.get('hortid')
        selected_status = request.form.get('status')
        status_value = 1 if selected_status == 'Active' else 0
        newPassword = request.form['newpassword']
        confirmPassword = request.form['confirmedPassword']
       
        connection, cursor = get_db_connection()      
        query = """
            SELECT 
                h.horticulturalist_id
            FROM 
                horticulturalist h
            WHERE horticulturalist_id = %s
            AND user_id != %s
                ;
                """ 
        try:
            cursor.execute(query, (hortid, user_id,))
            account = cursor.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

        if account:
            msg = 'Horticulturalist id already exists!'
            return redirect(url_for('edit_user',user_id = user_id,msg=msg))
        

        if newPassword and confirmPassword:
            if newPassword !=confirmPassword:

                msg = 'Password confirmation failed.!'
                return redirect(url_for('edit_user',user_id = user_id,msg=msg))
            else:
                #Automatic salt generation
                random_text = secrets.token_hex(16)
                
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                hashed = hashing.hash_value(newPassword, salt=random_text)
                
                update_user_query="""
                    UPDATE user
                    SET first_name = %s,
                        last_name = %s,
                        hashed_password=%s,
                        salt =%s,
                        phone = %s,
                        status = %s
                    WHERE id = %s;
                    """  
                update_Hoti_query="""
                        UPDATE horticulturalist
                        SET address = %s,
                        horticulturalist_id = %s
                        WHERE user_id = %s;
                    """ 
                connection, cursor = get_db_connection()
                try:
                    cursor.execute(update_user_query, (first_name,  last_name, hashed, random_text, phone,  status_value,user_id ))
                
                    cursor.execute(update_Hoti_query, (address, hortid, user_id))
                    connection.commit()
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    cursor.close()
                    connection.close()
                msg = 'You have successfully update!'
                # msg =horticulturalist_id
                # return redirect( url_for('login'))
        else:
            update_user_query="""
                UPDATE user
                SET first_name = %s,
                    last_name = %s,
                    
                    phone = %s,
                    status = %s
                WHERE id = %s;
                """  
            update_Hoti_query="""
                    UPDATE horticulturalist
                    SET address = %s,
                    horticulturalist_id = %s
                    WHERE user_id = %s;
                """ 
            connection, cursor = get_db_connection()
            try:
                cursor.execute(update_user_query, (first_name,  last_name, phone,  status_value,user_id ))
            
                cursor.execute(update_Hoti_query, (address, hortid, user_id))
                connection.commit()
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
            msg = 'You have successfully update!'
        return redirect(url_for('edit_user',user_id = user_id,msg=msg))
    
    else:
        return redirect(url_for('login'))
    
# Staff management
@app.route('/admin/staff')
def staff_management():
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    
    if not isLogin:
        return redirect(url_for('login'))
    else:
        if roleid != 1:
            return redirect(url_for('home'))
        else:
            staff_list = get_staff_info()
            return render_template('admin/staffMgt.html',isLogin=isLogin,username=username,roleid=roleid,staff_list=staff_list)

@app.route('/admin/staff/detail/<user_id>')
def staff_detail(user_id):  
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    
    if isLogin:
        if roleid != 1:
            return redirect(url_for('home'))
        else:
            staff_info = get_staff_info(f' WHERE u.id = {user_id}')
            return render_template('admin/staffDetail.html',isLogin=isLogin,username=username,roleid=roleid,staff_info=staff_info)
    else:
        return redirect(url_for('login')) 

@app.route('/admin/staff/edit/<int:user_id>', methods=['GET'])
def staff_edit(user_id):
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')   
    msg=''
    if isLogin:   
        staff_info = get_staff_info(f' WHERE u.id = {user_id}')
        position_list = get_position_list()
        department_list = get_department_list()
        return render_template('admin/staffEdit.html',isLogin=isLogin,username=username,roleid=roleid,msg=msg,staff_info=staff_info,position_list=position_list,department_list=department_list)
    else:
        return redirect(url_for('login'))

@app.route('/admin/staff/update/<int:user_id>', methods=['POST'])
def edit_staff_submit(user_id):
    isLogin=session.get('loggedin')
    username = session.get('username')
    roleid=session.get('roleid')
    if isLogin:
        first_name=request.form.get('firstName')
        last_name=request.form.get('lastName')     
        phone=request.form.get('phone')
        hire_date=request.form.get('hireDate')
        staffid=request.form.get('staffid')
        selected_status = request.form.get('status')
        status_value = 1 if selected_status == 'Active' else 0
        position_id=request.form.get('position')
        department_id=request.form.get('department')
        user_role_id = request.form.get('isAdmin')   
        newPassword = request.form['newpassword']
        confirmPassword = request.form['confirmedPassword']
        connection, cursor = get_db_connection()
        # check if staff id exists
        query = """
            SELECT 
                s.staff_id
            FROM 
                staff s
            WHERE staff_id = %s
            AND user_id != %s;
                """ 
        try:
            cursor.execute(query, (staffid, user_id,))
            account = cursor.fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()
        
        if account:
            flash('Staff id already exists!','error')
            return redirect(url_for('staff_edit',user_id = user_id))
        
        if newPassword and confirmPassword:
            if newPassword !=confirmPassword:
                flash('Password confirmation failed.!','error')
                
                return redirect(url_for('staff_edit',user_id = user_id))
            else:
                #Automatic salt generation
                random_text = secrets.token_hex(16)
                
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                hashed = hashing.hash_value(newPassword, salt=random_text)
                
                update_user_query="""
                    UPDATE user
                    SET first_name = %s,
                        last_name = %s,
                        hashed_password=%s,
                        salt =%s,
                        phone = %s,
                        status = %s,
                        role_id = %s
                    WHERE id = %s;
                    """  
                update_staff_query="""
                        UPDATE staff
                        SET position_id = %s,
                        department_id = %s,
                        hire_date = %s,
                        staff_id = %s
                        WHERE user_id = %s;
                    """ 
                connection, cursor = get_db_connection()
                try:
                    cursor.execute(update_user_query, (first_name,  last_name, hashed, random_text, phone,  status_value,user_role_id,user_id ))
                
                    cursor.execute(update_staff_query, (position_id, department_id, hire_date,staffid, user_id))
                    connection.commit()
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    cursor.close()
                    connection.close()
                flash('You have successfully update!','success')
        else:
            update_user_query="""
                UPDATE user
                SET first_name = %s,
                    last_name = %s,
                    phone = %s,
                    status = %s,
                    role_id = %s
                WHERE id = %s;
                """  
            update_staff_query="""
                        UPDATE staff
                        SET position_id = %s,
                        department_id = %s,
                        hire_date = %s,
                        staff_id = %s
                        WHERE user_id = %s;
                    """ 
            connection, cursor = get_db_connection()
            try:
                cursor.execute(update_user_query, (first_name,  last_name, phone,  status_value,user_role_id,user_id ))    
                cursor.execute(update_staff_query, (position_id, department_id, hire_date,staffid, user_id))
                connection.commit()
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
            flash('You have successfully update!','success')
        return redirect(url_for('staff_edit',user_id = user_id))
    return redirect(url_for('login'))

@app.route('/admin/staff/add', methods=['GET', 'POST'])
def add_staff():
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')  
    position_list = get_position_list()
    department_list = get_department_list()
    if isLogin:
        if request.method == 'POST' and  'newusername' in request.form and  'email' in request.form and 'newpassword' in request.form and 'confirmedPassword'in request.form and 'position' in request.form and 'department' in request.form and 'isAdmin' in request.form and 'status' in request.form:
            newusername = request.form['newusername']
            email = request.form['email']

            newPassword = request.form['newpassword']
            confirmPassword = request.form['confirmedPassword']
            
            position_id=request.form.get('position')
            department_id=request.form.get('department')
    
            selected_status = request.form.get('status')
            status_value = 1 if selected_status == 'Active' else 0
            user_role_id = request.form.get('isAdmin')
            

               # Check if account exists using MySQL
            query = """
            SELECT 
                u.username, 
                u.email
            FROM 
                user u
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
                    flash('Account already exists!','error')
                   
                elif account[1] == email:
                    flash('Email already exists!','error')
                   
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!','error')
               
            elif not re.match(r'^[A-Za-z0-9]+$', username):
                flash('Username must contain only characters and numbers!','error')
                
            elif newPassword !=confirmPassword:
                flash('Password confirmation failed.!','error')
            
                
            else:
                #Automatic salt generation
                random_text = secrets.token_hex(16)
                # Set default user profile
                first_name=request.form.get('firstName')
                last_name=request.form.get('lastName') 
                phone=request.form.get('phone')
                hire_date=request.form.get('hireDate')              
                join_date =datetime.now()
                # Automatically generate a user id
                staff_id = generate_user_num('STAF')
                
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                hashed = hashing.hash_value(newPassword, salt=random_text)
                

                connection, cursor = get_db_connection()   
                try:
                    cursor.execute('INSERT INTO user VALUES (NULL,%s,%s, %s, %s, %s, %s,%s, %s, %s, %s)', (newusername, hashed, random_text, first_name, last_name, email, phone, join_date, user_role_id, status_value))

                    new_user_id = cursor.lastrowid
                    if not hire_date:
                        hire_date = None
                    cursor.execute('''
                        INSERT INTO staff (user_id,staff_id,hire_date, position_id,department_id) 
                            VALUES (%s, %s,%s,%s, %s)
                        ''', (new_user_id, staff_id, hire_date,position_id,department_id))
                    connection.commit()
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    cursor.close()
                    connection.close()
                flash('You have successfully registered!','success')           
        elif request.method == 'POST':
            flash('Please fill out the form!','error')
        return render_template("admin/staffAdd.html",isLogin=isLogin,username=username,roleid=roleid,position_list=position_list, department_list=department_list)
    else:
        return redirect(url_for('login'))

def get_staff_info(extra_query=''):
    query = """
        SELECT 
            u.id,
            u.username,
            u.first_name,
            u.last_name,
            u.email,
            u.phone,
            DATE_FORMAT(u.join_date, '%Y-%m-%d') AS formatted_join_date,
            u.status,
            s.staff_id,
            DATE_FORMAT(s.hire_date, '%Y-%m-%d') AS formatted_hire_date,
            p.position_name,
            d.department_name,
            u.role_id
        FROM staff s
        JOIN user u ON s.user_id = u.id
        JOIN position p ON s.position_id = p.id
        JOIN department d ON s.department_id = d.id
        """ 
    if extra_query:
        query += extra_query
    connection, cursor = get_db_connection()
    try:
        cursor.execute(query)
        staff_list = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()
    return staff_list

def get_position_list():
    query = """
        SELECT 
            id,
            position_name
        FROM position
        """ 
    connection, cursor = get_db_connection()
    try:
        cursor.execute(query)
        position_list = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()
    return position_list  

def get_department_list():
    query = """
        SELECT 
            id,
            department_name
        FROM department
        """ 
    connection, cursor = get_db_connection()
    try:
        cursor.execute(query)
        department_list = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()
    return department_list
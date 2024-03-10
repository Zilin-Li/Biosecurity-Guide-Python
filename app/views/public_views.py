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




# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
hashing = Hashing(app)  #create an instance of hashing


@app.route("/")
def home(): 
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    return render_template("public/home.html", isLogin=isLogin, username=username,roleid=roleid)

@app.route("/login", methods=['GET', 'POST'])
def login():
    isLogin=session.get('loggedin')
    if not isLogin:
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
                user u
            WHERE username = %s;
                """ 
            connection, cursor = get_db_connection()
            account = None
            try:
                cursor.execute(query, (username,))
                # Fetch one record and return result
                account = cursor.fetchone()
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
            
            if account is not None:
                password = account[2]
                if hashing.check_value(password, user_password, salt=account[3]):
                # If account exists in accounts table 
                # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['id'] = account[0]
                    session['username'] = account[1]
                    session['roleid'] = account[4]

                    username = session.get('username')
                    userid = session.get('id')
                    if account[4] == 1:
                        return redirect( url_for('admin_dashboard'))                  
                    elif account[4] == 2:   
                        return redirect( url_for('staff_dashboard'))
                    elif account[4] == 3:   
                        return redirect( url_for('public_dashboard'))
                            
                else:
                    #password incorrect
                    msg = 'Incorrect password!'             
            else:
                # Account doesnt exist or username incorrect
                msg = 'Incorrect username'
        # Show the login form with message (if any)   
        return render_template('public/login.html', msg=msg)
    else:
        return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    isLogin=session.get('loggedin')
    if not isLogin:
    # Output message if something goes wrong...
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'confirmPassword'in request.form:
            # Create variables for easy access
            username = request.form['username']
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
                OR u.email = %s;
                """ 
            connection, cursor = get_db_connection()
            account = None
            try:
                cursor.execute(query, (username,email,))
                account = cursor.fetchone()
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
            # msg = account
            # If account exists show error and validation checks
            if account:
                if account[0]== username:
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
                first_name = None
                last_name = None
                phone = None
                join_date =datetime.now()
                role_id = 3
                status = 1
                # Automatically generate a user id
                horticulturalist_id = generate_user_num('HORT')
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                hashed = hashing.hash_value(password, salt=random_text)
                connection, cursor = get_db_connection()
                try:
                    cursor.execute('INSERT INTO user VALUES (NULL,%s,%s, %s, %s, %s, %s,%s, %s, %s, %s)', (username, hashed, random_text, first_name, last_name, email, phone, join_date, role_id, status))
                    user_id = cursor.lastrowid
                    cursor.execute('''
                        INSERT INTO Horticulturalist (user_id, horticulturalist_id) 
                            VALUES (%s, %s)
                        ''', (user_id, horticulturalist_id))
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
        # Show registration form with message (if any)
        return render_template("public/register.html",msg=msg)
    else:
         return redirect(url_for('home'))

def generate_user_num(roleName):
    # Gets the year, month, day, hour, second of the current time
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # Generate a 5-digit random number
    random_number = random.randint(10000, 99999)
    # Creat user id
    user_id = f"{roleName}{timestamp}{random_number}"
    return user_id

@app.route('/logout')
def logout():
    isLogin=session.get('loggedin')
    if isLogin:
    # Remove session data, this will log the user out
        session.pop('loggedin', False)
        session.pop('id', None)
        session.pop('username', None)
        session.pop('roleid', None)
        # Redirect to login page
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route("/dashboard")
def public_dashboard():
    # account='12345'
    isLogin=session.get('loggedin')
    username = session.get('username')
    # userid = session.get('id')
    roleid=session.get('roleid')
    return redirect( url_for('guide'))

# Profile - edit & change password
# Edit profile
@app.route("/profile/edit_profile")
def edit_user_profile():
    isLogin=session.get('loggedin')
    roleid=session.get('roleid')
    username = session.get('username')
    userid = session.get('id')
    user_profile = None 
    if isLogin:
        connection, cursor = get_db_connection()
        if roleid == 3:            
            query = """
                SELECT 
                    u.username, 
                    IFNULL(u.first_name, '') AS first_name ,
                    IFNULL(u.last_name,  '') AS last_name,
                    u.email, 
                    IFNULL(u.phone, '') AS phone, 
                    DATE_FORMAT(u.join_date, '%Y-%m-%d') AS formatted_join_date, 
                    h.horticulturalist_id, 
                    IFNULL(h.address,'') AS address,
                    u.status
                FROM 
                    user u
                JOIN 
                    horticulturalist h ON u.id = h.user_id
                WHERE 
                    u.id = %s;
            """
            try:
                cursor.execute(query, (userid,))
                user_profile = cursor.fetchone()
            except Exception as e:
                print(f"An error occurred: {e}")
        if roleid == 1 or  roleid == 2:
            query2 = """
                SELECT
                    u.username, 
                    IFNULL(u.first_name, '') AS first_name ,
                    IFNULL(u.last_name,  '') AS last_name,
                    u.email, 
                    IFNULL(u.phone, '') AS phone, 
                    s.staff_id,
                    DATE_FORMAT(s.hire_date, '%Y-%m-%d') AS formatted_hire_date, 
                    p.position_name,
                    d.department_name,
                    u.status
                FROM
                    user u
                INNER JOIN staff s ON u.id = s.user_id
                INNER JOIN position p ON s.position_id = p.id
                INNER JOIN department d ON s.department_id = d.id
                WHERE
                    u.id = %s;
                """
            try:
                cursor.execute(query2, (userid,))
                user_profile = cursor.fetchone()
            except Exception as e:
                print(f"An error occurred: {e}")
        cursor.close()
        connection.close()
        return render_template('public/editUserProfile.html',isLogin =isLogin,username=username,roleid=roleid,user_profile=user_profile)
    else:  
        return redirect(url_for('login'))
    

@app.route('/profile/edit_user_profile/submit', methods=['POST'])
def update_user_profile():
    isLogin=session.get('loggedin')
    roleid=session.get('roleid')
    if isLogin:
        connection, cursor = get_db_connection()
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        phone=request.form['phone']
        userid = session.get('id')
        update_user_query="""
            UPDATE user
            SET first_name = %s,
                last_name = %s,
                phone = %s
            WHERE id = %s;
            """  
        update_Hoti_query="""
                UPDATE Horticulturalist
                SET address = %s
                WHERE user_id = %s;
            """ 
        if roleid == 3:    
            address=request.form['address']           
            try:
                cursor.execute(update_user_query, (first_name,last_name,phone,userid,)) 
                cursor.execute(update_Hoti_query, (address, userid,))
                connection.commit()
                flash("The profile has been updated.","success")       
            except Exception as e:
                print(f"An error occurred: {e}")
        elif roleid == 1 or  roleid == 2:
            try:
                cursor.execute(update_user_query, (first_name,last_name,phone,userid,)) 
                connection.commit()
                flash("The profile has been updated.","success")
            except Exception as e:
                print(f"An error occurred: {e}")
        cursor.close()
        connection.close()    
        return redirect(url_for('edit_user_profile'))
    else:
        return redirect(url_for('login'))


@app.route('/test')
def test():
    flash("Test", 'error')
    return redirect(url_for('login'))

@app.route("/profile/change_password", methods=['GET','POST'])
# user,staff and admin can use this function.
def change_password():
    # account='12345' 
    isLogin=session.get('loggedin')
    userid = session.get('id')
    username = session.get('username')
    roleid=session.get('roleid') 
    msg = ''
    if request.method == 'POST' and 'currentPassword' in request.form and 'newPassword' in request.form and 'confirmNewPassword' in request.form:   
        currentPassword = request.form['currentPassword']
        newPassword = request.form['newPassword']
        confirmNewPassword = request.form['confirmNewPassword']
        # Get the stored password from database
        get_password_query = """
            SELECT 
                u.hashed_password, 
                u.salt 
            FROM 
                user u
            WHERE id = %s;
                """ 
        connection, cursor = get_db_connection()
        try:
            cursor.execute(get_password_query, (userid,))
            storedPassword = cursor.fetchone()
        except Exception as e:
                print(f"An error occurred: {e}")    
        if not currentPassword or not newPassword or not confirmNewPassword:
            msg = 'Please fill out the form!'
        elif not hashing.check_value(storedPassword[0], currentPassword, salt=storedPassword[1]):
            msg = 'The current password is incorrect.'
        elif newPassword != confirmNewPassword:
            msg = 'Password confirmation failed.!' 
        else:
            random_text = secrets.token_hex(16)
            hashedPassword = hashing.hash_value(newPassword, salt=random_text)
            msg=hashedPassword
            update_password_query="""        
                UPDATE user
                SET hashed_password = %s,
                    salt=%s
                WHERE id = %s;
            """
            try:
                cursor.execute(update_password_query, (hashedPassword, random_text,userid))
                connection.commit()
            except Exception as e:
                print(f"An error occurred: {e}")
        cursor.close()
        connection.close()
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('public/changePassword.html',isLogin =isLogin,username=username,roleid=roleid,msg=msg)

 

@app.route("/guide")
def guide():
    # account='12345'
    isLogin=session.get('loggedin')
    username = session.get('username')
    userid = session.get('id')
    roleid=session.get('roleid')
    guide_list = None
    if not isLogin:
        return redirect(url_for('login'))
    else:
        query ="""
        SELECT
            b.id,
            b.common_name,
            b.is_present_in_nz,
            bi.image_path
        FROM
            biosecurity b
        LEFT JOIN
            biosecurityimage bi ON b.id = bi.biosecurity_id AND bi.is_primary = 1
        """
        connection, cursor = get_db_connection()
        try:
            cursor.execute(query)
            guide_list = cursor.fetchall()
        except Exception as e:
                print(f"An error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

        return render_template('public/guidePage.html',isLogin =isLogin,username=username,roleid=roleid,guide_list=guide_list)

# disyplay the detail of the biosecurity


@app.route("/guide/<int:biosecurity_id>")
def guide_detail(biosecurity_id):
    isLogin = session.get('loggedin')
    username = session.get('username')
    userid = session.get('id')
    roleid = session.get('roleid')
    
    if not isLogin:
        return redirect(url_for('login'))
    
    biosecurity_query = """
    SELECT
        b.id,
        b.common_name,
        b.scientific_name,
        b.key_char,
        b.biology,
        b.impact,
        b.source_url,
        b.is_present_in_nz
    FROM
        biosecurity b
    WHERE
        b.id = %s
    """

    images_query = """
    SELECT
        image_path,
        description,
        is_primary
    FROM
        biosecurityImage
    WHERE
        biosecurity_id = %s
    """
    
    connection, cursor = get_db_connection()
    try:
        cursor.execute(biosecurity_query, (biosecurity_id,))
        biosecurity_detail = cursor.fetchone()
        
        # Fetch all images related to the biosecurity
        cursor.execute(images_query, (biosecurity_id,))
        images = cursor.fetchall()
        print(images)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        biosecurity_detail = None
        images = []
    finally:
        if connection:
            cursor.close()
            connection.close()

    # get primary image
    
    primary_image = None
    other_images = []
    if images:
        primary_image = next((image for image in images if image[2]), None)
    # get other images
        other_images = [image for image in images if not image[2]]
        print(other_images)
         

    # format data for display
    if biosecurity_detail:
        biosecurity_detail = {
            'id': biosecurity_detail[0],
            'common_name': biosecurity_detail[1],
            'scientific_name': biosecurity_detail[2],
            'key_char': biosecurity_detail[3],
            'biology': biosecurity_detail[4],
            'impact': biosecurity_detail[5],
            'source_url': biosecurity_detail[6],
            'is_present_in_nz': biosecurity_detail[7],
            'primary_image': primary_image[0] if primary_image else 'default.jpg',
            'other_images': other_images    
        }

    
    return render_template('public/guideDetail.html', isLogin=isLogin, username=username, roleid=roleid, guide_details=biosecurity_detail)


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

@app.route("/staff/dashboard")
def staff_dashboard():
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    if isLogin and roleid == 2:
        return render_template("staff/dashboard.html",isLogin=isLogin,username=username,roleid=roleid)
    else:
        return redirect( url_for('login'))
    
@app.route('/<role>/guide_management')
def guide_management(role):
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    if isLogin:
        expected_role = 'admin' if roleid == 1 else 'staff'
        if role != expected_role:
            return redirect(url_for('home'))
        else:
            return render_template('staff/guideMgt.html',isLogin=isLogin,username=username,roleid=roleid)
    else:
        return redirect(url_for('login'))
       
@app.route('/<role>/user')
def user_management(role):
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    
    if isLogin:
        expected_role = 'admin' if roleid == 1 else 'staff'
        if role != expected_role:
            return redirect(url_for('home'))
        else:
            query = """
            SELECT 
                u.id, 
                u.username, 
                u.email, 
                u.status, 
                h.horticulturalist_id 
            FROM 
                User u
            LEFT JOIN 
                Horticulturalist h ON u.id = h.user_id
            WHERE u.role_id = 3
            ORDER BY u.username;
                """ 
            connection, cursor = get_db_connection()
            try:
                cursor.execute(query)
                user_list = cursor.fetchall()
                print(user_list)
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
            return render_template('staff/userMgt.html',isLogin=isLogin,username=username,roleid=roleid,user_list=user_list)
    else:
        return redirect(url_for('login'))

@app.route('/<role>/user/detail/<user_id>')
def user_detail(role,user_id):  
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    
    if isLogin:
        expected_role = 'admin' if roleid == 1 else 'staff'
        if role != expected_role:
            return redirect(url_for('home'))
        else:
            query="""
            SELECT 
                u.id, 
                u.username, 
                CONCAT(COALESCE(u.first_name, ''), ' ', COALESCE(u.last_name, '')) AS full_name,
                u.email,
                u.phone,
                u.join_date, 
                u.status, 
                h.horticulturalist_id,
                h.address
            FROM 
                User u
            JOIN 
                Horticulturalist h ON u.id = h.user_id
            WHERE u.id = %s;
            """
            connection, cursor = get_db_connection()
            try:
                cursor.execute(query,(user_id,))
                user_details = cursor.fetchall()
                
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                cursor.close()
                connection.close()
            return render_template('staff/userDetail.html',isLogin=isLogin,username=username,roleid=roleid,user_details=user_details)
    else:
        return redirect(url_for('login'))         
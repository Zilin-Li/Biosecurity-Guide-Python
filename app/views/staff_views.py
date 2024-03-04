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
from datetime import datetime

@app.route("/staff/dashboard")
def staff_dashboard():
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    if roleid != 2:
        return redirect( url_for('home'))
    
    return render_template("staff/dashboard.html",isLogin=isLogin,username=username,roleid=roleid)

@app.route("/staff/profile")
def staff_profile():
    return "Staff profile"
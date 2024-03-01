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
from datetime import datetime, date
import secrets
import random

@app.route("/admin/dashboard")
def admin_dashboard():
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    return render_template("admin/dashboard.html",isLogin=isLogin,username=username,roleid=roleid)

@app.route("/admin/profile")
def admin_profile():
    return "Admin profile"
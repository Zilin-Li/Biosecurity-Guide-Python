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

@app.route("/admin/dashboard")
def admin_dashboard():

    return render_template("admin/dashboard.html")

@app.route("/admin/profile")
def admin_profile():
    return "Admin profile"
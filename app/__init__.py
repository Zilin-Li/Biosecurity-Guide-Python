# Bring our application together and tell Python interpreter that this is a package.
#Bring in flask and declace app variable
from flask import Flask
import mysql.connector
from .connect import *


app = Flask(__name__)

class Config(object):
    IMAGE_PATH = '/home/LUZilinLi1159924/Biosecurity/app/static/img/pests'


app.config.from_object(Config)


image_path = app.config['IMAGE_PATH']

def get_db_connection():
    connection = mysql.connector.connect(
        user=connect.dbuser,
        password=connect.dbpass,
        host=connect.dbhost,
        database=connect.dbname,
        autocommit=True
    )
    cursor = connection.cursor()
    return connection, cursor

from .views import public_views, staff_views, admin_views

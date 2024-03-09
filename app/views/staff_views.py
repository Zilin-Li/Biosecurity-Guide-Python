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

# display all guides in table
@app.route('/<role>/guide_management')
def guide_management(role):
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    if isLogin:
        expected_role = 'admin' if roleid == 1 else 'staff'
        if role != expected_role:
            return redirect(url_for('login'))
        else:
            # query to get all guides id, common name, scientific name,and primary image
            query ="""
                SELECT
                    b.id,
                    b.common_name,
                    b.scientific_name,
                    b.is_present_in_nz,
                    bi.image_path
                FROM
                    Biosecurity b
                LEFT JOIN
                    BiosecurityImage bi ON b.id = bi.biosecurity_id AND bi.is_primary = 1
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
            return render_template('staff/guideMgt.html',isLogin=isLogin,username=username,roleid=roleid,guide_list=guide_list)
            
    else:
        return redirect(url_for('login'))



@app.route('/<role>/guide/edit/<int:biosecurity_id>', methods=['GET'])
def guide_edit(role,biosecurity_id):
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    # 首先，检查用户是否已登录
    if 'loggedin' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    # 连接到数据库
    connection, cursor = get_db_connection()
    cursor = connection.cursor()
    info_query="""SELECT 
        b.id, 
        b.common_name, 
        b.scientific_name, 
        b.key_char,
        b.biology,
        b.impact,
        b.source_url,
        b.is_present_in_nz 
        FROM Biosecurity b 
        WHERE b.id = %s"""
    primary_image_query = """
        SELECT 
            bi.image_path 
        FROM 
            BiosecurityImage bi 
        WHERE 
            bi.biosecurity_id = %s 
        AND 
            bi.is_primary = 1
        """
    image_query = """
        SELECT 
            bi.image_path 
        FROM 
            BiosecurityImage bi 
        WHERE 
            bi.biosecurity_id = %s
        AND 
        bi.is_primary = 0
        """
    # join Biosecurity and BiosecurityImage tables to get guide details and primary image
    cursor.execute(info_query, (biosecurity_id,))
    guide_info = cursor.fetchone()
    print('guide_info~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:', guide_info)
    cursor.execute(primary_image_query, (biosecurity_id,))
    primary_image = cursor.fetchone()

    cursor.execute(image_query, (biosecurity_id,))
    images = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    connection.close()
    primary_image = primary_image if primary_image else ('',)
    images = []
    # format data
    guide_details = {
        'id': guide_info[0],
        'common_name': guide_info[1],
        'scientific_name': guide_info[2],
        'key_char': guide_info[3],
        'biology': guide_info[4],
        'impact': guide_info[5],
        'source_url': guide_info[6],
        'is_present_in_nz': guide_info[7],
        'primary_image': primary_image[0],
        'images': images
    }

    # 渲染编辑表单模板
    print('guide_details:', guide_details)
    print(guide_details)
    return render_template('staff/guideEdit.html',isLogin=isLogin,username=username,roleid=roleid,guide_details=guide_details)


@app.route('/<role>/guide/edit/<int:biosecurity_id>', methods=['POST'])
def guide_update(role,biosecurity_id):
    
    print('biosecurity_id:', biosecurity_id)
    return redirect(url_for('guide_management', role=role))
    
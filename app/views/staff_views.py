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
import os
import uuid

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
            bi.id,
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
    cursor.execute(primary_image_query, (biosecurity_id,))
    primary_image = cursor.fetchone()

    cursor.execute(image_query, (biosecurity_id,))
    images = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    connection.close()
    primary_image = primary_image if primary_image else ('',)


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

    return render_template('staff/guideEdit.html',isLogin=isLogin,username=username,roleid=roleid,guide_details=guide_details)









# update guide
@app.route('/<role>/guide/edit/<int:biosecurity_id>', methods=['POST'])
def guide_update(role,biosecurity_id):
    isLogin=session.get('loggedin')
    username = session.get('username')
    roleid=session.get('roleid')
    # 首先，检查用户是否已登录
    if 'loggedin' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    # 获取表单数据
    common_name = request.form['common_name']
    scientific_name = request.form['scientific_name']
    key_char = request.form['key_char']
    biology = request.form['biology']
    impact = request.form['impact']
    source_url = request.form['source_url']
    is_present_in_nz = request.form['is_present_in_nz']
    # 连接到数据库
    connection, cursor = get_db_connection()
    cursor = connection.cursor()
    # 更新数据库
    update_query = """
        UPDATE Biosecurity 
        SET 
            common_name = %s, 
            scientific_name = %s, 
            key_char = %s, 
            biology = %s, 
            impact = %s, 
            source_url = %s, 
            is_present_in_nz = %s
        WHERE 
            id = %s
        """
    cursor.execute(update_query, (common_name, scientific_name, key_char, biology, impact, source_url, is_present_in_nz, biosecurity_id))
    connection.commit()
    cursor.close()
    connection.close()
    flash('Guide updated successfully!')
    # 重定向到一个新的页面，例如指南详情页或指南列表
    return redirect(url_for('guide_edit', role=role, biosecurity_id=biosecurity_id))


# delete image
@app.route('/<role>/guide/image/delete/<int:image_id>', methods=['POST'])
def guide_image_delete(role, image_id):

    biosecurity_id = request.form.get('biosecurity_id')
    # connect to database
    connection, cursor = get_db_connection()
    cursor = connection.cursor()
    # get image path
    image_query = """
        SELECT 
            bi.image_path 
        FROM 
            BiosecurityImage bi 
        WHERE 
            bi.id = %s
        """
    cursor.execute(image_query, (image_id,))
    image_path = cursor.fetchone()[0]
    # delete image from database
    delete_query = """
        DELETE FROM BiosecurityImage WHERE id = %s
        """
    cursor.execute(delete_query, (image_id,))
    connection.commit()
    cursor.close()
    connection.close()

    # delete image from file system
    os.remove(os.path.join('app/static/img/pests/', image_path))

    return redirect(url_for('guide_edit', role=role, biosecurity_id=biosecurity_id))



# validate image file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
# add image
@app.route('/<role>/guide/image/add/<int:biosecurity_id>', methods=['POST'])
def guide_image_add(role, biosecurity_id):

    # 检查是否有文件在提交的表单中
    if 'new_image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    new_images = request.files.getlist('new_image')

    for image in new_images:
        # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空部分
        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(image.filename):
            flash('Invalid file type')
            return redirect(request.url)

        # generate a random filename by uuid
        random_filename = str(uuid.uuid4())
        _, ext = os.path.splitext(image.filename)
        filename = random_filename + ext

        image_path = os.path.join('app/static/img/pests/', filename)
        image.save(image_path)
        
        # save image to database
        connection, cursor = get_db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO BiosecurityImage (biosecurity_id, image_path, is_primary)
            VALUES (%s, %s, 0)
            """
        cursor.execute(query, (biosecurity_id, filename))
        connection.commit()
        cursor.close()
        connection.close()

    flash('Images uploaded successfully!')
    # 重定向到一个新的页面，例如指南详情页或指南列表
    return redirect(url_for('guide_edit', role=role, biosecurity_id=biosecurity_id))

# replace primary image
@app.route('/<role>/guide/image/replace/<int:biosecurity_id>', methods=['POST'])
def guide_image_replace(role, biosecurity_id):
    # get primary image
    connection, cursor = get_db_connection()
    cursor = connection.cursor()
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
    cursor.execute(primary_image_query, (biosecurity_id,))
    primary_image = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    # save uploaded image to app/static/images/pests
    new_image = request.files['primary_image']
    if new_image.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if not allowed_file(new_image.filename):
        flash('Invalid file type')
        return

    random_filename = str(uuid.uuid4())
    _, ext = os.path.splitext(new_image.filename)
    filename = random_filename + ext
    image_path = os.path.join('app/static/img/pests/', filename)
    new_image.save(image_path)

    # update database
    connection, cursor = get_db_connection()
    cursor = connection.cursor()
    # update primary image
    update_query = """
        UPDATE BiosecurityImage 
        SET image_path = %s 
        WHERE biosecurity_id = %s 
        AND is_primary = 1
        """
    cursor.execute(update_query, (filename, biosecurity_id))
    connection.commit()
    cursor.close()
    connection.close()

    # delete old primary image from file system
    os.remove(os.path.join('app/static/img/pests/', primary_image))

    flash('Primary image replaced successfully!')
    # 重定向到一个新的页面，例如指南详情页或指南列表
    return redirect(url_for('guide_edit', role=role, biosecurity_id=biosecurity_id))

# add guide
@app.route('/<role>/guide/add', methods=['GET'])
def guide_add(role):
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    # 首先，检查用户是否已登录
    if 'loggedin' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    return render_template('staff/guideAdd.html',isLogin=isLogin,username=username,roleid=roleid)

# insert guide
@app.route('/<role>/guide/add', methods=['POST'])
def guide_insert(role):
    isLogin=session.get('loggedin')
    username = session.get('username') 
    roleid=session.get('roleid')
    # 首先，检查用户是否已登录
    if 'loggedin' not in session:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))
    # 获取表单数据
    common_name = request.form['common_name']
    scientific_name = request.form['scientific_name']
    key_char = request.form['key_char']
    biology = request.form['biology']
    impact = request.form['impact']
    source_url = request.form['source_url']
    is_present_in_nz = request.form['is_present_in_nz']
    # 连接到数据库
    connection, cursor = get_db_connection()
    cursor = connection.cursor()
    # 插入数据
    insert_query = """
        INSERT INTO Biosecurity 
        (common_name, scientific_name, key_char, biology, impact, source_url, is_present_in_nz) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    cursor.execute(insert_query, (common_name, scientific_name, key_char, biology, impact, source_url, is_present_in_nz))
    connection.commit()
    biosecurity_id = cursor.lastrowid  # 获取新插入行的ID

    print(biosecurity_id, '~~~~~~~~~~~~~~~##################~~~~~~~~~~~~~~~~~~~~')
    cursor.close()
    connection.close()


    # save primary image to app/static/images/pests
    primary_image = request.files['primary_image']
    if primary_image.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if not allowed_file(primary_image.filename):
        flash('Invalid file type')
        return
    random_filename = str(uuid.uuid4())
    _, ext = os.path.splitext(primary_image.filename)
    filename = random_filename + ext
    image_path = os.path.join('app/static/img/pests/', filename)
    primary_image.save(image_path)

    # save image to database
    connection, cursor = get_db_connection()
    cursor = connection.cursor()

    # insert primary image
    insert_query = """
        INSERT INTO BiosecurityImage (biosecurity_id, image_path, is_primary)
        VALUES (%s, %s, 1)
        """
    cursor.execute(insert_query, (biosecurity_id, filename))
    connection.commit()
    cursor.close()
    connection.close()

    # save uploaded images to app/static/images/pests
    new_images = request.files.getlist('new_image')
    for image in new_images:
        if image.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(image.filename):
            flash('Invalid file type')
            return redirect(request.url)
        random_filename = str(uuid.uuid4())
        _, ext = os.path.splitext(image.filename)
        filename = random_filename + ext
        image_path = os.path.join('app/static/img/pests/', filename)
        image.save(image_path)
        # save image to database
        connection, cursor = get_db_connection()
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO BiosecurityImage (biosecurity_id, image_path, is_primary)
            VALUES (%s, %s, 0)
            """
        cursor.execute(insert_query, (biosecurity_id, filename))
        connection.commit()
        cursor.close()
        connection.close()

    flash('Guide added successfully!')
    # 重定向到一个新的页面，例如指南详情页或指南列表
    return redirect(url_for('guide_management', role=role))





    

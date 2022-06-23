from flask import Flask,Blueprint, render_template, request, redirect, url_for, session, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
from PIL import Image
import io
from . import db

admin = Blueprint('admin', __name__)

@admin.route("/admin_login/" , methods =['GET', 'POST'])
def admin_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['admin_id']
            #session['name'] = account['name']
            msg = 'Logged in successfully !'
            return redirect(url_for('admin.admin_index'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('admin_login.html', msg = msg,)

@admin.route("/admin_index")
def admin_index():
     if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM posts order by post_id desc') 
        posts = cursor.fetchall() 

        return render_template('admin_index.html',posts=posts)
      #return redirect(url_for('admin.adlogin'))
      
@admin.route("/admin_viewpost/<int:p_id>", methods=['GET', 'POST'])
def admin_viewpost(p_id):    
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM posts WHERE post_id = %s', (p_id,))    
        post = cursor.fetchone()
        cont = post['content'].replace('\n', '<br>')
        return render_template('admin_viewpost.html', post=post, cont=cont)
          
    return redirect(url_for('admin.admin_login'))

@admin.route("/delpost/<int:p_id>", methods=['post','get'])  
def delpost(p_id):    
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from posts where post_id = % s', (p_id, ))
    db.connection.commit()
    return redirect(url_for('admin.admin_index'))

@admin.route("/messages")
def messages():
     if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM contact') 
        msg = cursor.fetchall() 

        return render_template('messages.html',msg=msg)
    
@admin.route("/users/")
def users():
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('select * from users')
        users = cursor.fetchall()   
        return render_template('users.html', users=users)
    return redirect(url_for('admin.admin_login'))

@admin.route("/deluser/<int:u_id>", methods=['post','get'])  
def deluser(u_id):    
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from users where id = % s', (u_id, ))
    db.connection.commit()
    return redirect(url_for('admin.users'))

@admin.route('/admin_logout')
def admin_logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   #session.pop('name', None)
   return redirect(url_for('admin.admin_login'))
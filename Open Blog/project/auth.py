from flask import Flask,Blueprint, render_template, request, redirect, url_for, session, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
from PIL import Image
import io
from . import db

auth = Blueprint('auth', __name__)

@auth.route("/signup/" ,methods=['POST', 'GET'])
def signup():  
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'profilepic' in request.form and 'mobile' in request.form and 'email' in request.form and 'password' in request.form and 'interest[]' in request.form:
        name = request.form['name']
        username = request.form['username']
        propic = request.form['profilepic']
        mobile = request.form['mobile']  
        email = request.form['email']
        password = request.form['password']
        interests = request.form['interest[]']      
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
            
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL,% s, % s, % s, % s, % s, % s, %s)', (name, username, mobile, email, password, interests,propic, ))
            db.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)

@auth.route("/login/" , methods =['GET', 'POST'])
def signin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['name'] = account['name']
            msg = 'Logged in successfully !'
            return redirect(url_for('views.home'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg,)

@auth.route("/account/" ,methods=['POST', 'GET'])
def account(): 
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()    
        return render_template('account.html', account=account)
    return redirect(url_for('views.signin'))

@auth.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('name', None)
   return redirect(url_for('views.home'))



from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
from PIL import Image
import io
from . import db

views = Blueprint('views', __name__)

@views.route("/")
def home():
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()
        interest=account['interests']
        cursor.execute('SELECT * FROM posts order by post_id desc') 
        posts = cursor.fetchall()  
        cursor.execute('SELECT * FROM posts where category=%s limit 5',(interest,)) 
        post = cursor.fetchall()
        return render_template('index.html', account=account, posts=posts,post=post)
    return redirect(url_for('auth.signin'))

@views.route("/category/<string:cat>")
def category(cat):
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()
        interest=account['interests']
        cursor.execute('SELECT * FROM posts where category=%s order by post_id desc',(cat,)) 
        posts = cursor.fetchall()  
        cursor.execute('SELECT * FROM posts where category=%s limit 5',(interest,)) 
        post = cursor.fetchall()
        return render_template('index.html', account=account, posts=posts,post=post)
    return redirect(url_for('auth.signin'))

@views.route("/sort/<string:sort>")
def sort(sort):
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()
        interest=account['interests']
        if sort=='asc':
            cursor.execute('SELECT * FROM posts order by post_id asc') 
            posts = cursor.fetchall() 
        elif sort=='desc':
            cursor.execute('SELECT * FROM posts order by post_id desc') 
            posts = cursor.fetchall() 
        
        cursor.execute('SELECT * FROM posts where category=%s limit 5',(interest,)) 
        post = cursor.fetchall()
        return render_template('index.html', account=account, posts=posts,post=post)
    return redirect(url_for('auth.signin'))

@views.route("/post/" ,methods=['GET', 'POST'])
def post():
    if request.method == 'POST' and 'coverimg' in request.form and 'title' in request.form and 'subtitle' in request.form and 'category' in request.form and 'content' in request.form:
        coverimg = request.form['coverimg']
        title = request.form['title']
        subtitle=request.form['subtitle']
        category=request.form['category']
        content = request.form['content']        
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        accounta = cursor.fetchone()
        aid = session['id']
        aname = session['name']
        cursor.execute('INSERT INTO posts VALUES (% s,% s, % s, % s,NULL, % s, % s,% s,curdate())', (aid, coverimg, title, content, subtitle, category,aname ))
        db.connection.commit()
        
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
   
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()    
        return render_template('post.html', account=account)
    return redirect(url_for('signin'))


@views.route("/mypost/")
def mypost():
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()   
        cursor.execute('select * from posts where user_id =% s', (session['id'],)) 
        mypost=cursor.fetchall()
        return render_template('mypost.html', account=account, mypost=mypost)
    return redirect(url_for('auth.signin'))



@views.route("/viewpost/<int:p_id>", methods=['GET', 'POST'])
def viewpost(p_id):    
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM posts WHERE post_id = %s', (p_id,))    
        post = cursor.fetchone()
        cont = post['content'].replace('\n', '<br>')
        return render_template('viewpost.html', account=account, post=post, cont=cont)
    
    if request.method == 'POST':
        if request.form['delpos'] == 'dele':
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('delete from posts where post_id = % s', (p_id, ))       
    return redirect(url_for('auth.signin'))

@views.route("/delpos/<int:p_id>", methods=['post','get'])  
def delpos(p_id):    
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from posts where post_id = % s', (p_id, ))
    db.connection.commit()
    return redirect(url_for('views.mypost'))

@views.route("/delfav/<int:p_id>", methods=['post','get'])  
def delfav(p_id):    
    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from favorites where (post_id = % s) and (user_id= %s)', (p_id, session['id'] ),)
    db.connection.commit()
    return redirect(url_for('views.favorites'))

@views.route("/update/<int:p_id>", methods=['post','get'])  
def update(p_id):    
    if request.method == 'POST' and 'coverimg' in request.form and  'title' in request.form and 'subtitle' in request.form and 'category' in request.form and 'content' in request.form:
        coverimg = request.form['coverimg']
        title = request.form['title']
        subtitle=request.form['subtitle']
        category=request.form['category']
        content = request.form['content']   
        aid = session['id']
        aname = session['name']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select coverpic from posts where post_id=%s',(p_id,))
        posts=cursor.fetchone()  
        cp=posts['coverpic']
        if coverimg:          
            cursor.execute('update posts set user_id=%s, coverpic=%s, title=%s, content=%s, post_id=%s, subtitle=%s, category=%s, aname=%s, post_date=curdate() where post_id=%s', (aid,coverimg, title, content, p_id, subtitle, category,aname, p_id ))
        else:   
            coverimg=cp 
            cursor.execute('update posts set user_id=%s, coverpic=%s, title=%s, content=%s, post_id=%s, subtitle=%s, category=%s, aname=%s, post_date=curdate() where post_id=%s', (aid,coverimg, title, content, p_id, subtitle, category,aname, p_id ))
        db.connection.commit()

    return redirect(url_for('views.mypost'))

@views.route("/edit_post/<int:p_id>", methods=['post','get'])  
def edit_post(p_id):    
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM posts WHERE post_id = %s', (p_id,))    
        post = cursor.fetchone()        
        return render_template('edit_post.html',account=account, post=post)

    

@views.route("/add_favorites/<int:p_id>", methods=['post','get'])
def add_favorites(p_id):
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()
        cursor.execute('select * from posts where post_id=%s',(p_id,))
        posts=cursor.fetchone()
        title= posts['title']
        content= posts['content']
        aname= posts['aname']
        date= posts['post_date']
        coverpic=posts['coverpic']
        cursor.execute('insert into favorites values (NULL, %s, %s,%s,%s,%s,%s,%s)',(session['id'],p_id,title,content,aname,date,coverpic,))    
        post = cursor.fetchone()        
        db.connection.commit()
        return redirect(url_for('views.favorites'))
    
@views.route("/favorites/", methods=['post','get'])
def favorites():
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()     
        cursor.execute('select * from favorites where user_id = %s', (session['id'], ))   
        favpost=cursor.fetchall()
        db.connection.commit()
    return render_template('favorites.html', account=account, favpost=favpost)

@views.route("/authors/")
def authors():
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone() 
        cursor.execute('select name,mobile,email,profilepic from users')
        authors = cursor.fetchall()   
        return render_template('authors.html', account=account, authors=authors)
    return redirect(url_for('signin'))

@views.route("/update_ac/", methods=['post','get'])  
def update_ac():    
    if request.method == 'POST' and 'name' in request.form and 'profilepic' in request.form and 'mobile' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        profilepic=request.form['profilepic']
        mobile=request.form['mobile']
        email=request.form['email']
        password = request.form['password']        
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()
        ac=account['profilepic']
        aid = session['id']
        if profilepic:
            cursor.execute('update users set name=%s, mobile=%s, email=%s, password=%s, profilepic=%s where id=%s', (name,mobile,email,password,profilepic,aid ))
        else:
            profilepic=ac
            cursor.execute('update users set name=%s, mobile=%s, email=%s, password=%s,profilepic=%s where id=%s', (name,mobile,email,password,profilepic,aid ))
        db.connection.commit()
        return redirect(url_for('auth.account', account=account))
    return redirect(url_for('auth.signup'))

@views.route("/contact/", methods=['post','get'])
def contact():
    if request.method == 'POST' and 'email' in request.form and 'message' in request.form :
        email = request.form['email']
        message = request.form['message']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        accounta = cursor.fetchone()
        aid = session['id']
        aname = session['name']
        cursor.execute('INSERT INTO contact VALUES (NULL,% s,% s, % s, % s)', (aid, aname, email, message,))
        db.connection.commit()

    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()    
        return render_template('contact.html', account=account)
    return redirect(url_for('signin'))

@views.route("/about/")
def about():
    if 'loggedin' in session:
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()    
        return render_template('about.html', account=account)
    return redirect(url_for('signin'))
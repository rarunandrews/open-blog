from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app=Flask(__name__,template_folder='templates')

  
  
app.secret_key = 'hello'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'arun55'
app.config['MYSQL_DB'] = 'open-blog'
  
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/signup/" ,methods=['POST', 'GET'])
def signup():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'propic' in request.form and 'mobile' in request.form and 'email' in request.form and 'password' in request.form and 'interest[]' in request.form:
        name = request.form['name']
        username = request.form['username']
        propic = request.form['propic']
        mobile = request.form['mobile']  
        email = request.form['email']
        password = request.form['password']
        interests = request.form['interest[]']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO users VALUES (% s, % s, % s, % s, % s, % s, % s)', (name, username, propic, mobile, email, password, interests, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)

@app.route("/login/" , methods =['GET', 'POST'])
def signin():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route("/post/")
def post():
    return render_template('post.html')

@app.route("/mypost/")
def mypost():
    return render_template('mypost.html')

@app.route("/favorites/")
def favorites():
    return render_template('favorites.html')

@app.route("/authors/")
def authors():
    return render_template('authors.html')

@app.route("/viewpost/")
def viewpost():
    return render_template('viewpost.html')

@app.route("/contact/")
def contact():
    return render_template('contact.html')
if __name__=="__main__":
    app.run(debug=True)
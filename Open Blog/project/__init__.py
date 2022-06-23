from flask import Flask, render_template, request, redirect, url_for, session, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
from PIL import Image
import io

db = MySQL()

def create_app():
    app=Flask(__name__,template_folder='templates')
    save_path = '../static/image'
    app.secret_key = 'hello'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'arun55'
    app.config['MYSQL_DB'] = 'open-blog'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import admin
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    
    return app
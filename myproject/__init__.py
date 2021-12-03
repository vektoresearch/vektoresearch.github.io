import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()

app = Flask(__name__)

# User Database
app.config['SECRET_KEY'] = 'jue878215fd84;wndjhd3829e82!@@#%!^!&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ijonhaklugslva:28854a71f68fb7b90ad53f5eef3914d684fe100a6b6335e4996a4c49db514272@ec2-3-234-85-177.compute-1.amazonaws.com:5432/ded36j5kdcnac3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

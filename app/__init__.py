from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from configparser import ConfigParser
from flask_login import LoginManager
from loadsongs import load_song_lists
from flask_mail import Mail

parser = ConfigParser()
app = Flask(__name__)
songlist_pairs = load_song_lists()

difficulties = []
for i in range(1, 29):
    difficulties.append(i)
difficulties = list(zip(difficulties, difficulties))

parser.read('settings.ini')
app.config['SECRET_KEY'] = parser.get('settings', 'SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = parser.get('sql', 'SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'success'
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = parser.get('email', 'email')
app.config["MAIL_PASSWORD"] = parser.get('email', 'password')
mail = Mail(app)

from app import routes

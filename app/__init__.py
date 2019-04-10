from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from configparser import ConfigParser
from flask_login import LoginManager
from loadsongs import load_song_lists

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

from app import routes

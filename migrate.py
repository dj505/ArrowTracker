from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app/site.db"
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    song = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    lettergrade = db.Column(db.String(3), nullable=False)
    type = db.Column(db.String(7), nullable=True)
    difficulty = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(8), nullable=False)
    stagepass = db.Column(db.String(5), nullable=False)
    ranked = db.Column(db.String(5), nullable=False)
    length = db.Column(db.String(8), nullable=True, default="N/A")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="None")

    def __repr__(self):
        return f"Post('{self.song}', '{self.score}', '{self.lettergrade}', '{self.type}', '{self.difficulty}', '{self.platform}', '{self.stagepass}', '{self.ranked}')"

class WeeklyPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    song = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    lettergrade = db.Column(db.String(3), nullable=False)
    type = db.Column(db.String(7), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(8), nullable=False)
    stagepass = db.Column(db.String(5), nullable=False)
    ranked = db.Column(db.String(5), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="None")

    def __repr__(self):
        return f"Post('{self.song}', '{self.score}', '{self.lettergrade}', '{self.type}', '{self.difficulty}', '{self.platform}', '{self.stagepass}', '{self.ranked}')"

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    skill_lvl = db.Column(db.String(12), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    bracketlink = db.Column(db.String(150), nullable=False)
    image_file = db.Column(db.String(20), default='None', nullable=False)
    contactinfo = db.Column(db.String(150), default='No contact info provided', nullable=True)

    def __repr__(self):
        return f"Tournament('{self.name}', '{self.skill_lvl}, '{self.description}', '{self.bracketlink}', '{self.image_file}', '{self.contactinfo}')"

if __name__ == '__main__':
    manager.run()
    db.drop_all()

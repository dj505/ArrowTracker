from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from app import songlist_pairs, difficulties

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That user already exists!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email has already been taken!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class UpdateAccountForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That user already exists!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email has already been taken!')

class ScoreForm(FlaskForm):
    song = SelectField('Song', coerce=str, choices=songlist_pairs, validators=[DataRequired()])
    lettergrade = SelectField('Letter Grade', coerce=str, choices=(('f', 'F'), ('d', 'D'), ('c', 'C'), ('b', 'B'), ('a', 'A'), ('s', 'S'), ('ss', 'SS'), ('sss', 'SSS')), validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    stagepass = SelectField('Stage Pass', coerce=str, choices=(('1', 'True'), ('0', 'False')), validators=[DataRequired()])
    type = SelectField('Type', coerce=str, choices=(('singles', 'Singles'), ('doubles', 'Doubles')), validators=[DataRequired()])
    difficulty = SelectField('Difficulty', coerce=int, choices=difficulties, validators=[DataRequired()])
    platform = SelectField('Platform', coerce=str, choices=(('pad', 'Pad'), ('keyboard', 'Keyboard')), validators=[DataRequired()])
    ranked = SelectField('Ranked?', coerce=str, choices=(('1', 'Ranked'), ('0', 'Unranked')), validators=[DataRequired()])
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired
from app import songlist_pairs, difficulties

class ScoreForm(FlaskForm):
    song = SelectField('Song', coerce=str, choices=songlist_pairs, validators=[DataRequired()])
    lettergrade = SelectField('Letter Grade', coerce=str, choices=(('f', 'F'), ('d', 'D'), ('c', 'C'), ('b', 'B'), ('a', 'A'), ('s', 'S'), ('ss', 'SS'), ('sss', 'SSS')), validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    stagepass = SelectField('Stage Pass', coerce=str, choices=(('True', 'True'), ('False', 'False')), validators=[DataRequired()])
    type = SelectField('Type', coerce=str, choices=(('singles', 'Singles'), ('doubles', 'Doubles')), validators=[DataRequired()])
    difficulty = SelectField('Difficulty', coerce=int, choices=difficulties, validators=[DataRequired()])
    platform = SelectField('Platform', coerce=str, choices=(('pad', 'Pad'), ('keyboard', 'Keyboard')), validators=[DataRequired()])
    ranked = SelectField('Ranked?', coerce=str, choices=(('True', 'Ranked'), ('False', 'Unranked')), validators=[DataRequired()])
    submit = SubmitField('Submit')

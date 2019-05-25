from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from app import songlist_pairs, difficulties

class ScoreForm(FlaskForm):
    song = SelectField('Song', coerce=str, choices=[tuple(map(lambda x: x.decode('utf-8'), tup)) for tup in songlist_pairs], validators=[DataRequired()])
    lettergrade = SelectField('Letter Grade', coerce=str, choices=(('f', 'F'), ('d', 'D'), ('c', 'C'), ('b', 'B'), ('a', 'A'), ('s', 'S'), ('ss', 'SS'), ('sss', 'SSS')), validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    stagepass = SelectField('Stage Pass', coerce=str, choices=(('True', 'True'), ('False', 'False')), validators=[DataRequired()])
    type = SelectField('Type', coerce=str, choices=(('singles', 'Singles'), ('doubles', 'Doubles'), ('co-op', 'Co-op')), validators=[DataRequired()])
    difficulty = SelectField('Difficulty (Co-Op player count at bottom)', coerce=str, choices=difficulties, validators=[DataRequired()])
    platform = SelectField('Platform', coerce=str, choices=(('pad', 'Pad'), ('keyboard', 'SF2 Keyboard'), ('sf2-pad', 'SF2 Pad')), validators=[DataRequired()])
    ranked = SelectField('Ranked?', coerce=str, choices=(('False', 'Unranked'), ('True', 'Ranked')), validators=[DataRequired()])
    picture = FileField('Verification Score (Optional)', validators=[FileAllowed(['jpg', 'png', 'JPG', 'PNG'])])
    submit = SubmitField('Submit')

class WeeklyForm(FlaskForm):
    lettergrade = SelectField('Letter Grade', coerce=str, choices=(('f', 'F'), ('d', 'D'), ('c', 'C'), ('b', 'B'), ('a', 'A'), ('s', 'S'), ('ss', 'SS'), ('sss', 'SSS')), validators=[DataRequired()])
    score = IntegerField('Score', validators=[DataRequired()])
    stagepass = SelectField('Stage Pass', coerce=str, choices=(('True', 'True'), ('False', 'False')), validators=[DataRequired()])
    type = SelectField('Type', coerce=str, choices=(('singles', 'Singles'), ('doubles', 'Doubles'), ('co-op', 'Co-op')), validators=[DataRequired()])
    difficulty = SelectField('Difficulty', coerce=str, choices=difficulties, validators=[DataRequired()])
    platform = SelectField('Platform', coerce=str, choices=(('pad', 'Pad'), ('keyboard', 'SF2 Keyboard'), ('sf2-pad', 'SF2 Pad')), validators=[DataRequired()])
    ranked = SelectField('Ranked?', coerce=str, choices=(('False', 'Unranked'), ('True', 'Ranked')), validators=[DataRequired()])
    picture = FileField('Verification Score (Optional)', validators=[FileAllowed(['jpg', 'png', 'JPG', 'PNG'])])
    submit = SubmitField('Submit')

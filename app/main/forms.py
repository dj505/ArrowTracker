from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired
from app import songlist_pairs

class SearchForm(FlaskForm):
    filters = (
    ("ranked-score", "Verified, Score"),
    ("ranked-difficulty", "Verified, Difficulty"),
    ("unranked-score", "Unverified, Score"),
    ("unranked-difficulty", "Unverified, Difficulty"))
    song = SelectField('Song', coerce=str, choices=songlist_pairs)
    filters = SelectField('Filter', coerce=str, choices=filters)
    userfilter = StringField('User [OPTIONAL]')
    submit = SubmitField('Search')

class TournamentForm(FlaskForm):
    name = StringField('Tournament Name', validators=[DataRequired()])
    description = StringField('Description')
    bracketlink = StringField('Bracket Link (Challonge or other)')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Submit')
    contactinfo = StringField('Contact Information')
    skill_lvl = SelectField('Skill Level', coerce=str, choices=(('Beginner', 'Beginner'),
                                                                ('Intermediate', 'Intermediate'),
                                                                ('Advanced', 'Advanced')),
                                                                validators=[DataRequired()])

class TournamentEditForm(FlaskForm):
    name = StringField('Tournament Name', validators=[DataRequired()])
    description = StringField('Description')
    bracketlink = StringField('Bracket Link (Challonge or other)')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Submit')
    contactinfo = StringField('Contact Information')
    skill_lvl = SelectField('Skill Level', coerce=str, choices=(('Beginner', 'Beginner'),
                                                                ('Intermediate', 'Intermediate'),
                                                                ('Advanced', 'Advanced')),
                                                                validators=[DataRequired()])

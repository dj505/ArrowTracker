from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired
from app import songlist_pairs

class SearchForm(FlaskForm):
    filters = (
    ("ranked-score", "Ranked, Score"),
    ("ranked-difficulty", "Ranked, Difficulty"),
    ("unranked-score", "Unranked, Score"),
    ("unranked-difficulty", "Unranked, Difficulty"))
    song = SelectField('Song', coerce=str, choices=songlist_pairs)
    filters = SelectField('Filter', coerce=str, choices=filters)
    userfilter = StringField('User [OPTIONAL]')
    submit = SubmitField('Submit')

class TournamentForm(FlaskForm):
    name = StringField('Tournament Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')
    skill_lvl = SelectField('Skill Level', coerce=str, choices=(('Beginner', 'Beginner'),
                                                                ('Intermediate', 'Intermediate'),
                                                                ('Advanced', 'Advanced')),
                                                                validators=[DataRequired()])

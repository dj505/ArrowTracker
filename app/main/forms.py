from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from app import songlist_pairs

class SearchForm(FlaskForm):
    filters = (
    ("ranked-score", "Ranked, Score"),
    ("ranked-difficulty", "Ranked, Difficulty")
    ("unranked-score", "Ranked, Score"),
    ("unranked-difficulty", "Ranked, Difficulty")
    song = SelectField('Song', coerce=str, choices=songlist_pairs)
    filters = SelectField('Filter', coerce=str, choices=filters)
    userfilter = StringField('User [OPTIONAL]')
    submit = SubmitField('Submit')

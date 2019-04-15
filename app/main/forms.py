from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from app import songlist_pairs

class SearchForm(FlaskForm):
    filters = (
    ("score", "Score"),
    ("difficulty", "Difficulty"),
    ("stagepass", "Stage Pass"),
    ("stagebreak", "Stage Break"),
    ("ranked", "Ranked"),
    ("unranked", "Unranked"),
    ("pad", "Pad"),
    ("keyboard", "Keyboard")
    )
    song = SelectField('Song', coerce=str, choices=songlist_pairs)
    filters = SelectField('Filter', coerce=str, choices=filters)
    submit = SubmitField('Submit')

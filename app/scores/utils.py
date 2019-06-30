from PIL import Image
import os
import secrets
from flask import current_app
from flask_login import current_user
from app import db, logging, raw_songdata
from app.models import Post, User

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/score_screenshots', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn

def return_completion(user, difficulty):
    user = user = User.query.filter_by(username=user).first_or_404()
    allscores = Post.query.filter_by(author=user).all()
    data = {}
    passinggrades = ['a','s','ss','sss']
    completed = 0
    if difficulty == "singles":
        data['singles'] = {}
        for i in range(25):
            diff = i+1
            for score in allscores:
                if score.difficulty == diff and score.lettergrade in passinggrades:
                    completed += 1
            data['singles'][diff] = completed
    return(data)

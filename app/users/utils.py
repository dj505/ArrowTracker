import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail
from app.models import User
import json

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Arrow Tracker: Password Reset Request', sender='jaydenb505@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, please visit:
{url_for('users.reset_token', token=token, _external=True)}

If you didn't request this reset, please ignore this email - the unique token used for the reset will expire in 30 minutes.
No changes will be made without using the above link.
'''
    mail.send(msg)

def update_rivals(list, id, currentuser):
    users_not_found = []
    valid_users = []
    for rival in list:
        user = User.query.filter_by(id)
        if not user:
            users_not_found.append(rival)
        elif id != currentuser:
            valid_users.append(rival)
    json_path = os.path.join(current_app.root_path, 'static/rivals', str(id) + '.json')
    if not os.path.isfile(json_path):
        with open(json_path, 'w') as f:
            f.write('{}')
    with open(json_path) as f:
        rivallist = json.load(f)
    rivallist['rivals'] = valid_users
    with open(json_path, 'w') as f:
        json.dump(rivallist, f)
    return

def get_rivals(id):
    json_path = os.path.join(current_app.root_path, 'static/rivals', str(id) + '.json')
    if not os.path.isfile(json_path):
        return ["No rivals"]
    else:
        with open(json_path) as f:
            rivallist = json.load(f)
        return rivallist

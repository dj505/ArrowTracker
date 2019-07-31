from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt, raw_songdata
from app.models import User, Post
from app.users.forms import (RegisterForm, LoginForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm)
from app.users.utils import save_picture, send_reset_email
import json

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Hello, {form.username.data}! You may now log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()
        user.email = user.email.lower()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful! Welcome, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful!', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/dashboard/updatepfp', methods=["POST"])
@login_required
def update_pfp():
    if request.method == 'POST':
        current_user.image_file = request.form['submit_button']
        db.session.commit()
        flash('Profile image updated!', 'success')
    return redirect(url_for('users.dashboard'))

@users.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.favsong = form.favsong.data
        db.session.commit()
        flash('Account details updated!', 'success')
        return redirect(url_for('users.dashboard'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.favsong.data = current_user.favsong
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("dashboard.html", title="Dashboard", image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    scores = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page)
    difficulty = None
    for score in scores.items:
        difficulty = str(score.difficulty)
    return render_template("user_posts.html", scores=scores, difficulty=difficulty, user=user, songdata=raw_songdata)

@users.route("/userpage/<string:username>")
def user_page(username):
    user = User.query.filter_by(username=username).first_or_404()
    scores = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).limit(5).all()
    return render_template("user_profile.html", scores=scores, user=user)

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect_for(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('A reset email has been reset with instructions! Make sure you check your spam folder!', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect_for(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid or expired!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'You password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route("/members")
def members():
    users = User.query.all()
    total = db.engine.execute('select count(*) from User').scalar()
    return render_template('users.html', users=users, total=total)

@users.route("/members/supporters")
def supporters():
    with open('supporters.json', 'r') as f:
        supporters = json.load(f)
    total = len(supporters)
    return render_template('supporters.html', supporters=supporters, total=total)

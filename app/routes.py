from flask import Flask, render_template, flash, redirect, url_for, request
from app import app, db, bcrypt
from app.forms import RegisterForm, LoginForm, UpdateAccountForm, ScoreForm
from app.models import User, Post
import secrets
import os
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
    scores = Post.query.all()
    for score in scores:
        difficulty = str(score.difficulty)
    return render_template("home.html", scores=scores, difficulty=difficulty)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Hello, {form.username.data}! You may now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful! Welcome, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template("about.html")

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account details updated!', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("dashboard.html", title="Dashboard", image_file=image_file, form=form)

@app.route('/post/new_score', methods=["GET", "POST"])
@login_required
def new_score():
    form = ScoreForm()
    if form.validate_on_submit():
        post = Post(song = form.song.data, score = form.score.data, lettergrade = form.lettergrade.data, type = form.type.data, difficulty = form.difficulty.data, platform = form.platform.data, stagepass = form.stagepass.data, ranked = form.ranked.data, author = current_user)
        db.session.add(post)
        print(post)
        db.session.commit()
        flash('Score has been submitted!', 'success')
        return redirect(url_for('home'))
    return render_template("new_score.html", title="New Score", form=form)

@app.route('/post/<int:score_id>')
def score(score_id):
    score = Post.query.get_or_404(score_id)
    difficulty = str(score.difficulty)
    return render_template('score.html', title=score.song, score=score, difficulty=difficulty)

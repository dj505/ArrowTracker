from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from app import db, logging, raw_songdata
from app.models import Post, WeeklyPost
from app.scores.forms import ScoreForm, WeeklyForm
from app.scores.utils import save_picture, allowed_file
import os
from weekly import get_current_weekly, randomize_weekly

scores = Blueprint('scores', __name__)

@scores.route('/post/new_score', methods=["GET", "POST"])
@login_required
def new_score():
    form = ScoreForm()
    if form.validate_on_submit():
        difficulty = request.form.get('diffDrop')
        try:
            file = request.files['file']
        except:
            picture_file = "None"
            file = None
            flash('No file uploaded', 'info')
        if file != None:
            if file.filename == '':
                flash('No file selected!', 'error')
                picture_file = "None"
                return redirect(request.url)
            if file and allowed_file(file.filename):
                picture_file = save_picture(file)
                flash('File uploaded successfully!', 'success')
            elif file and not allowed_file(file.filename):
                picture_file = "None"
                flash('You can\'t upload that!', 'error')
        post = Post(song = form.song.data, score = form.score.data, lettergrade = form.lettergrade.data, difficulty = difficulty, platform = form.platform.data, stagepass = form.stagepass.data, ranked = form.ranked.data, length = form.length.data, author = current_user, image_file = picture_file)
        db.session.add(post)
        db.session.commit()
        flash('Score has been submitted!', 'success')
        return redirect(url_for('main.home'))
    return render_template("new_score.html", title="New Score", form=form, songdata=raw_songdata)

@scores.route('/post/<int:score_id>')
def score(score_id):
    bluegrades = ['a', 'b', 'c', 'd']
    goldgrades = ['s', 'ss', 'sss']
    redgrades = ['f']
    score = Post.query.get_or_404(score_id)
    return render_template('score.html', score=score, songdata=raw_songdata, bluegrades=bluegrades, goldgrades=goldgrades, redgrades=redgrades)

@scores.route('/post/<int:score_id>/delete', methods=["POST"])
def delete_score(score_id):
    score = Post.query.get_or_404(score_id)
    if score.author == current_user or current_user.id == 1:
        if score.image_file != "None":
            try:
                os.remove(os.path.join(current_app.root_path, 'static/score_screenshots', score.image_file))
            except:
                flash('Score screenshot couldn\'t be found.', 'info')
        db.session.delete(score)
        db.session.commit()
        flash('Your score has been deleted!', 'success')
        return redirect(url_for('main.home'))
    elif score.author != current_user:
        abort(403)

@scores.route('/challenge/weekly/<int:score_id>/delete', methods=["POST"])
def delete_weekly(score_id):
    score = WeeklyPost.query.get_or_404(score_id)
    if score.author != current_user:
        abort(403)
    if score.image_file != "None":
        os.remove(os.path.join(current_app.root_path, 'static/score_screenshots', score.image_file))
    db.session.delete(score)
    db.session.commit()
    flash('Your score has been deleted!', 'success')
    return redirect(url_for('main.home'))

@scores.route('/challenge/weekly', methods=["GET", "POST"])
@login_required
def weekly():
    current_weekly = get_current_weekly()
    form = WeeklyForm()
    if form.validate_on_submit():
        try:
            file = request.files['file']
        except:
            flash('Score not submitted. Verification screenshot required.')
            return redirect(url_for('main.home'))
        if file != None:
            if file.filename == '':
                flash('Score not submitted. Verification screenshot required.')
                return redirect(url_for('main.home'))
            if file and allowed_file(file.filename):
                picture_file = save_picture(file)
                flash('File uploaded successfully!', 'success')
                post = WeeklyPost(song = current_weekly, score = form.score.data, lettergrade = form.lettergrade.data, type = form.type.data, difficulty = form.difficulty.data, platform = form.platform.data, stagepass = form.stagepass.data, ranked = form.ranked.data, author = current_user, image_file = picture_file)
                db.session.add(post)
                db.session.commit()
            elif file and not allowed_file(file.filename):
                    flash('Score not submitted. Verification screenshot required.')
                    return redirect(url_for('main.home'))
        flash('Score has been submitted!', 'success')
        return redirect(url_for('scores.weekly'))
    ldb = WeeklyPost.query.order_by(WeeklyPost.score.desc()).all()
    return render_template('weekly.html', current_weekly=current_weekly, form=form, ldb=ldb)

@scores.route('/challenge/weekly/<int:score_id>')
def weeklyscore(score_id):
    bluegrades = ['a', 'b', 'c', 'd']
    goldgrades = ['s', 'ss', 'sss']
    redgrades = ['f']
    score = WeeklyPost.query.get_or_404(score_id)
    return render_template('weeklyscore.html', score=score, bluegrades=bluegrades, goldgrades=goldgrades, redgrades=redgrades)

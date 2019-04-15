from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.scores.forms import ScoreForm

scores = Blueprint('scores', __name__)

@scores.route('/post/new_score', methods=["GET", "POST"])
@login_required
def new_score():
    form = ScoreForm()
    if form.validate_on_submit():
        post = Post(song = form.song.data, score = form.score.data, lettergrade = form.lettergrade.data, type = form.type.data, difficulty = form.difficulty.data, platform = form.platform.data, stagepass = form.stagepass.data, ranked = form.ranked.data, author = current_user)
        db.session.add(post)
        print(post)
        db.session.commit()
        flash('Score has been submitted!', 'success')
        return redirect(url_for('main.home'))
    return render_template("new_score.html", title="New Score", form=form)

@scores.route('/post/<int:score_id>')
def score(score_id):
    score = Post.query.get_or_404(score_id)
    difficulty = str(score.difficulty)
    return render_template('score.html', title=score.song, score=score, difficulty=difficulty)

@scores.route('/post/<int:score_id>/delete', methods=["POST"])
def delete_score(score_id):
    score = Post.query.get_or_404(score_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your score has been deleted!', 'success')
    return redirect(url_for('main.home'))

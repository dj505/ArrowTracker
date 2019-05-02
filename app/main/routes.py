from flask import render_template, request, Blueprint, current_app, session, redirect, url_for, flash, Markup
from flask_login import current_user, login_required
from app.main.forms import SearchForm, TournamentForm, TournamentEditForm
from app.models import Post, Tournament
from app import songlist_pairs, difficulties, db
from sqlalchemy import desc, or_
from app.config import GetChangelog

main = Blueprint('main', __name__)

@main.route("/")
def home():
    flashmsg = Markup(f'New update! 2019-04-29 | <a href="/changelog">View Changelog</a>')
    flash(flashmsg, 'secondary')
    page = request.args.get('page', 1, type=int)
    scores = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=15, page=page)
    return render_template("home.html", scores=scores)

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)
    if request.method == "POST" and form.validate():
        session['song_search'] = form.song.data
        session['filters'] = form.filters.data
        session['userfilter'] = form.userfilter.data
        return redirect(url_for('main.search_results'))
    return render_template("search.html", songlist=songlist_pairs, form=form)

@main.route('/search_results/')
def search_results():
    if session['filters'] == 'ranked-score':
        results = Post.query.filter(Post.song == session['song_search'], Post.platform == 'pad', Post.image_file != "None").order_by(desc(Post.score))
    elif session['filters'] == 'unranked-score':
        results = Post.query.filter(Post.song == session['song_search'], or_(Post.platform == 'keyboard', Post.platform == 'sf2-pad')).order_by(desc(Post.score))
    if session['filters'] == 'ranked-difficulty':
        results = Post.query.filter(Post.song == session['song_search'], Post.platform == 'pad', Post.image_file != "None").order_by(desc(Post.difficulty))
    elif session['filters'] == 'unranked-difficulty':
        results = Post.query.filter(Post.song == session['song_search'], or_(Post.platform == 'keyboard', Post.platform == 'sf2-pad')).order_by(desc(Post.difficulty))
    return render_template("search_results.html", results=results)

@main.route('/changelog')
def changelog():
    return render_template("changelog.html", changelog=GetChangelog())

@main.route('/resources')
def resources():
    return render_template("resources.html", changelog=GetChangelog())

@main.route('/howto')
def howto():
    return render_template("howto.html", changelog=GetChangelog())

@main.route("/tournaments/view")
@login_required
def tournaments():
    page = request.args.get('page', 1, type=int)
    tournaments = Tournament.query.order_by(Tournament.date_posted.desc()).paginate(per_page=16, page=page)
    return render_template("tournaments.html", tournaments=tournaments)

@main.route("/tournaments/create", methods=["GET", "POST"])
@login_required
def create_tournament():
    form = TournamentForm(request.form)
    if form.validate_on_submit():
        tournament = Tournament(name = form.name.data, skill_lvl = form.skill_lvl.data, description = form.description.data, user_id = current_user.id)
        db.session.add(tournament)
        db.session.commit()
        flash('Tournament created!', 'success')
        return redirect(url_for('main.tournaments'))
    return render_template("create_tournament.html", form=form)

@main.route("/tournaments/<int:tournament_id>/edit", methods=["GET", "POST"])
@login_required
def edit_tournament(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    form = TournamentEditForm()
    if form.validate_on_submit():
        tournament.name = form.name.data
        tournament.description = form.description.data
        tournament.skill_lvl = form.skill_lvl.data
        db.session.commit()
        flash('Tournament info updated!', 'success')
        return redirect(url_for('main.tournaments'))
    form.name.data = tournament.name
    form.description.data = tournament.description
    form.skill_lvl.data = tournament.skill_lvl
    if tournament.user_id != current_user.id:
        abort(403)
    return render_template('edit_tournament.html', tournament=tournament, form=form)

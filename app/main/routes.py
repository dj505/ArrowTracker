from flask import render_template, request, Blueprint, current_app, session, redirect, url_for, flash, Markup
from flask_login import current_user, login_required
from app.main.forms import SearchForm, TournamentForm, TournamentEditForm
from app.models import Post, Tournament
from app import songlist_pairs, difficulties, db, raw_songdata
from sqlalchemy import desc, or_
from app.config import GetChangelog
from app.main.utils import save_picture, allowed_file
import os

# We can define all of the "@main" decorators below as a "blueprint" that
# allows us to easily call or redirect the user to any of them from anywhere.
main = Blueprint('main', __name__)

# The route for the main homepage.
@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    scores = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=15, page=page)
    total = db.engine.execute('select count(*) from Post').scalar()
    return render_template("home.html", scores=scores, total=total, songdata=raw_songdata)

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/search', methods=['GET', 'POST']) # The methods 'GET' and 'POST' tell this route that
def search():                                   # we can both request and send data to/from the page.
    form = SearchForm(request.form)
    if request.method == "POST" and form.validate():
        session['song_search'] = form.song.data
        session['filters'] = form.filters.data
        session['length'] = form.length.data
        return redirect(url_for('main.search_results'))
    return render_template("search.html", form=form)

@main.route('/search_results/')
def search_results():
    if session['filters'] == 'old':
        results = Post.query.filter(Post.song.like('%' + session['song_search'] + '%'), Post.length == None)
    if session['filters'] == 'all':
        results = Post.query.filter(Post.song.like('%' + session['song_search'] + '%'), Post.length == session['length'])
    elif session['filters'] == 'verified':
        results = Post.query.filter(Post.song.like('%' + session['song_search'] + '%'), Post.length == session['length'], Post.platform == 'pad', )
    elif session['filters'] == 'unverified':
        results = Post.query.filter(Post.song.like('%' + session['song_search'] + '%'), Post.length == session['length'], or_(Post.platform == 'keyboard', Post.platform == 'sf2-pad'))
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
    picture_file = "None"
    if form.validate_on_submit():
        try:
            file = request.files['file']
        except:
            file = None
            flash('No file uploaded', 'info')
        if file != None:
            if file.filename == '':
                flash('No file selected!', 'error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                picture_file = save_picture(file)
                flash('File uploaded successfully!', 'success')
            elif file and not allowed_file(file.filename):
                flash('You can\'t upload that!', 'error')
        tournament = Tournament(name = form.name.data, skill_lvl = form.skill_lvl.data, description = form.description.data, bracketlink = form.bracketlink.data, image_file = picture_file, contactinfo = form.contactinfo.data, user_id = current_user.id)
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
        tournament.image_file = picture_file
        tournament.name = form.name.data
        tournament.description = form.description.data
        tournament.skill_lvl = form.skill_lvl.data
        tournament.bracketlink = form.bracketlink.data
        tournament.contactingo = form.contactinfo.data
        db.session.commit()
        flash('Tournament info updated!', 'success')
        return redirect(url_for('main.tournaments'))
    form.name.data = tournament.name
    form.description.data = tournament.description
    form.skill_lvl.data = tournament.skill_lvl
    form.bracketlink.data = tournament.bracketlink
    form.contactinfo.data = tournament.contactinfo
    if tournament.user_id != current_user.id:
        abort(403)
    return render_template('edit_tournament.html', tournament=tournament, form=form)

@main.route('/tournament/<int:tournament_id>')
def tournament(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    return render_template('tournament.html', tournament=tournament)

@main.route('/tournament/<int:tournament_id>/delete', methods=["POST"])
def delete_tournament(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    if tournament.user_id != current_user.id:
        abort(403)
    if tournament.image_file != "None":
        os.remove(os.path.join(current_app.root_path, 'static/tournament_pics', tournament.image_file))
    db.session.delete(tournament)
    db.session.commit()
    flash('Your tournament has been deleted!', 'success')
    return redirect(url_for('main.tournaments'))

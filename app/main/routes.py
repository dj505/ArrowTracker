from flask import render_template, request, Blueprint, current_app, session, redirect, url_for, flash, Markup
from app.main.forms import SearchForm
from app.models import Post
from app import songlist_pairs, difficulties
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

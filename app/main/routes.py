from flask import render_template, request, Blueprint, current_app, session, redirect, url_for
from app.main.forms import SearchForm
from app.models import Post
from app import songlist_pairs, difficulties
from sqlalchemy import desc

main = Blueprint('main', __name__)

@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    scores = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
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
    if session['filters'] == 'score':
        results = Post.query.filter(Post.song == session['song_search']).order_by(desc(Post.score))
    elif session['filters'] == 'difficulty':
        results = Post.query.filter(Post.song == session['song_search']).order_by(desc(Post.difficulty))
    return render_template("search_results.html", results=results)

from flask import render_template, request, Blueprint, current_app, session, redirect, url_for
from app.main.forms import SearchForm
from app.models import Post
from app import songlist_pairs, difficulties

main = Blueprint('main', __name__)

@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    scores = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    for score in scores.items:
        difficulty = str(score.difficulty)
    return render_template("home.html", scores=scores, difficulty=difficulty)

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)
    if request.method == "POST" and form.validate():
        session['song_search'] = form.song.data
        session['filters'] = form.filters.data
        return redirect(url_for('main.search_results'))
    return render_template("search.html", songlist=songlist_pairs, form=form)

@main.route('/search_results/')
def search_results():
    results = Post.query.filter(Post.song == session['song_search'])
    results = [u.__dict__ for u in results]
    for result in results:
        result['lvl_prefix'] = result['type'][0].upper()
        result['difficulty'] = str(result['difficulty'])
        result['lettergrade'] = result['lettergrade'].upper()
        result['platform'] = result['platform'].capitalize()
        if result['stagepass'] == "True":
            result['stagepass'] = "Pass"
        elif result['stagepass'] == "False":
            result['stagepass'] = "Break"
        if result['ranked'] == "False":
            result['ranked'] = "Unranked"
        elif result['ranked'] == "True":
            result['ranked'] = "Ranked"
        else:
            result['ranked'] = "Unknown"
    return render_template("search_results.html", results=results)

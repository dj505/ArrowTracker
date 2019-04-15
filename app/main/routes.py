from flask import render_template, request, Blueprint, current_app
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
        return redirect(url_for('search_results'))
    return render_template("search.html", songlist=songlist_pairs, form=form)

@main.route('/search_results/')
def search_results():
    current_app.logger.info(session['song_search'])
    song = session['song_search']
    filter = session['filters']
    if filter == "score" or filter == "difficulty":
        query = 'SELECT * FROM piu WHERE song = "{}"'.format(song)
    if filter == "stagepass":
        query = 'SELECT * FROM piu WHERE song = "{}" AND stagepass = 1'.format(song)
    if filter == "stagebreak":
        query = 'SELECT * FROM piu WHERE song = "{}" AND stagepass = 0'.format(song)
    if filter == "ranked":
        query = 'SELECT * FROM piu WHERE song = "{}" AND ranked = 1'.format(song)
    if filter == "unranked":
        query = 'SELECT * FROM piu WHERE song = "{}" AND ranked = 0'.format(song)
    if filter == "pad":
        query = 'SELECT * FROM piu WHERE song = "{}" AND platform = "pad"'.format(song)
    if filter == "keyboard":
        query = 'SELECT * FROM piu WHERE song = "{}" AND platform = "keyboard"'.format(song)
    cur = mysql.connection.cursor()
    result = cur.execute(query)
    results = cur.fetchall()
    results = list(results)
    if filter != "difficulty":
        results = sorted(results, key=lambda tup: tup['score'], reverse=True)
    else:
        results = sorted(results, key=lambda tup: int(tup['difficulty']), reverse=True)
    if len(results) > 0:
        for result in results:
            result['lvl_prefix'] = result['type'][0].upper()
            result['difficulty'] = str(result['difficulty'])
            result['lettergrade'] = result['lettergrade'].upper()
            result['platform'] = result['platform'].capitalize()
            if result['stagepass'] == 1:
                result['stagepass'] = "Yes"
            elif result['stagepass'] == 0:
                result['stagepass'] = "No"
            if result['ranked'] == 0:
                result['ranked'] = "Unranked"
            elif result['ranked'] == 1:
                result['ranked'] = "Ranked"
            else:
                result['ranked'] = "Unknown"
    return render_template("search_results.html", results=results)

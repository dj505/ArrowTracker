from flask import render_template, request, Blueprint, current_app
from app.models import Post

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

from flask import (
    Blueprint, render_template
)

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/')
@bp.route('/index')
def index():
    return render_template("home.html")


@bp.route('/profile')
def profile():
    return render_template("profile.html")


@bp.route('/start')
def start():
    return render_template("start_auth.html")

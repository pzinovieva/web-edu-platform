from flask import (
    Blueprint, render_template
)

bp = Blueprint('parents', __name__, url_prefix='/parents')


@bp.route('/how_to')
def how_to_learn():
    return render_template("how_to_parents.html")


@bp.route('/recommendation')
def recommendation():
    return render_template("recommendation.html")

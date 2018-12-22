from flask import Blueprint, render_template
from urlhunter.models import User

bp = Blueprint('user', __name__)


@bp.route('/<string:username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/index.html', user=user)

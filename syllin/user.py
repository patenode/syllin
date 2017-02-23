from flask import Blueprint, render_template
from flask import redirect
from flask import url_for
from models import User

views = Blueprint(name='user',
                  import_name=__name__,
                  template_folder='templates/user',
                  url_prefix='/u')


# TODO: Instead of using a mock class, get actual ID from user session
class CU:
    id = 4
current_user = CU()

def get_user(id):
    return User.query.filter_by(id=id).first_or_404()

@views.route('/', defaults=dict(user_id=current_user.id))
def my_profile(user_id):
    return redirect(url_for('user.profile', user_id=user_id))

@views.route('/<user_id>/')
def profile(user_id):
    return render_template('user/profile.html', user=get_user(user_id))

@views.route('/<user_id>/library')
def library(user_id):
    return render_template('user/library.html', user=get_user(user_id))

@views.route('/<user_id>/statistics')
def statistics(user_id):
    return render_template('user/statistics.html', user=get_user(user_id))
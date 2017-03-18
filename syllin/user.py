from flask import Blueprint, render_template
from flask import redirect
from flask import url_for

from syllin.models import User, Song

views = Blueprint(name='user',
                  import_name=__name__,
                  template_folder='templates/user',
                  url_prefix='/u')


def get_user(id):
    return User.query.filter_by(id=id).first_or_404()


# TODO: Instead of using a mock data value, get actual ID from user session (login)
class CU:
    def __init__(self, future_id):
        self._id = future_id
        self.usr_obj = None

    def __getattr__(self, item):
        if not self.usr_obj:
            self.usr_obj = get_user(self._id)
        return getattr(self.usr_obj, item)


current_user = CU(4)


@views.route('/')
def my_profile():
    return profile(current_user.id)


@views.route('/<user_id>/')
def profile(user_id):
    return render_template('user/profile.html', user=get_user(user_id))


def get_sorting_options():
    return [
        ['Newest', True],
        ['Most Popular', False],
        ['Album', False],
        ['Song', False],
        ['Artist', False]
    ]


@views.route('/library')
def my_library():
    return library(current_user.id)


# TODO: Replace with actual song query
def get_songs():
    return Song.query.all()


@views.route('/<user_id>/library')
def library(user_id):
    return render_template('user/library.html',
                           user=get_user(user_id),
                           sorting_options=get_sorting_options(),
                           songs=get_songs())


@views.route('/stats')
def my_stats():
    return stats(current_user.id)


@views.route('/<user_id>/stats')
def stats(user_id):
    return render_template('user/stats.html', user=get_user(user_id))

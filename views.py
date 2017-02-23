from flask import render_template

import album
import song
import user
from app import application
from user import current_user
from models import Song

application.register_blueprint(user.views)
application.register_blueprint(album.views)
application.register_blueprint(song.views)


@application.route('/')
def index():
    q = Song.query.all()
    return render_template('discovery.html', user_id=current_user.id, songs=q)


@application.route('/<tag>')
def link(tag):
    return f"Processing the tag '{tag}'..."


@application.route('/settings')
def settings():
    return render_template('settings.html', user_id=current_user.id)

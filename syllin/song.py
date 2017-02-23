from flask import Blueprint, render_template
from syllin.models import Song

views = Blueprint(name='song',
                  import_name=__name__,
                  template_folder='templates/song',
                  url_prefix='/s')


@views.route('/')
def discovery():
    return render_template('song/discovery.html')


@views.route('/<int:song_id>')
def view(song_id):
    s = Song.query.filter_by(id=song_id).first_or_404()
    return render_template('song/view.html', song=s)


@views.route('/<int:song_id>/buy', methods=['GET', 'POST'])
def buy(song_id):
    return render_template('song/buy.html', song_id=song_id)


@views.route('/<int:song_id>/thanks')
def purchased(song_id):
    return render_template('song/thanks.html', song_id=song_id)

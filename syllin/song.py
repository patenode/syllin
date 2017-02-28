from flask import Blueprint, render_template

from syllin.models import Song

views = Blueprint(name='song',
                  import_name=__name__,
                  template_folder='templates/song',
                  url_prefix='/s')


def get_song(id):
    return Song.query.filter_by(id=id).first_or_404()

@views.route('/<int:song_id>')
def view(song_id):
    return render_template('song/view.html', song=get_song(song_id))


@views.route('/<int:song_id>/buy', methods=['GET', 'POST'])
def buy(song_id):
    return render_template('song/buy.html', song=get_song(song_id))


@views.route('/<int:song_id>/thanks')
def purchased(song_id):
    return render_template('song/thanks.html', song=get_song(song_id))

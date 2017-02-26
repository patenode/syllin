from flask import Blueprint, render_template

from syllin.models import Album

views = Blueprint(name='album',
                  import_name=__name__,
                  template_folder='templates/album',
                  url_prefix='/a')


def get_album(id):
    return Album.query.filter_by(id=id).first_or_404()


@views.route('/<int:album_id>')
def view(album_id):
    return render_template('album/view.html', album=get_album(album_id))


@views.route('/<int:album_id>/buy', methods=['GET', 'POST'])
def buy(album_id):
    return render_template('album/buy.html', album=get_album(album_id))


@views.route('/<int:album_id>/thanks')
def purchased(album_id):
    return render_template('album/thanks.html', album=get_album(album_id))

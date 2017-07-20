from flask import Blueprint, render_template, current_app, request
from flask_security.core import current_user
from syllin.models import Song, SongLink
from syllin.forms.forms import SongPurchaseForm
from syllin.database_methods import buySong, user_owns_song


views = Blueprint(name='song',
				  import_name=__name__,
				  template_folder='templates/song',
				  url_prefix='/s')


def get_song(id):
	return Song.query.filter_by(id=id).first_or_404()

@views.route('/<int:song_id>', methods=['GET', 'POST'])
def view(song_id):
	form = SongPurchaseForm()
	domain_url = request.url_root

	link = None
	if current_user.is_authenticated and user_owns_song(current_user, song_id=song_id):
		link = SongLink.query.filter(SongLink.song_id==song_id).filter(SongLink.referrer_id==current_user.id).first().key

	if form.validate_on_submit():
		if not current_user.is_authenticated:
			return current_app.login_manager.unauthorized()
		buySong(song_id=song_id, buyer_id=current_user.id, seller_id=2)

	return render_template('song/view.html', song=get_song(song_id), form=form, link=link, domain_url=domain_url[:-1])


# I'm using view to post purchases
@views.route('/<int:song_id>/buy', methods=['GET', 'POST'])
def buy(song_id):
	return render_template('song/buy.html', song=get_song(song_id))


@views.route('/<int:song_id>/thanks')
def purchased(song_id):
	return render_template('song/thanks.html', song=get_song(song_id))

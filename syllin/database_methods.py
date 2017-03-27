from syllin.db_model import db
from syllin.models import User, Role, Purchase, Song, Album, SongLink
from syllin.random_string import get_random_string

def buySong(song_id, buyer_id, seller_id):
    song = Song.query.get(song_id)
    buyer = User.query.get(buyer_id)
    seller = User.query.get(seller_id)

    purchase = Purchase(buyer=buyer, seller=seller, song=song)

    # The buyer gets a song link
    song_link = SongLink(song=song, referrer=buyer, key=get_random_string(40))

    db.session.add(purchase)
    db.session.add(song_link)
    db.session.commit()


def addSongs(l_song_titles, album):
    for song_title in l_song_titles:
        db.session.add(Song(title=song_title, album=album))
    db.session.commit()


def roles():
    if not Role.query.first():
        user_datastore.create_role(name="artist")
        user_datastore.create_role(name='admin')
    
    if not User.query.first():
        user_datastore.create_user(email='admin@example.com',
                                   password=encrypt_password('adminpassword'), roles=['admin'])

def setupDatabaseForDebug():
    
    
    roles()

    if not Album.query.first():
        db.session.add(Album(title="The Pink Album", artist=User.query.get(2)))


    if len(Song.query.all()) < 3:
        addSongs(["Frumpy r", "!!Curmudgeon", "Fuck ^^^^^^^me briskly"], Album.query.get(1))
        buySong(1, 2, 1)

    if not SongLink.query.first():
        song_link = SongLink(song_id=4, referrer_id=2, key="idk")
        db.session.add(song_link)
    db.session.commit()

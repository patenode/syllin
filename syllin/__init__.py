from flask_security import Security, SQLAlchemyUserDatastore

from syllin import views
from syllin.app import application
from syllin.db_model import db
from syllin.models import User, Role, Purchase, Song, Album  

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(application, user_datastore)
db.init_app(application)


def addSongs(l_song_titles, album):
    for song_title in l_song_titles:
        db.session.add(Song(title=song_title, album=album))
    db.session.commit()


def buySong(song_id, buyer_id, seller_id):
    song = Song.query.get(song_id)
    buyer = User.query.get(buyer_id)
    seller = User.query.get(seller_id)

    purchase = Purchase(buyer=buyer, seller=seller, song=song)

    db.session.add(purchase)
    db.session.commit()


def roles():
    if not Role.query.first():
        user_datastore.create_role(name='admin')
        user_datastore.create_user(email='admin@example.com',
                                   password='adminpassword', roles=['admin'])


def setupDatabaseForDebug():

    if not User.query.first():
        roles()
        user_datastore.create_user(email='matt@nobien.net', password='password')
        user_datastore.create_user(email='joosh@nobien.net', password='password')


    if not Album.query.first():
        db.session.add(Album(title="The Pink Album", artist=User.query.get(2)))


    if len(Song.query.all()) < 10:
        addSongs(["Frumpy r", "!!Curmudgeon", "Fuck ^^^^^^^me briskly"], Album.query.get(1))
        buySong(1, 2, 1)

    db.session.commit()


@application.before_first_request
def initDB():
    db.create_all()
    setupDatabaseForDebug()
    db.session.commit()

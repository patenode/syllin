from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password
from syllin import views
from syllin.security import user_datastore, security
from syllin.app import application
from syllin.db_model import db
from syllin.models import User, Role, Purchase, Song, Album  
from flask_mail import Mail


application.config.update(dict(
    DEBUG = True,
    # email server
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'syllin.mail',
    MAIL_PASSWORD = 'Syllinpassword',

    # administrator list
    ADMINS = ['my_username@gmail.com']
))

mail = Mail()

mail.init_app(application)
# Setup Flask-Security

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
        user_datastore.create_role(name="artist")
        user_datastore.create_role(name='admin')
    

    user_datastore.create_user(email='admin@example.com',
                                   password=encrypt_password('adminpassword'), roles=['admin'])


def setupDatabaseForDebug():
    
    
    roles()

    if not Album.query.first():
        db.session.add(Album(title="The Pink Album", artist=User.query.get(2)))


    if len(Song.query.all()) < 3:
        addSongs(["Frumpy r", "!!Curmudgeon", "Fuck ^^^^^^^me briskly"], Album.query.get(1))
        buySong(1, 2, 1)

    db.session.commit()


@application.before_first_request
def initDB():
    db.create_all()
    setupDatabaseForDebug()
    db.session.commit()

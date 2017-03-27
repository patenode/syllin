from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password
from syllin import views
from syllin.security import user_datastore, security
from syllin.app import application
from syllin.db_model import db
from syllin.models import User, Role, Purchase, Song, Album
from flask_mail import Mail
from syllin.database_methods import setupDatabaseForDebug


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



## Jinja functions
@application.context_processor
def utility_processor():
    def user_owns_song(user, song):
        if Purchase.query.filter(Purchase.buyer_id==user.id).filter(Purchase.song_id==song.id).first():
            return True
        else:
            return False

    return dict(user_owns_song=user_owns_song)

@application.before_first_request
def initDB():
    db.create_all()
    setupDatabaseForDebug()
    db.session.commit()

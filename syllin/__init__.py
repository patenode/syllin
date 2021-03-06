from flask_security import Security, SQLAlchemyUserDatastore
from flask import current_app
from flask_security.core import current_user
from flask_security.utils import encrypt_password
from syllin import views
from syllin.security import user_datastore, security
from syllin.app import application
from syllin.db_model import db
from syllin.models import User, Role, Purchase, Song, Album
from flask_mail import Mail
from syllin.database_methods import setupDatabaseForDebug, user_owns_song


application.config.update(dict(
    DEBUG = True,
    # email server
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'syllin.mail',
    MAIL_PASSWORD = 'pleasechangethis',

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
    return dict(user_owns_song=user_owns_song)

@application.before_first_request
def initDB():
    db.create_all()
    setupDatabaseForDebug()
    db.session.commit()

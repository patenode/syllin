from flask.ext.security import Security, SQLAlchemyUserDatastore
from db_model import db
from models import User, Role, Album, Purchase, Song # For Flask-Security
from app import application
import views


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(application, user_datastore)
db.init_app(application)


def addSongs(l_song_titles):
    for song_title in l_song_titles:
        db.session.add(Song(title=song_title))
    db.session.commit()
def buySong(song_id, buyer_id, seller_id):
    song = Song.query.get(song_id)
    buyer = User.query.get(buyer_id)
    seller = User.query.get(seller_id)

    purchase = Purchase(buyer=buyer, seller=seller, song=song)

    db.session.add(purchase)
    db.session.commit()

def setupDatabaseForDebug():
    if not User.query.first():
        user_datastore.create_user(email='matt@nobien.net', password='password')
        user_datastore.create_user(email='joosh@nobien.net', password='password')

    if len(Song.query.all()) < 3:
        addSongs(["Big booty butts", "Cat Party", "Needle in the Hay"])
        buySong(1,2,1)

    db.session.commit()


@application.before_first_request
def initDB():
    db.create_all()
    setupDatabaseForDebug()
    db.session.commit()

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
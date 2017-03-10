from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

from syllin.db_model import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    profile_pic = db.Column(db.Text()) # s3 url
    bio = db.Column(db.Text())
    favorite_artists = db.Column(db.Text())
    registered_artist = db.Column(db.Boolean)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime()) # Used for (Member Since)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "User {} : {} : {}".format(self.id, self.email, self.password)


class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    songs = db.relationship("Song", back_populates="album")
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artist = db.relationship("User", backref=db.backref('albums', lazy='dynamic'))
    cover_art = db.Column(db.Text()) # s3 url


class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    
    album_id = db.Column(db.Integer(), db.ForeignKey("album.id"))
    album = db.relationship("Album", back_populates="songs")
    
    resource_uri = db.Column(db.Text())
    
    title = db.Column(db.Text())

    artist_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    artist = db.relationship("User", backref=db.backref('songs', lazy='dynamic'))

    def __repr__(self):
        return "{} : {}".format(self.id, self.title)


class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = db.Column(db.Integer, primary_key=True)

    buyer_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    buyer = db.relationship("User", foreign_keys=[buyer_id], backref=db.backref('purchases', lazy='dynamic'))

    seller_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    seller = db.relationship("User", foreign_keys=[seller_id], backref=db.backref('sells', lazy='dynamic'))

    song_id = db.Column(db.Integer(), db.ForeignKey('song.id'), nullable=False)
    song = db.relationship("Song", foreign_keys=[song_id], backref=db.backref('sold', lazy='dynamic'))

    __table_args__ = (
        db.UniqueConstraint('buyer_id', 'song_id', name='_song_buyer_purchase_uc'),
    )

    def __init__(self, buyer=None, seller=None, song=None):
        self.seller = seller
        self.buyer = buyer
        self.song = song

    def __repr__(self):
        return "Purchase {}".format(self.song.title)


class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    buyer_id = db.Column(db.Integer(), db.ForeignKey('user.id'),  nullable=False)
    buyer = db.relationship("User", foreign_keys=[buyer_id],backref=db.backref('recommended_to', lazy='dynamic'))

    seller_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    seller = db.relationship("User", foreign_keys=[seller_id], backref=db.backref('recommended_by', lazy='dynamic'))

    song_id = db.Column(db.Integer(), db.ForeignKey('song.id'), nullable=False)
    song = db.relationship("Song", foreign_keys=[song_id], backref=db.backref('recommendations', lazy='dynamic'))

    __table_args__ = (
        db.UniqueConstraint('buyer_id', 'song_id', name='_song_buyer_recommendation_uc'),
        )

    def __init__(self, buyer=None, seller=None, song=None):
        self.seller = seller
        self.buyer = buyer
        self.song = song

    def __repr__(self):
        return "Recommend {}".format(self.song.title)
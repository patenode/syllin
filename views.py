from models import User, Song, Album, Role, Purchase
from flask import render_template
from app import application

@application.route('/jeff')
def home():
    q = "Hello "

    for user in User.query.all():
        q = q + user.email
    return q

@application.route('/purchases')
def purchases():
    q = ""
    para = "<p>{}</p>"
    for purchase in Purchase.query.all():
        q = q + para.format(str(purchase))

    return q

@application.route('/songs')
def song():
    q = "Songs "

    para = "<p>{}</p>"
    for song in Song.query.all():
        q = q +"  " + para.format(str(song))
    return q

@application.route('/users')
def users():
    q = "Users "

    para = "<p>{}</p>"
    for user in User.query.all():
        q = q +"  " + para.format(str(user))
    return q


@application.route('/users/<user_id>')
def display_user(user_id):
    user = User.query.get(user_id)

    purchased_songs = [purchase.song for purchase in user.purchases]
    out = ""

    for purchase in user.purchases:
        out += "<p>{}</p>".format(str(purchase))

    return render_template("user_library.html",purchased_songs=purchased_songs)

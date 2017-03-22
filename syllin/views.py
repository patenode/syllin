import boto3, os, json
from flask import render_template, request, redirect
from flask_security import roles_accepted, login_required
from flask_security.core import current_user
from syllin import user, song, album
from syllin.security import user_datastore
from syllin.app import application
from syllin.db_model import db
from syllin.models import Song, User, Role, Album
from syllin.templated import templated
from syllin.forms.forms import SongForm, AlbumForm

application.register_blueprint(user.views)
application.register_blueprint(album.views)
application.register_blueprint(song.views)


@application.route('/')
@login_required
def index():
    q = Song.query.all()

    # Purely for visualization, creates tag list 't'
    from random import getrandbits
    rand_bool = lambda: bool(getrandbits(1))
    t = [('Genre {i}'.format(i=i), rand_bool()) for i in range(5)]
    return render_template('discovery.html', user=current_user, songs=q, tags=t)


@application.route('/<tag>')    
def link(tag):
    return "Processing the tag '{tag}'...".format(tag=tag)


@application.route('/settings')
def settings():
    return render_template('settings.html', user=current_user)

@application.route('/promote', methods=["POST", "GET"])
@roles_accepted('admin')
@templated('promote.html')
def promoteUsers():
    # Post role    
    user_id = request.form.get("user", None)
    if user_id:
        user = User.query.get(user_id)
        verifyArtist(user)
     
    # Get non-artists   
    users = User.query.all() #filter(~User.roles.any(Role.name=='artist'))

    return dict(users=users)#dict(users=users)


def verifyArtist(user):
    user_datastore.add_role_to_user(user, user_datastore.find_role('artist'))
    db.session.commit()

@application.route("/file_upload")
@templated("fileUpload.html")
@roles_accepted('admin', 'artist')
def fileUpload():
    form = SongForm()
    return dict(form=form)

@application.route("/new_album",methods=["GET", "POST"])
@templated("album/new_album.html")
@login_required
def albumUpload():
    form = AlbumForm()

    if form.validate_on_submit():
        album_title = form.title.data
        album_cover_url = form.s3_data_url.data

        song = Album(title=album_title, cover_art=album_cover_url, artist=current_user)
        db.session.add(song)
        db.session.commit();
        return redirect('/success')

    return dict(form=form)


## API

@application.route('/sign_s3/')
@login_required
def sign_s3():
    S3_BUCKET = os.environ.get('S3_BUCKET')

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = boto3.client('s3')

    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })


@application.route("/submit_form", methods=["POST"])
@templated('printSelectedFile.html')
@roles_accepted('admin', 'artist')
def submit_form():
    song_name = request.form["title"]
    song_url = request.form["s3_data_url"]

    song = Song(title=song_name, resource_uri=song_url, artist=current_user)
    db.session.add(song)
    db.session.commit();
    # update_account(username, full_name, avatar_url) ##TODO -- Print the url, just to prove that it's coming through (in html)

    return dict(fileUrl=song_url)

@application.route("/update-profile", methods=["POST"])
@login_required
def update_profile():
    
    user = User.query.get(current_user.id)

    user.name = request.form['name']
    user.bio = request.form['bio']
    if (request.form['s3_data_url']):
        user.profile_pic = request.form['s3_data_url']

    user.favorite_artists = request.form['favorite-artists']

    db.session.add(user)
    db.session.commit();
    return "NOPE"
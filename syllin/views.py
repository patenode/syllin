import boto3, os, json
from flask import render_template, request
from flask_security import roles_accepted, login_required
from flask_security.core import current_user
from syllin import user, song, album
from syllin.security import user_datastore
from syllin.app import application
#from syllin.user import current_user
from syllin.db_model import db
from syllin.models import Song, User, Role
from syllin.templated import templated

application.register_blueprint(user.views)
application.register_blueprint(album.views)
application.register_blueprint(song.views)


@application.route('/')
@login_required
def index():
    q = Song.query.all()
    return render_template('discovery.html', user_id=current_user.id, songs=q)


@application.route('/<tag>')
def link(tag):
    return "Processing the tag '{tag}'...".format(tag=tag)


@application.route('/settings')
def settings():
    return render_template('settings.html', user_id=current_user.id)

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
    users = User.query.filter(~User.roles.any(Role.name=='artist'))

    return dict(users=users)#dict(users=users)


def verifyArtist(user):
    user_datastore.add_role_to_user(user, user_datastore.find_role('artist'))
    db.session.commit()

# possible problem with forward slash in app.route?
@application.route("/file_upload")
@templated("fileUpload.html")
@roles_accepted('admin', 'artist')
def fileUpload():
    return dict()

@application.route('/sign_s3/')
@roles_accepted('admin', 'artist')
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
    song_name = request.form["song_name"]
    song_url = request.form["song_url"]

    song = Song(title=song_name, resource_uri=song_url, artist=current_user)
    db.session.add(song)
    db.session.commit();
    # update_account(username, full_name, avatar_url) ##TODO -- Print the url, just to prove that it's coming through (in html)


    return dict(fileUrl=song_url)



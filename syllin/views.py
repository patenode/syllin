import boto3, os, json
from flask import render_template, request

from syllin import user, song, album
from syllin.app import application
from syllin.user import current_user
from syllin.models import Song
from syllin.templated import templated

application.register_blueprint(user.views)
application.register_blueprint(album.views)
application.register_blueprint(song.views)


@application.route('/')
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


# possible problem with forward slash in app.route?
@application.route("/file_upload/")
@templated("fileUpload.html")
def fileUpload():
    return dict()


@application.route('/sign_s3/')
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


@application.route("/submit_form/", methods=["POST"])
@templated('printSelectedFile.html')
def submit_form():
    username = request.form["username"]
    full_name = request.form["full-name"]
    avatar_url = request.form["avatar-url"]

    # update_account(username, full_name, avatar_url) ##TODO -- Print the url, just to prove that it's coming through (in html)


    return dict(fileUrl=avatar_url)

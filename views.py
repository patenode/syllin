from models import User, Song, Album, Role, Purchase
from flask import render_template, request
from app import application
from templated import templated
import boto3, os, json

@application.route('/')
def index_view():
   return "Index"

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
@templated("user_library.html")
def display_user(user_id):
    user = User.query.get(user_id)

    purchased_songs = [purchase.song for purchase in user.purchases]
    out = ""

    for purchase in user.purchases:
        out += "<p>{}</p>".format(str(purchase))

    return dict(purchased_songs=purchased_songs)

#possible problem with forward slash in app.route?
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
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
  )

  return json.dumps({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
  })


@application.route("/submit_form/", methods = ["POST"])
@templated('printSelectedFile.html')
def submit_form():
  username = request.form["username"]
  full_name = request.form["full-name"]
  avatar_url = request.form["avatar-url"]

  #update_account(username, full_name, avatar_url) ##TODO -- Print the url, just to prove that it's coming through (in html)


  return dict(fileUrl = avatar_url)
  
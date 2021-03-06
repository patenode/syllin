from wtforms import StringField, IntegerField, SubmitField, HiddenField, SelectField
from flask_security.forms import RegisterForm, Required
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [Required()])

class SongForm(FlaskForm):
	title = StringField('Title', [Required("A song needs a title")])
	album = SelectField('Album', coerce=int) # Must be dynamically filled : form.album.choices
	s3_data_url = HiddenField()
	submit = SubmitField("Add Song")

class AlbumForm(FlaskForm):
	title = StringField('Album Title', [Required("An album needs a title")])
	s3_data_url = HiddenField() 
	submit = SubmitField("Add Album")

class SongPurchaseForm(FlaskForm):
	song_id = HiddenField()
	user_id = HiddenField()
	purchase = SubmitField("Purchase")
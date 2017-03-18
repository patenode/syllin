from wtforms import StringField, IntegerField, SubmitField, HiddenField
from flask_security.forms import RegisterForm, Required
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [Required()])

class SongForm(FlaskForm):
	title = StringField('Title', [Required("A song needs a title")])
	#album_id = IntegerField('Album')
	s3_data_url = HiddenField()
	resource_url = StringField('resource_url', [Required("Need a music file")])
	submit = SubmitField("Add Song")


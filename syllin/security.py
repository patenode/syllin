from syllin.db_model import db
from syllin.models import User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from syllin.app import application

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(application, user_datastore)
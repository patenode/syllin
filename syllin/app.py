import os

from flask import Flask

application = Flask(__name__)

## Config
if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            "ENGINE": "POSTGRES!!!!",
            'NAME': 'i1',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + DATABASES['default']['USER'] + ':' + \
                                                DATABASES['default']['PASSWORD'] + '@' + DATABASES['default'][
                                                    'HOST'] + ':' + DATABASES['default']['PORT'] + '/' + \
                                                DATABASES['default']['NAME']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
application.config['SECURITY_PASSWORD_SALT'] = 'TODO-Figure_out_if_I_should_change_this'
application.config['SECRET_KEY'] = 'CanUGuessMe_ThisValueDOesntMatter'
application.config['SECURITY_REGISTERABLE'] = True
application.config['SECURITY_CONFIRM_ERROR_VIEW'] = "/login"
application.config['SECURITY_UNAUTHORIZED_VIEW'] = '/login' 
application.config['SECURITY_POST_REGISTER_VIEW'] = '/' 
application.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'register-user.html'
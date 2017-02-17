from flask import Flask
import os

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
else :
    DATABASES = {
        'default': {
            "ENGINE" : "POSTGRES!!!!",
            'NAME': 'industry4',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+ DATABASES['default']['USER'] +':'+ DATABASES['default']['PASSWORD'] +'@'+ DATABASES['default']['HOST'] +':'+ DATABASES['default']['PORT'] +'/'+ DATABASES['default']['NAME']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

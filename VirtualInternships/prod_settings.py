from .settings import *
import django_heroku

DEBUG = False

ALLOWED_HOSTS = ['django-env.eba-ichhqupp.us-west-2.elasticbeanstalk.com', 'covintern.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# AWS Setup
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'corona-internships'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_DEFAULT_ACL = None

AWS_ACCESS_KEY_ID = 'AKIAV5WS73MYQB4ILC7J'
AWS_SECRET_ACCESS_KEY = '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'

# Authentication
LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Activate Django-Heroku.
django_heroku.settings(locals())
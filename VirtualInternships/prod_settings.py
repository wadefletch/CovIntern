import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['django-env.eba-ichhqupp.us-west-2.elasticbeanstalk.com', 'covintern.com']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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

# Sentry Logging
sentry_sdk.init(
    dsn="https://bc6a9f6c56974ec6881770c11088d9f6@sentry.io/5174690",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Activate Django-Heroku.
django_heroku.settings(locals(), logging=False)

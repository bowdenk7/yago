"""
Django settings for Yago project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from util.settingsUtil import get_env_variable
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Bowden Kelly', 'bowdenk7@gmail.com'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_variable('DJANGO_DEBUG') == "True"
HEROKU = get_env_variable('HEROKU') == "True"
USE_AWS = get_env_variable('USE_AWS') == "True"

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

if HEROKU:
    DATABASES = {'default': dj_database_url.config()}
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2'
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': 'localhost',             # Set to empty string for localhost.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Allow all host headers
ALLOWED_HOSTS = ['*']

if USE_AWS:
    AWS_BUCKET_NAME = get_env_variable('AWS_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
    S3_URL = 'http://s3.amazonaws.com/%s/' % AWS_BUCKET_NAME
    DEFAULT_FILE_STORAGE = 'Util.s3utils.MediaRootS3BotoStorage'
    STATICFILES_STORAGE = 'Util.s3utils.StaticRootS3BotoStorage'

    STATIC_URL = S3_URL + 'static/'
    MEDIA_ROOT = S3_URL + 'uploads/'

#uncomment for SES email support
# EMAIL_BACKEND = 'django_ses.SESBackend'
# EMAIL_PORT = 465
# EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
# EMAIL_HOST_USER = get_env_variable("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_HOST_PASSWORD")



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'markdown',
    'geoposition',
    'account',
    'feed',
    'user_post',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'yagoapp.urls'

WSGI_APPLICATION = 'yagoapp.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
if not USE_AWS:
    STATIC_URL = '/static/'

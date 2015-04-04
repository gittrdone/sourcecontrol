"""
Django settings for sourcecontrol project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import sys
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

#DB URL support
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5l2#a%gtdo-d)b!auf-7du_ozo09tha1y!kw)r#!#f))$blf8k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sourceControlApp',
    'reporting',
    'celery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'update_repos': {
        'task': 'sourceControlApp.tasks.reprocess_repos',
        'schedule': timedelta(seconds=1800),
    },
}
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

ROOT_URLCONF = 'sourcecontrol.urls'

WSGI_APPLICATION = 'sourcecontrol.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse("postgres://xqxyrljduzoqzb:xbJndoQsZj3xqXjzSs0pH4QsS5@ec2-54-204-45-196.compute-1.amazonaws.com:5432/d1ii2r5g0om1q1")
}
if 'TRAVIS' in os.environ:
    DATABASES = {
            'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travisci',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
elif "test" in sys.argv:
    DATABASES['default'] = { "ENGINE": "django.db.backends.sqlite3" }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..' ,'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'sourcecontrol.processors.repo_nav_options',
    'sourcecontrol.processors.repo_nav_options_reports'
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sourcecontrolme@gmail.com'
EMAIL_HOST_PASSWORD = 'sourcecontrol.me'

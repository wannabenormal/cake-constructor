from pathlib import Path
import os
from environs import Env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

env = Env()
env.read_env()
STRIPE_PUBLIC_KEY = env.str('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env.str('STRIPE_SECRET_KEY')

SECRET_KEY = 'django-insecure-+_&^71pgrwa%o6b$r5d15^7ypt&460-nzdr^0=yl!upxn=abdc'

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['*'])

INSTALLED_APPS = [
    'debug_toolbar',
    'cakeshop.apps.CakeshopConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'accounts.apps.AccountsConfig',
    'phonenumber_field',
    'utm_tracker'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utm_tracker.middleware.UtmSessionMiddleware',
    'utm_tracker.middleware.LeadSourceMiddleware',
]

ROOT_URLCONF = 'cake_constructor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cake_constructor.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning', }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = ['*']
CORS_ALLOW_HEADERS = ['*']
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000"]
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'


#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "static"),
#]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

INTERNAL_IPS = [
    '127.0.0.1',
]

LOGIN_REDIRECT_URL = '/'

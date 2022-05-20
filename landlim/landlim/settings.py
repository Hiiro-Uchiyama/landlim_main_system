## landlim_web_edition - ç - 2022 - Hiiro Uchiyama
## Edit 2021/6/26 - The settings are defined.
## Edit 2021/6/27 - More message apps in the settings.
## Edit 2021/8/17 - The name of the database was changed to LandLim.
## Edit 2021/9/23 - I thought about the API.
## Edit 2021/12/17 - We have added blogs and jobs to our search system.
## I want to change the database name.
## The UI is very subtle.
## Let's debug and test.

## Function to get here
## Save your location in advance
## You get points for actually going there and posting.
## The implementation of blockchain and APIs is a barrier.
## Maybe we should not include the map feature in the submission list.
## How to set it up
## Let's make jobs and blogs (ads) visible
## Let's display it in a list
## How about a sidebar that appears if you are logged in so you can go right back to the jobs and blogs?
## Contact function needs to be further improved.
## Connect with EC
## Sell locally
## I would like to interact with other services via API
## Video stand-alone posting
## Measure distance and display
## Local map
## World Map
## Display order algorithm
## User trend storage
## User activity monitoring data model
## Validation of data to be passed
## Form validation
## I think we should be able to embed YouTube videos.
## Notice
## Make it impossible to incorporate <>programs in the text
## Set up validators
## Maybe you can add some emotion to your post.
## The video portion is still a work in progress.
## Improving the quality of content
## Prepare a visual of the code.
## Algorithm implementation.

import os
import dj_database_url
from pathlib import Path

## Build paths inside the project like this: BASE_DIR / 'subdir'.
## Quick-start development settings - unsuitable for production
## See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
## SECURITY WARNING: keep the secret key used in production secret!
## SECURITY WARNING: don't run with debug turned on in production!
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'SECRET_KEY'

## False for the production environment.
DEBUG = True

## Allowed domains
ALLOWED_HOSTS = []

## If you want to add more applications, add them here
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'post',
    'core',
    'bootstrap4',
    'accounts',
    'want_todo',
    'search_post',
    'search_blog',
    'search_recruit',
    'notification',
    'contact',
    'bookmark',
    'report',
    'api',
    'blog',
    'guide',
    'recent',
    'recruit',
    'description',
    'message',
    'taggit',
    'versatileimagefield',
    'rules.apps.AutodiscoverRulesConfig',
    'django_cleanup',
    'widget_tweaks',
    'storages',
    'sorl.thumbnail',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.instagram',
    'django_summernote',
    'rest_framework',
    'django.forms',
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

## WhiteNoiseMiddleware is required in the production environment.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'landlim.urls'

## PROJECT_ROOT settings
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

## Setting up access to templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'builtins':[
                'bootstrap4.templatetags.bootstrap4',
            ],
            'libraries': {
                'show__pagenated_post_list': 'blog.templatetags.show__pagenated_post_list',
                'show___pagenated_post_list': 'recruit.templatetags.show___pagenated_post_list',
            }
        },
    },
]

## wsgi application setup
WSGI_APPLICATION = 'landlim.wsgi.application'

## https://docs.djangoproject.com/en/3.1/ref/settings/#databases
## If an error occurs on the local server
## sudo brew services start postgresql
## sudo brew services stop postgresql
## brew services restart postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'landlim',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
    }
}

## Password validation
## https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

## This is determined by the number of sites.
SITE_ID = 2

## Set up your social account.
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

## Google social account settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'

## Internationalization
## https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

## Specify a static file
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

## Google Mail settings
DEFAULT_FROM_EMAIL = 'DEFAULT_FROM_EMAIL'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'

## Setting up AWS
## https://docs.djangoproject.com/en/3.1/howto/static-files/
AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
AWS_STORAGE_BUCKET_NAME = 'AWS_STORAGE_BUCKET_NAME'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = S3_URL
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_EXPIRE = 63115200

## upload file
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

## django-summernote
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'

## Specify the character format of the file
FILE_CHARSET = 'utf-8'

## Specifying the number of pagination posts to display
PAGE_PER_ITEM = 4

SITE_HOST = 'http://127.0.0.1:8000'
ENABLE_SSL = False

## Django's default user model settings
AUTH_USER_MODEL = 'accounts.User'
## URL to redirect to after login
LOGIN_REDIRECT_URL = '/accounts/own_page/'
## URL for login
LOGIN_URL = '/accounts/login/'

## app.Comment: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

## for managing tag objects.
TAGGIT_CASE_INSENSITIVE = True

## Setting the pagination of objects displayed on a single page
POST_NUM_PER_PAGE = 20

## Manage image objects.
THUMBNAIL_DEBUG = True

## Path to the multilingual configuration folder for multilingual sites
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

## Setting up for multilingualism
## Available in Japanese and English
from django.utils.translation import ugettext_lazy as _
LANGUAGES = [
    ('ja', _('Japanese')),
    ('en', _('English')),
]

JWT_AUTH = {
    'JWT_VERIFY_EXPIRATION': False,
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'NON_FIELD_ERRORS_KEY': 'detail',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
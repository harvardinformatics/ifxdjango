"""
Django settings for ifxdjango project.

Generated by 'django-admin startproject' using Django 2.2.4.

Created on  {% now "Y-m-d" %}

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from decimal import Decimal

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('{{project_name|upper}}_DJANGO_KEY', 'alskdfjalskdja')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('{{project_name|upper}}_DEBUG', 'FALSE').upper() == 'TRUE'

SITE_ID = 1

ALLOWED_HOSTS = ['*']

IFX_AUTH_NEW_USER_ENABLED = False

DB_USERNAME = os.environ.get('{{project_name|upper}}_USERNAME', '{{project_name}}')
DB_PASSWORD = os.environ.get('{{project_name|upper}}_PASSWORD', '{{project_name}}')
DB_DATABASE = os.environ.get('{{project_name|upper}}_DATABASE', '{{project_name}}')
DB_HOSTNAME = os.environ.get('{{project_name|upper}}_HOSTNAME', '{{project_name}}')
LOGLEVEL = os.environ.get('{{project_name|upper}}_LOGLEVEL', 'INFO')
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'rcsmtp.rc.fas.harvard.edu:25')

if SMTP_SERVER:
    try:
        eles = SMTP_SERVER.strip().split(':')
        eles.append(25)
        EMAIL_HOST = eles[0].strip()
        EMAIL_PORT = int(eles[1])
    except Exception as e:
        print('Something wrong with the SMTP_SERVER environment variable: %s' % str(e))



# App name and token
IFX_APP = {
    'token' : os.environ.get('{{project_name|upper}}_IFX_APP_TOKEN'),
    'name': '{{project_name}}',
}
IFX_AUTH_META_KEY = 'HTTP_HKEY_EDUPERSONPRINCIPALNAME'

ALLOWED_HOSTS = ['{{project_name}}-drf', 'ifxonboard-drf', 'localhost', '127.0.0.1', 'ifx.fas.harvard.edu', 'fiine.rc.fas.harvard.edu']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True


if IFX_APP['token'] == 'FIXME':
    print('HEY!!!!!  Set the IFX_APP_TOKEN in docker-compose!')


# Application definition
INSTALLED_APPS = [
    'ifxuser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djvocab',
    'ifxauth',
    'author',
    'ifxrequest',
    'ifxbilling',
    'ifxreport',
    'django_extensions',
    '{{project_name}}',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'ifxauth.auth.IfxRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'author.middlewares.AuthorDefaultBackendMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'ifxauth.auth.IfxRemoteUserBackend',
]

ROOT_URLCONF = '{{project_name}}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/static', os.path.join(BASE_DIR, 'static'), os.path.join(BASE_DIR, 'frontend', 'dist'),],
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

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':       'django.db.backends.mysql',
        'NAME':         DB_DATABASE,
        'USER':         DB_USERNAME,
        'PASSWORD':     DB_PASSWORD,
        'HOST':         DB_HOSTNAME,
        'PORT':         3306,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8mb4,collation_connection=utf8mb4_unicode_ci,group_concat_max_len=50000'
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True
UNICODE_JSON = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/{{project_name}}/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'public')
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


## Logging setup
# Logging setup.  Meant to log everything to stderrr
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'level': LOGLEVEL,
            'filters': ['require_debug_false'],
        },
        'console_debug': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'level': LOGLEVEL,
            'filters': ['require_debug_true'],
        },
        'mail_admins_debug': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'filters': ['require_debug_true'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        '{{project_name}}': {
            'handlers': ['console', 'console_debug', 'mail_admins'],
            'level': LOGLEVEL,
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'console_debug'],
            'level': LOGLEVEL,
            'propagate': False
        },
        'ifxauth': {
            'handlers': ['console', 'console_debug'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


CSRF_USE_SESSIONS = False
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'https://*.rc.fas.harvard.edu', 'https://*.fas.harvard.edu']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

AUTH_USER_MODEL = 'ifxuser.IfxUser'

# User that will 'author' request state changes that are not done by a person
DEFAULT_USERNAME = '{{project_name}}'

IFXREQUEST_PROCESSOR_MODULE = '{{project_name}}.request.processor'
IFXREQUEST_DEFAULT_USERNAME = '{{project_name}}'
IFX_AUTH_NEW_USER_ENABLED = False

MEDIA_ROOT = '/app/media/'
MEDIA_URL = '/{{project_name}}/media/'

# Needed for file uploads :)
FILE_UPLOAD_PERMISSIONS = 0o644

IFXREPORT_FILE_ROOT = os.path.join(MEDIA_ROOT, 'reports')
IFXREPORT_URL_ROOT = f'{MEDIA_URL}reports'

ADMINS = [
    ('Aaron Kitzmiller', 'akitzmiller@g.harvard.edu'),
    ('Ifx Admin', 'ifx@fas.harvard.edu'),
]

SERVER_EMAIL = 'ifx@fas.harvard.edu'
DEFAULT_EMAIL_FROM_ADDRESS = 'ifx@fas.harvard.edu'

class EMAILS():
    '''
    Email addresses
    '''
    DEFAULT_EMAIL_FROM_ADDRESS = DEFAULT_EMAIL_FROM_ADDRESS

class GROUPS():
    '''
    Group names
    '''
    ADMIN_GROUP_NAME = 'Admin'
    ACCOUNT_REQUEST_COMPLETED_NOTIFICATION_GROUP = 'Admin'
    REQUEST_APPROVERS_GROUP_NAME = 'Admin'


class IFXMESSAGES():
    '''
    ifxmail message names
    '''
    ACCOUNT_REQUEST_REJECTION_MESSAGE_NAME = '{{project_name}}_account_request_rejection_message'
    ACCOUNT_REQUEST_MODIFICATION_NOTIFICATION_MESSAGE = '{{project_name}}_account_request_modification_notification_message'
    ACCOUNT_REQUEST_USER_UPDATE_NOTIFICATION_MESSAGE = '{{project_name}}_account_request_user_update_notification_message'
    ACCOUNT_REQUEST_APPROVER_NOTIFICATION_MESSAGE = '{{project_name}}_account_request_approver_notification_message'
    ACCOUNT_REQUEST_COMPLETED_MESSAGE = '{{project_name}}_account_request_completed_message'
    ACCOUNT_REQUEST_COMPLETED_USER_NOTIFICATION_MESSAGE = '{{project_name}}_account_request_completed_user_notification_message'


class ROLES():
    '''
    Names for roles, corresponding to account request tracks
    '''
    TEST = 'test'
    MODULES = [
        '{{project_name}}_admin',
        '{{project_name}}_user',
    ]
    PACKAGE_NAME = '{{project_name}}.roles'
    ADMIN_ROLE_NAME = '{{project_name}}_admin'

ACCOUNT_REQUEST_TRACKS = ['{{project_name}}_admin', '{{project_name}}_user']

# Assuming ifxbilling is installed, these models should be ignored by the django-author pre-save
# so that author values can be directly set
AUTHOR_IGNORE_MODELS = [
    'ifxbilling.BillingRecord',
    'ifxbilling.Transaction',
]

STANDARD_QUANTIZE = Decimal('0.0000')
TWO_DIGIT_QUANTIZE = Decimal('0.00')
REQUESTS_TIMEOUT = 300

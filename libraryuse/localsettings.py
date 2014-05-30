# Django local settings for libraryuse project.

import os
from mongoengine import register_connection
#os.environ['HTTP_PROXY'] = 'http://skoda.library.emory.edu:3128'
os.environ['ORACLE_HOME'] = '/opt/instantclient_11_2'
os.environ['LD_LIBRARY_PATH'] = '/opt/instantclient_11_2'
os.environ['TNS_ADMIN'] = '/opt/instantclient_11_2/network/admin/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEV_ENV = True

# IP addresses that should be allowed to see DEBUG info
INTERNAL_IPS = ('127.0.0.1', '127.0.1.1',)

ADMINS = (
     ('Michael Mitchell', 'mmitc3@emory.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'library_information',        # Or path to database file if using sqlite3.
        'USER': 'libraryuse',                     # Not used with sqlite3.
        'PASSWORD': 'd1gb00ks',                # Not used with sqlite3.
        'HOST': 'db.library.emory.edu',   # Set to empty string for localhost. Not used with sqlite3.
        #'HOST': 'kamina.library.emory.ed,
        #'HOST': 'localhost',
        'PORT': '',        
    },
   # 'mongodb' : {
   #     'ENGINE' : 'django_mongodb_engine',
   #     'NAME' : 'libraryuse'
   #}
}

# MongoDB settings
#register_connection(alias='default',name='libraryuse')

#DATABASE_ROUTERS= ['dbrouter.DBRouter']

SOUTH_DATABASE_ADAPTERS = {
    'default': "south.db.mysql",
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = '12345avria9h0veoinlkdnkalndvlkasndivlskdvjaklsj'

# LDAP configuration
AUTH_LDAP_SERVER = 'ldaps://vlad.service.emory.edu'
AUTH_LDAP_BASE_USER = 'uid=libweb,ou=services,o=emory.edu' # DN of the  base LDAP user (e.g., 'uid=foo,ou=bar,o=emory.edu')
AUTH_LDAP_BASE_PASS = 'untilthecowscomehome' # password for that user
AUTH_LDAP_SEARCH_SUFFIX = 'o=emory.edu'
AUTH_LDAP_SEARCH_FILTER = '(uid=%s)'
AUTH_LDAP_CHECK_SERVER_CERT = False # set to False to skip server cert verification (TESTING ONLY)
AUTH_LDAP_CA_CERT_PATH = ''        # full path to CA cert bundle


# for Developers only: to use sessions in runserver, uncomment this line (override configuration in settings.py)
SESSION_COOKIE_SECURE = False

CACHE_BACKEND = 'file:///tmp/oe_cache'

#These setting should not be needed on staging and production
EMAIL_HOST = 'smtp.service.emory.edu'
#EMAIL_PORT = 465
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
SERVER_EMAIL = 'mmitc3@emory.edu'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'basic': {
            'format': '[%(asctime)s] %(levelname)s:%(name)s::%(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
         },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,            
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'basic'
        },
    },
    'loggers': {
        'libraryuse': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


# file libraryuse/settings.py
# 
#   Copyright 2013 Emory University General Library
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Django settings for libraryuse project.

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, '..', 'sitemedia'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    # defaults:
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",

    # application-specific:
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # flatpages middleware should always be last (fallback for 404)
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'libraryuse.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, '..', 'templates'),
    
)

LOGIN_URL = '/admin'
LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    #'django.contrib.markup',
    'django.contrib.humanize',
    'django_tables2',
    'south',
    'eullocal.django.emory_ldap',
    'libraryuse',
    'tastypie',
    'tastypie_mongoengine',

)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

FILE_UPLOAD_HANDLERS = (
    # removing default MemoryFileUploadHandler so all uploaded files can be treated the same
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_AGE = 604800   # 1 week (Django default is 2 weeks)
SESSION_COOKIE_SECURE = True  # mark cookie as secure, only transfer via HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

try:
    from localsettings import *
except ImportError:
    import sys
    print >>sys.stderr, '''Settings not defined. Please configure a version
        of localsettings.py for this site. See localsettings.py.dist for
        setup details.'''
    del sys

TEST_RUNNER = 'digitizedbooks.testutil.ManagedModelTestRunner'


# disable south tests and migrations when running tests
# - without these settings, test fail on loading initial fixtured data
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

AUTH_USER_MODEL = 'emory_ldap.EmoryLDAPUser'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'eullocal.django.emory_ldap.backends.EmoryLDAPBackend',
)

###########################
## GRRRRRRRRRRRRRRRRRRR ##
#########################


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
    'mongodb' : {
        'ENGINE' : 'django_mongodb_engine',
        'NAME' : 'libraryuse'
   }
}

# MongoDB settings
register_connection(alias='default',name='libraryuse')

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




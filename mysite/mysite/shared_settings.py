# Django settings for mysite project.
import os.path
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
#my first commit
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'homes',
            #os.path.join(PROJECT_ROOT, 'mysql.db'),                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'thebakery',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(
    os.path.dirname(__file__),
    '../../static',
    ),
)
STATICSITEMAPS_ROOT_DIR = os.path.join(
    os.path.dirname(__file__),
    '../../static',
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'nyp189eu)&amp;kc-2dku#sb+-70vj2c3xzxuoen3a^i+4t-i*uzhs'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mysite.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, '../../site-templates/'),
)

INSTALLED_APPS = (
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
   'django.contrib.sites',
 #   'django.contrib.messages',
   'django.contrib.staticfiles',
    'search',
    'django.contrib.admin',
    'crispy_forms',
    'django.contrib.humanize',
    'django_twilio',
    'django_tables2',
    'mathfilters',
    'leaflet',
    'django.contrib.sitemaps',
    'static_sitemaps',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

LEAFLET_CONFIG = {
    #'SPATIAL_EXTENT': (5.0, 44.0, 7.5, 46),
    #'DEFAULT_CENTER': (6.0, 45.0),
    #'DEFAULT_ZOOM': 16,
    #'TILES': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'SCALE': 'imperial',
    'RESET_VIEW': False,
}

TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)
STATICSITEMAPS_ROOT_SITEMAP = 'mysite.urls.sitemaps'

#TO DO MOVE TO ENV VARIABLES
TWILIO_AUTH_TOKEN = '9c9026216c818eb92f78c5921a2d322c'
TWILIO_ACCOUNT_SID = 'AC54c41ac1142b993d70a3177837c111ef'
TWILIO_DEFAULT_CALLERID = '9185495854'
#DJANGO_TWILIO_FORGERY_PROTECTION = False

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
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
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

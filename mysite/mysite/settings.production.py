# Django settings for mysite project.
try:
    from shared_settings import *
except ImportError:
    pass



INSTALLED_APPS = (
   'django.contrib.auth',
   'django.contrib.contenttypes',
   'django.contrib.sessions',
 #   'django.contrib.sites',
 #   'django.contrib.messages',
   'django.contrib.staticfiles',
    'search',
    'django.contrib.admin',
    'crispy_forms',
    'django.contrib.humanize',
    'django_twilio',
    'django_tables2',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# Django settings for mysite project.
try:
    from shared_settings import *
except ImportError:
    pass


DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
   'debug_toolbar',
   )
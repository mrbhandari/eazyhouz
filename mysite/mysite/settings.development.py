# Django settings for mysite project.
try:
    from shared_settings import *
except ImportError:
    pass


import os.path
DEBUG = True
TEMPLATE_DEBUG = DEBUG
from .base import *


STRIPE_SECRET_KEY = 'kjnnkjnfsksdgjk'
STRIPE_PUBLIC_KEY = 'kjnnkjnfsncvbgjk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q=-bn^ow0)d2_w$$y=pm(2&(p%az99yv-2s7nv#uh$0369o%he'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['ebenezerchurch.pythonanywhere.com'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    #'debug_toolbar',
    'django_extensions',
    'wagtail.contrib.styleguide',
]

MIDDLEWARE = MIDDLEWARE + [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Django-Debug-Toolbar
#INTERNAL_IPS = ("127.0.0.1", "172.17.0.1")


try:
    from .local import *
except ImportError:
    pass

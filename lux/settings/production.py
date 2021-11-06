from .base import *
from core.site_settings.models import GoogleScripts

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = [config('IP_HOST'), config('HOST_NAME')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('YOUR_DB_NAME'),
        'USER':config('YOUR_DB_USERNAME'),
        'PASSWORD':config('YOUR_DB_PASSWORD'),
        'HOST':config('YOUR_DB_HOST'),
        'PORT':config('YOUR_HOST_PORT')
    }
}


# AWS S3 Buckets Configuration
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_STORAGE_BUCKET_NAME = ""

AWS_S3_FILE_OVERWRITE = False
AWS_DEAFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# To recovering password and send emails:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #'django.core.mail.backends.filebased.EmailBackend'
EMAIL_HOST_USER = GoogleScripts.gmail_user_account
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_PASSWORD = GoogleScripts.gmail_password


STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')

try:
    from .local import *
except ImportError:
    pass
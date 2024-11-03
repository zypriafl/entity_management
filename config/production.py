import os

from entity_management.settings import *  # noqa

# Server Settings
DEBUG = False
ALLOWED_HOSTS = ['study.local.uberspace.de']
CSRF_TRUSTED_ORIGINS = ['https://www.studylife-muenchen.de', 'https://studylife-muenchen.de', 'https://study.uber.space']
SECRET_KEY = os.environ['SECRET_KEY']

# HTTPS Settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Google Captcha Settings
RECAPTCHA_PUBLIC_KEY = '6LccWDoUAAAAAMv5iCOIzTPUYtf3i4ORKzWLXm7h'
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_PORT = 587
ADMINS = [admin for admin in os.environ['ADMINS'].split(', ')]
DEFAULT_FROM_EMAIL = 'noreply@studylife-muenchen.de'
SERVER_EMAIL = 'noreply@studylife-muenchen.de'


# Uberspace static dir
STATIC_ROOT = '/home/study/html/static/'

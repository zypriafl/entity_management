import os

from entity_management.settings import *

# Server Settings
DEBUG = False
ALLOWED_HOSTS = ['studylife-muenchen.de', 'study.uber.space', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['studylife-muenchen.de', 'study.uber.space']
SECRET_KEY = os.environ['SECRET_KEY']

# Google Captcha Settings
RECAPTCHA_PUBLIC_KEY = '6LccWDoUAAAAAMv5iCOIzTPUYtf3i4ORKzWLXm7h'
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']


# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['EMAIL_HOST']  #'smtp.mailgun.org'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER'] #'noreply@mg.studylife-muenchen.de'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD'] #'7QwslqAOjvoQmYxO7S'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
ADMINS = [admin for admin in os.environ['ADMINS'].split(', ')]
DEFAULT_FROM_EMAIL = 'noreply@studylife-muenchen.de'
SERVER_EMAIL = 'noreply@studylife-muenchen.de'


# Uberspace static dir
STATIC_ROOT = '/home/study/html/static/'

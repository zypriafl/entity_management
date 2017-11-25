import os
from entity_management.settings import *

DEBUG = False
ALLOWED_HOSTS = ['studylife-muenchen.de', 'study.uber.space', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['studylife-muenchen.de', 'study.uber.space']

SECRET_KEY = os.environ['SECRET_KEY']

# Google Captcha Settings
RECAPTCHA_PUBLIC_KEY = '6LccWDoUAAAAAMv5iCOIzTPUYtf3i4ORKzWLXm7h'
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

# Uberspace static dir
STATIC_ROOT = '/home/study/html/static/'
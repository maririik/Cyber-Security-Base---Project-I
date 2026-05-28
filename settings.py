"""
FLAW 4 & 5: A05 Security Misconfiguration
- DEBUG = True exposes stack traces and internal info to users
- SECRET_KEY is hardcoded and weak
- No password validation
- FIX for DEBUG: Set DEBUG = False in production
- FIX for SECRET_KEY: use environment variable
- FIX for passwords: add AUTH_PASSWORD_VALIDATORS
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# FLAW 4: Hardcoded weak secret key (A05 Security Misconfiguration)
# FIX: SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'password123'

# FLAW 4: Debug mode on (A05 Security Misconfiguration)
DEBUG = True
# FIX: DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notes_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'notes_app/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# FLAW 5: No password validators (A07 Identification and Authentication Failures)
# FIX: see views.py register function for manual length check
AUTH_PASSWORD_VALIDATORS = []

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
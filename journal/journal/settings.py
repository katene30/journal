"""
Django settings for journal project.
"""

from pathlib import Path
from decouple import config, Csv
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Comma-separated hostnames, e.g. "journal-abc123.a.run.app,hauora.example.com"
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Comma-separated origins incl. scheme, e.g. "https://journal-abc123.a.run.app"
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:5173,http://127.0.0.1:5173',
    cast=Csv(),
)

# Hosts like Cloud Run terminate HTTPS at a proxy and forward plain HTTP
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'entries',
]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'journal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'journal.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.getenv('DATABASE_URL'):
    # Health checks reconnect if a serverless DB (e.g. Neon) dropped an idle connection
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, conn_health_checks=True)


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Pacific/Auckland'
USE_I18N = True
USE_TZ = True


# Static files

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth
LOGIN_URL = '/api/auth/login/'
LOGIN_REDIRECT_URL = '/app/'
LOGOUT_REDIRECT_URL = '/app/'

# Allauth settings
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
# 'none' until the SPA has a confirm-email page: with 'optional', every signup
# emailed a confirmation link to an API route that has no page behind it
ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# dj-rest-auth settings (use sessions, not tokens)
REST_AUTH = {
    'USE_JWT': False,
    'SESSION_LOGIN': True,
    'TOKEN_MODEL': None,
    'REGISTER_SERIALIZER': 'journal.serializers.CustomRegisterSerializer',
    'LOGIN_SERIALIZER': 'journal.serializers.CustomLoginSerializer',
    'PASSWORD_RESET_SERIALIZER': 'journal.serializers.SpaPasswordResetSerializer',
}

# Password reset links expire after an hour, and stop working once used
# (Django's tokens include the password hash)
PASSWORD_RESET_TIMEOUT = 60 * 60

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    # Per IP; stops the reset form being used to flood someone's inbox
    'password_reset': '5/hour',
    # Per user; limits password guessing from a logged-in session
    'account_delete': '5/hour',
}

# Email: SMTP when EMAIL_HOST is set (production), otherwise printed to the console
EMAIL_HOST = config('EMAIL_HOST', default='')
if EMAIL_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_TIMEOUT = 10
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Hauora Journal <noreply@localhost>')
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

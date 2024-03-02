from decouple import config
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['45.77.105.55', 'freeomi.com', 'www.freeomi.com', '127.0.0.1', 'aff6-113-203-199-3.ngrok-free.app']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'django.contrib.sites',  # Required for django-allauth
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.twitter',

    'account',
    'panel',
    'landing',
    'hcaptcha',
    'ckeditor',
    'ckeditor_uploader',
]

CKEDITOR_UPLOAD_PATH = "ckedit/uploads/"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
    # 'oauth2_provider.backends.OAuth2Backend',
    # 'social_core.backends.twitter.TwitterOAuth',
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

AUTH_USER_MODEL = 'account.User'

ROOT_URLCONF = 'freebitcoin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'freebitcoin.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config("DB_NAME"),
#         'USER': config("DB_USER"),
#         'PASSWORD': config("DB_PASSWORD"),
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'freebit',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'port': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

PRINT_LOG = True
OFF_EMAIL = False

PASSWORD_RESET_TIMEOUT = 86400

# Emails settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'basic': {
            'handlers': ['basic_h'],
            'level': 'DEBUG',
        },
        'basic.error': {
            'handlers': ['basic_e'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
    'handlers': {
        'basic_h': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'simple',
        },
        'basic_e': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
            'formatter': 'simple',
        },
    },
    'formatters': {
        'simple': {
            'format': '{levelname} : {asctime} : {message}',
            'style': '{',
        }
    }
}

LOGIN_REDIRECT_URL = "panel:index"
LOGIN_URL = "landing:landing"
LOGOUT_URL = 'account:logout'

HCAPTCHA_SITEKEY = config('HCAPTCHA_SITEKEY')
HCAPTCHA_SECRET = config('HCAPTCHA_SECRET')

COINMARKET_API_KEY = config('COINMARKET_API_KEY')
BITLAB = config('BITLAB')
BITLAB_TOKEN = config('BITLAB_TOKEN')
CPX_HASH = config('CPX_HASH')
CPX_APP_ID = config('CPX_APP_ID')

TOKEN_PER_USD = 500
MIN_TOKEN_REDEEMABLE = 100

MIN_WITHDRAWAL = 1

# ROLL_SECONDS = 30  # 24 hours to seconds
ROLL_SECONDS = 1 * 60 * 60  # 1 hour to seconds
ROLL_LINK_LIFETIME = 24 * 60 * 60  # 24 hours to seconds

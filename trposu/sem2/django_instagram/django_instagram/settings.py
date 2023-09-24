from pathlib import Path
from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
load_dotenv(dotenv_path='.env_prod')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = getenv('SECRET_KEY')

DEBUG = True if getenv('DEBUG') == "True" else False

ALLOWED_HOSTS = ['*', ]

INSTALLED_APPS = [
    'image_uploader_widget',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'feeds.apps.FeedsConfig',
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

ROOT_URLCONF = 'django_instagram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'django_instagram.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': BASE_DIR / 'logs/logs.log',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['file'],
            'level': getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

JAZZMIN_SETTINGS = {
    'site_logo': 'favicon.png',
    'login_logo': 'img/babushka-photo.png',
    'welcome_sign': 'Администратор Babushka',
    'copyright': 'Babushka',
    'search_model': ['auth.User', 'feeds.group', 'feeds.post'],
    'topmenu_links': [
        {'name': 'Открыть сайт',  'url': 'index'}
    ],
    'usermenu_links': [
        {'name': 'Открыть сайт',  'url': 'index', 'new_window': False, 'icon': 'fas fa-external-link-square-alt'}
    ],
    'custom_links': {
        'feeds': [
            {'name': 'Пользователи', 'url': 'admin:auth_user_changelist', 'icon': 'fas fa-user'},
        ]
    },
    'icons': {
        'feeds.group': 'fas fa-users',
        'feeds.post': 'fas fa-camera-retro',
        'admin.logentry': 'fas fa-address-book',
    },
    'hide_apps': ['auth'],
    'related_modal_active': False,
    'show_ui_builder': False,
    'dark_mode_theme': 'darkly',
}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static', ]

MEDIA_URL = 'media/'
MEDIA_ROOT = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

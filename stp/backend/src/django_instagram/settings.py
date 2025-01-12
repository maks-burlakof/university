from pathlib import Path

from django_instagram.config.settings import get_settings

env = get_settings()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.secret_key.get_secret_value()
DEBUG = env.debug

FRONTEND_URL = env.frontend_url
BACKEND_URL = env.backend_url
ALLOWED_HOSTS = env.allowed_hosts
CORS_ALLOWED_ORIGINS = env.allowed_origins

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "auth_app.apps.AuthAppConfig",
    "users_app.apps.UsersAppConfig",
    "groups_app.apps.GroupsAppConfig",
    "posts_app.apps.PostsAppConfig",
    "core_app.apps.CoreAppConfig",
    "corsheaders",
    "storages",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_instagram.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "django_instagram.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.database_name,
        "USER": env.database_username,
        "PASSWORD": env.database_password.get_secret_value(),
        "HOST": env.database_hostname,
        "PORT": env.database_port,
    }
}

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

AWS_ACCESS_KEY_ID = env.s3_access_key_id.get_secret_value()
AWS_SECRET_ACCESS_KEY = env.s3_secret_access_key.get_secret_value()
AWS_STORAGE_BUCKET_NAME = env.s3_bucket_name
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com"
AWS_S3_REGION_NAME = env.s3_region_name
AWS_S3_ENDPOINT_URL = f"https://{env.s3_endpoint_url}"
AWS_QUERYSTRING_EXPIRE = "3600"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
DEFAULT_FILE_STORAGE = "core_app.storage.PrivateMediaStorage"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "users_app.User"

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "logs.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": LOG_FILE,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["file"],
            "level": env.log_level,
        },
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Babushka API",
    "DESCRIPTION": "University project Babushka - social network for publishing "
    "photos, inspired by Instagram.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": env.access_token_lifetime,
    "REFRESH_TOKEN_LIFETIME": env.refresh_token_lifetime,
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}

JAZZMIN_SETTINGS = {
    "site_logo": "favicon.png",
    "login_logo": "babushka-logo.png",
    "welcome_sign": "Babushka administrator",
    "copyright": "Babushka",
    "search_model": ["user_app.User", "group_app.Group", "post_app.Post"],
    "topmenu_links": [{"name": "Open website", "url": FRONTEND_URL}],
    "usermenu_links": [
        {
            "name": "Open website",
            "url": FRONTEND_URL,
            "new_window": False,
            "icon": "fas fa-external-link-square-alt",
        }
    ],
    # "custom_links": {
    #     "feeds": [
    #         {
    #             "name": "Пользователи",
    #             "url": "admin:auth_user_changelist",
    #             "icon": "fas fa-user",
    #         },
    #     ]
    # },
    # "icons": {
    #     "feeds.group": "fas fa-users",
    #     "feeds.post": "fas fa-camera-retro",
    #     "admin.logentry": "fas fa-address-book",
    # },
    "hide_apps": ["auth"],
    "related_modal_active": False,
    "show_ui_builder": False,
    "dark_mode_theme": "darkly",
}

LANGUAGE_CODE = "en-en"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login"

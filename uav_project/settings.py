from pathlib import Path

# Yes, its a URI, not a URL, fight me :P
import dj_database_url as dj_database_uri
from corsheaders.defaults import default_headers

from uav_project.utils.envanter import env
from uav_project.utils.exceptions import EnvironmentVariableNotSet

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str(
    "SECRET_KEY",
    "django-insecure-$z3n69y0*nhhl791&%f&ry)pkr0f9(sr)v6z^__a0*l%%r&2)1",
)

# SECURITY WARNING: don't run with debug turned on in production!
# Its only meant to be used in development.
# For larger project, you can add a multi-layer settings e.g. the DEBUG
# has some level of security, where a second layer of security is
# added like SERVER_TYPE = "development" or "production".
DEBUG = env.bool("DEBUG", False)

if not DEBUG:
    if not (allowed_hosts := env.list("ALLOWED_HOSTS", [])):
        raise EnvironmentVariableNotSet(
            "ALLOWED_HOSTS environment variable is not set."
        )
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", allowed_hosts)


# Application definition

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    "django_json_widget",
    # uav_project apps
    "uav_project",
    "uav_project.user",
    "uav_project.uav",
    "uav_project.rental",
]

AUTH_USER_MODEL = "uav_project_user.UAVUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Third-party middlewares
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "uav_project.urls"

# Rest Framework (DRF) settings
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "uav_project.utils.helpers.PageSizeControllablePaginator",  # noqa: E501
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
    ),
}

# Enabling and disabling the browsable API interface dynamically for
# security reasons.
if ENABLE_BROWSABLE_API := env.bool("ENABLE_BROWSABLE_API", False):
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    )

# CORS settings
if not DEBUG:
    if not (allowed_origins := env.list("CORS_ALLOWED_ORIGINS", [])):
        raise EnvironmentVariableNotSet(
            "CORS_ALLOWED_ORIGINS environment variable is not set."
        )
    CORS_ALLOWED_ORIGINS = allowed_origins
# If debug is enabled (development environment), allow all origins
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_HEADERS = env.list(
    "CORS_ALLOW_HEADERS",
    (
        *default_headers,
        "x-timezone",
    ),
)

MEDIA_ROOT = env.str("MEDIA_ROOT", "/app/tmp/media/")
MEDIA_URL = env.str("MEDIA_URL", "/media/")


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "uav_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
if not env.str("DATABASE_URI", ""):
    raise EnvironmentVariableNotSet(
        "DATABASE_URI environment variable is not set."
    )
DATABASES = {
    "default": dj_database_uri.config(env="DATABASE_URI"),
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = env.str("TIME_ZONE", "UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

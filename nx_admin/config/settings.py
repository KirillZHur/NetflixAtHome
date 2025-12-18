import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

INTERNAL_IPS = os.environ.get("INTERNAL_IPS").split(",")

CORS_ALLOWED_ORIGINS = os.environ.get("ORIGINS").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("ORIGINS").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "movies",
    "django_extensions",
    "corsheaders",
]

if DEBUG:
    INSTALLED_APPS.append(
        "debug_toolbar",
    )


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.append(
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates/"), os.path.join(BASE_DIR, "movies/templates/")],
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

print(os.path.join(BASE_DIR, "templates/"))

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'movies',
        'USER': 'postgres',
        'PASSWORD': '1111',
        'HOST': 'database_nx_admin',
        'PORT': '5432',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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

AUTHENTICATION_BACKENDS = [
    "common.backend.AuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_API = os.environ.get("AUTH_API")

AUTH_USER_MODEL = "movies.CustomUser"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCALE_PATHS = ["movies/locale"]

MINIO_ENDPOINT_URL = os.getenv('MINIO_ENDPOINT', 'http://localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET', 'movies')
MINIO_PUBLIC_BASE = os.getenv('MINIO_PUBLIC_BASE', 'movies')


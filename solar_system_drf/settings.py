from pathlib import Path
import os

# Add these at the top of your settings.py
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

from urllib.parse import urlparse, parse_qsl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-ydg9@pk^+$2r9a=ge(vebf#%_-_wu_@m7qr7yyb%2u4bwd@e1f"
)


# DEBUG = True
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = [
    ".vercel.app",
    "localhost",
    "127.0.0.1",
    # Add your custom domain if you have one
]
DEBUG=True
CSRF_TRUSTED_ORIGINS = [
    "https://*.vercel.app",
    # add your custom domain if you use one
]


# Media files configuration (for image uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Configure static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Enable WhiteNoise for static file compression
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Use default static files storage for Vercel
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Ensure static files are served correctly in production
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

# Make sure your app is in INSTALLED_APPS
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
    "myapp",
    "cloudinary",
    "cloudinary_storage",
]


# Whitenoise configuration
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "myapp.middleware.auth_middleware.AuthMiddleware",
]

# For WhiteNoise: enables efficient static file serving
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (if needed)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

ROOT_URLCONF = "solar_system_drf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "myapp/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "solar_system_drf.wsgi.application"


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }



# Local development database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "solar_system",
        "USER": "postgres",
        "PASSWORD": "admin",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# for the deployment database Neon and for filing upload use cloudinary
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": tmpPostgres.path.replace("/", ""),
        "USER": tmpPostgres.username,
        "PASSWORD": tmpPostgres.password,
        "HOST": tmpPostgres.hostname,
        "PORT": 5432,
        "OPTIONS": dict(parse_qsl(tmpPostgres.query)),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]

# Vercel specific settings
USE_TZ = True
TIME_ZONE = "UTC"

# Disable Django's built-in server in production
if not DEBUG:
    import django
    from django.core.management.commands.runserver import Command as RunserverCommand

    RunserverCommand.default_port = "8000"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


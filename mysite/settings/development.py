from .base import *

import os
from dotenv import load_dotenv

load_dotenv(".env")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("USER_NAME"),
        "PASSWORD": os.getenv("USER_PASSWORD"),
        # Name of docker service running postgres
        "HOST": "db",
        "PORT": os.getenv("DB_PORT"),
    }
}

INSTALLED_APPS += ["silk"]
MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]

DEBUG = True

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")

COOKIE_SAMESITE = "None"
COOKIE_DOMAIN = "localhost"

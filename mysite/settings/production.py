from .base import *
from decouple import Config, RepositoryEnv, Csv
import dj_database_url
from pathlib import Path

config = Config(RepositoryEnv(Path(__file__).resolve().parent.parent.parent / '.env.production'))

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {
    'default': dj_database_url.config(
      default=config('DATABASE_URL'),
      conn_max_age=600,
      conn_health_checks=True,
    )
}

CORS_ALLOWED_ORIGINS = [
  "https://skilltrainer.org",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
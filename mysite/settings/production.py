from .base import *
#from decouple import Config, RepositoryEnv, Csv
from decouple import config, Csv
import dj_database_url
#from pathlib import Path

#Path(__file__).resolve().parent.parent.parent / '.env.production'
#config = Config(RepositoryEnv(Path('/home/deploy/skill-trainer/backend/.env.production')))

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(
      default=config('DATABASE_URL'),
      conn_max_age=6000,
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
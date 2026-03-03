from .base import *
from decouple import Config, RepositoryEnv, Csv
import dj_database_url
from pathlib import Path

config = Config(RepositoryEnv(Path(__file__).resolve().parent.parent.parent / '.env.development'))

DEBUG = True

SECRET_KEY='django-insecure-4f0f04b935445c4aa7f1af689e94c976605bbccb3320d8086efda1be6a1b13aa1a76a8cf761a67285a40d30d7c109369fd36c8a'

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {
    'default': dj_database_url.config(
      default=config('DATABASE_URL'),
      conn_max_age=600,
      conn_health_checks=True,
    )
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
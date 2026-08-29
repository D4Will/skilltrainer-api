import os
from dotenv import load_dotenv

load_dotenv(".env")

environment = os.getenv("DJANGO_ENV")

if environment == "production":
    from .production import *
else:
    from .development import *

from .base import *

DEBUG = config("DEBUG", cast=bool)
ALLOWED_HOSTS = ['ip-address', 'www.your-website.com']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

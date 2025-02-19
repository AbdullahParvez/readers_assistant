from .base import *

DEBUG = config("DEBUG", cast=bool)
ALLOWED_HOSTS = ['www.ampreader.xyz', 'ampreader.xyz','172.104.96.104']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

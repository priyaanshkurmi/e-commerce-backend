from .base import *
import dj_database_url

DEBUG = False

DATABASES = {
    "default": dj_database_url.parse(
        os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.ManifestStaticFilesStorage"

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.ManifestStaticFilesStorage",
        "OPTIONS": {
            "manifest_strict": False,  # Tell Django 6.0 to ignore missing files
        },
    },
}

MEDIA_URL = ""
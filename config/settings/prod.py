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

# (Removed the deprecated STATICFILES_STORAGE variable)

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        # Changed backend to skip compression and avoid the FileNotFoundError
        "BACKEND": "whitenoise.storage.ManifestStaticFilesStorage",
    },
}

MEDIA_URL = ""
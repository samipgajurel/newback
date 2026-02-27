"""
Django settings for backend project.
Production + Docker + MySQL ready
"""

from pathlib import Path
from datetime import timedelta
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# =========================================================
# SECURITY
# =========================================================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

DEBUG = os.getenv("DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True


# =========================================================
# APPLICATIONS
# =========================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party
    "rest_framework",
    "corsheaders",

    # Local apps
    "accounts",
    "internships",
]


# =========================================================
# MIDDLEWARE
# =========================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # static in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "backend.wsgi.application"


# =========================================================
# DATABASE (MySQL - Docker service name = mysql)
# =========================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "interntrack"),
        "USER": os.getenv("DB_USER", "samip"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "mysql"),  # IMPORTANT for docker
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# =========================================================
# PASSWORD VALIDATORS
# =========================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# CORS
# =========================================================
CORS_ALLOW_ALL_ORIGINS = True


# =========================================================
# AUTH
# =========================================================
AUTH_USER_MODEL = "accounts.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# =========================================================
# EMAIL
# =========================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "1") == "1"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)


# =========================================================
# FRONTEND BASE URL
# =========================================================
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:8080")


# =========================================================
# OFFICE GPS VALIDATION (custom feature)
# =========================================================
OFFICE_LAT = float(os.getenv("OFFICE_LAT", "0"))
OFFICE_LNG = float(os.getenv("OFFICE_LNG", "0"))
OFFICE_RADIUS_M = int(os.getenv("OFFICE_RADIUS_M", "100"))

CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "http://localhost:8080,http://127.0.0.1:8080",
    ).split(",")
    if o.strip()
]

ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
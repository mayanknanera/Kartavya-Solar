from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def get_env(key, default=None, cast=None, required=False):
    """Read an environment variable, optionally casting its type."""
    value = os.environ.get(key, default)
    if required and value is None:
        raise ImproperlyConfigured(f"Set the {key} environment variable.")
    if cast and value is not None:
        if cast == bool:
            if isinstance(value, bool):
                return value
            return str(value).lower() in ("true", "1", "yes")
        return cast(value)
    return value


# ── Security ──────────────────────────────────────────────────────────────────

SECRET_KEY = get_env("SECRET_KEY", required=True)
DEBUG = get_env("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = get_env("ALLOWED_HOSTS", default="").split(",") if get_env("ALLOWED_HOSTS") else []

# ── Apps ──────────────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",       # Required by allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "core",
    "accounts",
    "tailwind",
    "theme",
    "django_browser_reload",
]

# ── Auth ──────────────────────────────────────────────────────────────────────

AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# ── Middleware ────────────────────────────────────────────────────────────────

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# ── URLs & Templates ──────────────────────────────────────────────────────────

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.cart_count",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ── Database ──────────────────────────────────────────────────────────────────

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ── Password Validation ───────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── Internationalisation ──────────────────────────────────────────────────────

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ── Static & Media ────────────────────────────────────────────────────────────

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Sites Framework ───────────────────────────────────────────────────────────

SITE_ID = 1  # Required by allauth; Site record is created via migration 0007

# ── Allauth / Login ───────────────────────────────────────────────────────────

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_ADAPTER = "accounts.adapters.CustomAccountAdapter"

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": get_env("GOOGLE_CLIENT_ID", default=""),
            "secret": get_env("GOOGLE_CLIENT_SECRET", default=""),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

# ── Email ─────────────────────────────────────────────────────────────────────

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = get_env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = get_env("EMAIL_PORT", default=587)
EMAIL_USE_TLS = get_env("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = get_env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = get_env("EMAIL_PASSWORD", default="")
DEFAULT_FROM_EMAIL = get_env("DEFAULT_FROM_EMAIL", default="")
SERVER_EMAIL = get_env("EMAIL_HOST_USER", default="")
EMAIL_TIMEOUT = 10

# ── Tailwind ──────────────────────────────────────────────────────────────────

TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = ["127.0.0.1"]
NPM_BIN_PATH = get_env("NPM_BIN_PATH", default="npm")

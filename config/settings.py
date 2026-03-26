from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / '.env')

# Helper function to get environment variables
def get_env(key, default=None, cast=None):
    value = os.environ.get(key, default)
    if cast and value is not None:
        if cast == bool:
            # Handle boolean conversion
            if isinstance(value, bool):
                return value
            return str(value).lower() in ('true', '1', 'yes')
        return cast(value)
    return value

# security
SECRET_KEY = get_env('SECRET_KEY', default="django-insecure-b4vpfgnn*t-cvda59n^$=+fh#by6s%-k+3c%y#cp!qo))@8am$")
DEBUG = get_env('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = []

# apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

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

# auth
AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# middleware
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

# urls / templates
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

# database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'solar_db', # Your PostgreSQL database name
        'USER': 'admin',    # Your PostgreSQL username
        'PASSWORD': 'admin',  # Your PostgreSQL password
        'HOST': 'localhost',    # Usually 'localhost' for local development
        'PORT': '', # Leave blank for default port 5432
    }
}


# password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# i18n
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# static / media
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# sites
SITE_ID = 1

# account
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None

SOCIALACCOUNT_LOGIN_ON_GET = True

# New allauth settings (updated syntax)
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = "optional"

# Custom adapter for handling redirects after social login
ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'

# social
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

# Email Configuration
# SMTP backend for sending actual emails (OTP, contact form)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# SMTP Configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', default='mayank73463@gmail.com')
EMAIL_HOST_PASSWORD = get_env('EMAIL_PASSWORD', default='')
DEFAULT_FROM_EMAIL = get_env('DEFAULT_FROM_EMAIL', default='Kartavya Solar <mayank73463@gmail.com>')
SERVER_EMAIL = get_env('EMAIL_HOST_USER', default='mayank73463@gmail.com')

# Email timeout settings
EMAIL_TIMEOUT = 10  # seconds

# tailwind
TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = ["127.0.0.1"]
NPM_BIN_PATH = "/home/raghu/.nvm/versions/node/v24.12.0/bin/node"

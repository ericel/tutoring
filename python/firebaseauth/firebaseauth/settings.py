"""
Django settings for firebaseauth project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-^pyffvm8anf8&h6!i@lwli&7(7!!-iv446s_v4v*3cv!e_jy#e"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "*"
]

# Google Cloud Certificate
SERVICE_ACCOUNT_PATH = 'firebaseauth/service_account.json' # Your firebase service account path

# Firebase Admin credentials
if not firebase_admin._apps:
    # FIREBASE SETTINGS
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    
    # cred = credentials.ApplicationDefault()
    default_app = firebase_admin.initialize_app(
        cred, {"projectId": "[PROJECTID]", "storageBucket": "[PROJECTID].appspot.com"}
    )
firestore = firestore.client()

# allow IFRAME
X_FRAME_OPTIONS = 'LOCALHOST'#'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

# CSRF_TRUSTED_ORIGINS = ['https://*.mydomain.com','https://*.127.0.0.1','https://*.localhost']
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
CSRF_TRUSTED_ORIGINS = [
    "http://*.127.0.0.1",
    "http://*.localhost",
]
# GOOGLE client ID useful for Google Identity Login
GOOGLE_CLIENT_ID = (
    "[ENTER YOUR GOOGLE IDENTITY WEB API KEY]" 
)


# Authentication settings
AUTH_USER_MODEL = "account.CustomUser" # Use CustomUser because we are making use of external auth apis
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/login"
LOGOUT_REDIRECT_URL = "/"
CONTEXT_PROCESSORS = "django.contrib.auth.context_processors.auth"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "account",
    "rest_framework"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Cors Headers App
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    # End Cors Headers App
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "firebaseauth.urls"
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "firebaseauth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# DRF Auth Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        # UnicodeJSONRenderer has an ensure_ascii = False attribute,
        # thus it will not escape characters.
        "rest_framework.renderers.JSONRenderer",
        # You only need to keep this one if you're using the browsable API
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "firebaseauth-files-static")
STATICFILES_DIRS = [
    # TODO: configure the name and path to your development static directory
    os.path.join(BASE_DIR, "static")
]

MEDIA_URL = "/media/"  # django-storages
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = False
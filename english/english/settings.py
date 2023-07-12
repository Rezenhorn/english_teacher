import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("../infra/.env")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "default-key")

DEBUG = os.getenv("DEBUG", False) == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split()


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "about.apps.AboutConfig",
    "core.apps.CoreConfig",
    "students.apps.StudentsConfig",
    "dictionary.apps.DictionaryConfig",
    "users.apps.UsersConfig",
    "quiz.apps.QuizConfig",
    "django_bootstrap5",
    "bootstrap_datepicker_plus"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "english.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "english.wsgi.application"

if not DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.getenv("DB_NAME", "postgres"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "db"),
            "PORT": os.getenv("DB_PORT", "5432")
        }
    }

    if os.environ.get("GITHUB_WORKFLOW"):
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "github_actions",
                "USER": "postgres",
                "PASSWORD": "postgres",
                "HOST": "127.0.0.1",
                "PORT": "5432",
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]
else:
    STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "about:index"

AUTH_USER_MODEL = "users.User"

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

HOMEWORK_PER_PAGE = 10
PROGRESS_PER_PAGE = 30
DICTIONARY_WORDS_PER_PAGE = 30

CSRF_FAILURE_VIEW = "core.views.csrf_failure"

DATE_INPUT_FORMATS = "DD.MM.YYYY"

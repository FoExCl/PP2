"""Django settings for Ely_BABY project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import inspect
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y+vy50*evcx!4$fxgs#%zq*271ehwkqsg+4*&v%3k@=_vbyx$g'

# SECURITY WARNING: don't run with debug turned on in production!7
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
#DEBUG = True

PORT= int(os.getenv("PORT", 8000))
HOST= os.getenv("HOST", "0.0.0.0")
#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ["*",".cleverapps.io", "app_3c083f94-d650-4192-b569-c77573a0b109"]
CSRF_TRUSTED_ORIGINS=["https://*.cleverapps.io","https://app_3c083f94-d650-4192-b569-c77573a0b109.cleverapps.io"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # aplicaciones instaladas/hechas
    'django_bootstrap5',
    'loginApp',
    "crispy_forms",
    "crispy_bootstrap5",
    "InventarioApp",
    "CajaApp",
    "VentasApp",
    "GraficosApp",

]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Ely_BABY.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ely_BABY.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.mysql',
    #    'NAME': 'bjvhcp3oyzg8gz8rofmk',
    #    'USER': 'ujnhca2f8jmcyl9u',
    #    'PASSWORD': '49RmrZ3zD5XYeviq72Mx',
    #    'HOST': 'bjvhcp3oyzg8gz8rofmk-mysql.services.clever-cloud.com',
    #    'PORT': '3306'
    #}
    "default": dj_database_url.config(default=os.getenv("CC_Connection_URL_DB"))
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'elybabyapp@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'bqmz vods ynui jwfd'  # Your email password or app password
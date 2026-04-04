import os
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-e7y2svjrg+u-1s+$*@u_vkemd=j_%*uvk&+76)_9ii94xip#31'

DEBUG = True
ALLOWED_HOSTS = ['*']

APPEND_SLASH = True 

INSTALLED_APPS = [
    'jazzmin', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app',
    'phone_field',
    'django_google_maps'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'A1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'A1.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === JAZZMIN SETTINGS (UPDATED FOR EASY ADMIN CREATION) ===

JAZZMIN_SETTINGS = {
    "site_title": "A1 Bakery Admin",
    "site_header": "A1 Bakery",
    "site_brand": "A1 Bakery",
    "welcome_sign": "Welcome, Owner!",
    "copyright": "A1 Bakery Ltd",
    "search_model": "main_app.Product",
    "logout_link": "logout", 
    
    "hide_models": ["auth.group"], 

    "topmenu_links": [
        {"name": "Open Website", "url": "home", "permissions": ["auth.view_user"]},
    ],

    "icons": {
        "auth.user": "fas fa-user-shield",
        "main_app.Product": "fas fa-birthday-cake",
        "main_app.Order": "fas fa-shopping-cart",
        "main_app.Feedback": "fas fa-star",
    },
}


JAZZMIN_UI_TWEAKS = {
    "theme": "darkly", 
    "navbar": "navbar-dark", 
    "sidebar": "sidebar-dark-warning", 
    "accent": "accent-warning",
    "sidebar_nav_child_indent": True,
    "button_classes": {
        "primary": "btn-warning",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
        
    }
}

LOGOUT_ON_GET = True
LOGIN_REDIRECT_URL = '/order/'
LOGOUT_REDIRECT_URL = '/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
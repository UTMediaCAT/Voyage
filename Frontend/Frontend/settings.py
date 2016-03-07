"""
Django settings for Frontend project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+r!(k=mpt5oe*i&ghi%fg$&&veh(rg2f2=rd#tnb8+@!pisf6u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'home',
    'articles',
    'tweets',
    'explorer',
    'statistics',
    'options',
    'visualizations',
    'advanced_filters',
    'easy_select2'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Frontend.urls'

WSGI_APPLICATION = 'Frontend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    'ADMIN_NAME': 'Voyage',

    'SEARCH_URL': '/admin/articles/article/',

    'MENU': (
        {'label': 'Scope', 'icon':'icon-screenshot', 
         'models': ('explorer.referringsite', 'explorer.referringtwitter', 'explorer.sourcesite', 'explorer.sourcetwitter', 'explorer.keyword')},
        
        {'label': 'Data', 'icon':'icon-book', 'models': ('articles.article', 'tweets.tweet')},

        {'label': 'Downloads', 'icon':'icon-download', 'url': '/options/downloads'},

        {'label': 'Statistics', 'icon':'icon-signal', 'models': (
            {'label': 'Articles', 'url': '/statistics/articles'},
            {'label': 'Tweets', 'url': '/statistics/tweets'},
        )},

        {'label': 'Visualizations', 'icon':'icon-fullscreen', 'models': (
            {'label': 'Article - Source Site', 'url': '/visualizations/article_hypertree'},
            {'label': 'Article - Keyword', 'url': '/visualizations/article_spacetree'},
            {'label': 'Article - Weighted', 'url': '/visualizations/article_weightedtree'},
            {'label': 'Article - Movable', 'url': '/visualizations/article_forcegraph'},
            {'label': 'Tweet - Source Site', 'url': '/visualizations/tweet_hypertree'},
            {'label': 'Tweet - Keyword', 'url': '/visualizations/tweet_spacetree'},
            {'label': 'Tweet - Weighted', 'url': '/visualizations/tweet_weightedtree'},
            {'label': 'Tweet - Movable', 'url': '/visualizations/tweet_forcegraph'},
        )},

        {'label': 'Authorization', 'icon':'icon-lock', 'models': ('auth.user', 'auth.group')},
    )
}

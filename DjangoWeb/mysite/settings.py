"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bw%mdhze-+o)4p7)jl^beo)^8qf0pda+nuxy77eh52lz_(q_n+'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG가True이고 ALLOWED_HOSTS가 비어 있으면, 호스트는 ['localhost', '127.0.0.1', '[::1]']에 대해서 유효합니다.
DEBUG = False
# DEBUG = os.environ.get('DEBUG', False)

# open to all
ALLOWED_HOSTS = ['*', '0.0.0.0', 'loadbalancer', 'web_app']
# ALLOWED_HOSTS = [os.environ.get('HOST', '*'), ]
API_HOST = os.environ.get('API_HOST', 'localhost:8000')

# USE_X_FORWARDED_HOST=True
# Application definition
# 애플리케이션을 생성한 후 장고에 사용해야 한다고 알려줘야 합니다. 이 역할을 하는 파일이 recsys/settings.py입니다.
# 앱을 현재의 프로젝트에 포함시키기 위해서는, 앱의 구성 클래스에 대한 참조를 INSTALLED_APPS 설정에 추가해야 합니다.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'item2vec',
    'mysite',
    'corsheaders',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]


##CORS
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)


ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ko'

# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = 'Asia/Seoul' #'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

""" 
이건 DEBUG = True 일때는 무시됨. 
STATIC_ROOT는 실 서비스 환경을 위한 설정 항목
그래서 개발 과정에선 STATIC_ROOT에 지정한 경로가 실제로 존재하지 않거나 아예 STATIC_ROOT 설정 항목 자체가 없어도 문제없이 동작함.

"""
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

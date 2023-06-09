"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'daphne',
    'chat',
    'accounts',
    'corsheaders',
    'reviews',
    'studies',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_htmx',
    'storages',
    'taggit',
    'multiselectfield',
    'rest_framework',

    # allauth
    'django.contrib.sites',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # social providers
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
]

TUI_EDITOR_LANGUAGE = ['ko']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    'config.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.alarm',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# localtime 사용
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'accounts.User'

# django-taggit
TAGGIT_CASE_INSENSITIVE = True


# django-taggit customization (config/utils.py 참고)
TAGGIT_TAGS_FROM_STRING = 'config.utils.custom_tag_string'
TAGGIT_STRING_FROM_TAGS = 'config.utils.space_joiner'

# -------- allauth --------
## secret
GITHUB_SECRET_KEY = os.getenv('GITHUB_SECRET_KEY')
GOOGLE_EMAIL_SECRET_KEY = os.getenv('GOOGLE_EMAIL_SECRET_KEY')

## social setting
AUTHENTICATION_BACKENDS = (
    # 장고 기본 사용자 인증 백엔드
    'django.contrib.auth.backends.ModelBackend',

    # allauth를 사용한 인증 백엔드
    "allauth.account.auth_backends.AuthenticationBackend",
)

SOCIALACCOUNT_PROVIDERS = {
    'github' : {
        'APP' : {
            'client_id': '21fdc27a6953e4613324',
            'secret': GITHUB_SECRET_KEY,
            'key': '',
        }
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SITE_ID = 1

# 로그인 시 유저네임, 이메일 모두 인증 가능
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

## 로그인 성공 시 리다이렉트할 경로
LOGIN_REDIRECT_URL = "/studies"

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True

## 소셜 로그인 후 바로 가입이 아닌 부가정보를 입력받기 위한 옵션
SOCIALACCOUNT_AUTO_SIGNUP = False

## 부가정보 자동 입력을 위한 Adpater 연결
SOCIALACCOUNT_ADAPTER = 'accounts.adapters.CustomSocialAccountAdapter'

ACCOUNT_EMAIL_REQUIRED = True
# 회원가입 메일 인증 관련
## 회원가입 시 이메일 인증 여부
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
## get 방식으로 email 인증에 접속했을 때 허용시켜주는 옵션
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True

## 이메일 전송
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"  # 메일 호스트 서버
EMAIL_PORT = 587  # gmail과 통신하는 포트
EMAIL_HOST_USER = 'altudy12@gmail.com'  # 발신할 이메일 주소
EMAIL_HOST_PASSWORD = GOOGLE_EMAIL_SECRET_KEY  # 발신할 메일의 비밀번호
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[altudy]'
EMAIL_USE_TLS = True  # TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 사이트와 관련한 자동응답 받을 이메일 주소

# -------- end allauth --------

# Celery CRONJOB
from celery.schedules import crontab

CELERY_TIMEZONE = 'Asia/Seoul'

CELERY_BEAT_SCHEDULE = {
    'remove-unused-tags-every-day': {
        'task': 'reviews.tasks.remove_unused_tags',
        'schedule': crontab(hour=5, minute=0),
    },
    # 'check-if-beat-is-up-and-running': {
    #     'task': 'reviews.tasks.check_beat',
    #     'schedule': 20,
    # },
}

# django-cors-headers
CORS_ALLOWED_ORIGINS = [
    'http://43.202.59.123',
]

# For daphne
ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# 비동기 함수에서의 ORM 작성
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'

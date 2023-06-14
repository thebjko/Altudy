from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xp!@&&qeef7p9uf996hlb5h#@n@04(aeqc=yo553=!h#h1^c4v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# 개발환경에서 진행시 sqlite3 또는 로컬 MySQL 서버를 사용하도록 수정
if 'MYSQL_PASSWORD' in os.environ and 'MYSQL_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DB_NAME'),
            'USER': 'root',
            'PASSWORD': os.getenv('MYSQL_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }


# Django debug toolbar 관련
INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = [
    '127.0.0.1',
]

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
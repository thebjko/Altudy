from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Django 프로젝트의 설정 모듈을 'celery' 프로그램의 기본 설정으로 설정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('config')

# 여기서 Celery 설정은 Django의 설정을 사용합니다.
# 'CELERY'라는 네임스페이스에서 시작하는 모든 구성 키를 사용합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱을 위한 Celery를 자동으로 로드합니다.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


'''
RabbitMQ 설치 및 실행
brew install rabbitmq
export PATH=$PATH:/usr/local/sbin
rabbitmq-server (또는 brew services start/stop rabbitmq)

MacOS does not have Supervisor pre-installed but there's an alternative called launchd - native service management framework for MacOS.
'''
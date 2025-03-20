import os
from celery import Celery

# Django 설정 모듈 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heyb.settings')

app = Celery('heyb')

# Django 설정에서 Celery 관련 설정 가져오기
app.config_from_object('django.conf:settings', namespace='CELERY')

# 등록된 Django 앱에서 task 자동 로드
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 
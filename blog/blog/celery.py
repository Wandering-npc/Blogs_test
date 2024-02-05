import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
app = Celery('blog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# app.conf.broker_url = 'redis://redis:6379/0'
# app.conf.result_backend = 'redis://redis:6379/0'
app.conf.beat_schedule = {
    'send_email_digest_daily': {
        'task': 'app.blog.tasks.send_email_digest',
        'schedule': crontab(hour=19, minute=11),
    },
}

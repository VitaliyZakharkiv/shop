import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

app = Celery('shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'send_report_every_month': {
#         'task': 'profil.tasks.send_message_on_email',
#         'schedule': crontab(minute='*/2'),
#     }
# }

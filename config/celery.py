import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("gotchacoins")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# celery -A config.celery worker -E -l info
# celery -A config.celery beat -l info

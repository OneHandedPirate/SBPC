import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SamberiPriceCheckerProject.settings')
app = Celery("SamberiPriceCheckerProject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(['pricechecker'])
app.conf.broker_pool_limit = 10
app.conf.broker_transport_options = {'visibility_timeout': 3600}

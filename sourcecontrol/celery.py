from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sourcecontrol.settings')

app = Celery('sourcecontrol', broker='redis://redistogo:a2f5069ceb48214b7c19d69c5f636181@greeneye.redistogo.com:10102/')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

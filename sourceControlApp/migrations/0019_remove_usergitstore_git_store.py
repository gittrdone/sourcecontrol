# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0018_auto_20141123_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergitstore',
            name='git_store',
        ),
    ]

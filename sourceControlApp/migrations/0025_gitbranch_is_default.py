# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0024_auto_20141214_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitbranch',
            name='is_default',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0004_auto_20141207_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='desc',
            field=models.CharField(default=b'', max_length=1024),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_auto_20141120_0606'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='chart_type',
            field=models.CharField(default=b'Pie', max_length=4, choices=[(b'pie', b'Pie'), (b'bar', b'Bar'), (b'line', b'Line')]),
            preserve_default=True,
        ),
    ]

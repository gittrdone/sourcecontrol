# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0003_query_chart_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='chart_type',
            field=models.CharField(default=b'pie', max_length=4, choices=[(b'pie', b'Pie'), (b'bar', b'Bar'), (b'line', b'Line')]),
        ),
    ]

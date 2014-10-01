# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repoManager', '0003_auto_20140930_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitstore',
            name='repoName',
            field=models.CharField(max_length=30),
        ),
    ]

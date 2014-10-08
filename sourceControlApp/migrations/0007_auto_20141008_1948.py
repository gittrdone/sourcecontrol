# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0006_auto_20141001_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitstore',
            name='repoDescription',
            field=models.CharField(default=b'', max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gitstore',
            name='repoName',
            field=models.CharField(max_length=100),
        ),
    ]

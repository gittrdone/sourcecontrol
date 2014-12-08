# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0021_auto_20141207_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitrepo',
            name='jenkins_url',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gitrepo',
            name='job_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]

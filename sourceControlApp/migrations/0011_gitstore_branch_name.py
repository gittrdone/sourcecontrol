# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0010_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitstore',
            name='branch_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]

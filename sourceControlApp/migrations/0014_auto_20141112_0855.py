# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0013_auto_20141110_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='codeauthor',
            name='additions',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='codeauthor',
            name='deletions',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

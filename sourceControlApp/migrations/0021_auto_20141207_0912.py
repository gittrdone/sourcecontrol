# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0020_auto_20141207_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergitstore',
            name='num_break_build',
        ),
        migrations.AddField(
            model_name='codeauthor',
            name='num_break_build',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

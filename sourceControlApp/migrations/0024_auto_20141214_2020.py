# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0023_auto_20141209_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='codeauthor',
            name='num_build',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='codeauthor',
            name='num_fix_build',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

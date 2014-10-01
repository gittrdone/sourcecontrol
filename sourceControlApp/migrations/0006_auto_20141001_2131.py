# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0005_auto_20141001_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codeauthor',
            name='repo',
        ),
        migrations.AddField(
            model_name='codeauthor',
            name='repository',
            field=models.ForeignKey(default=-1, to='sourceControlApp.GitStore'),
            preserve_default=False,
        ),
    ]

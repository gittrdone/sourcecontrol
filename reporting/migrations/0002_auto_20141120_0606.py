# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0014_auto_20141112_0855'),
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='user',
            field=models.ForeignKey(default=None, to='sourceControlApp.SourceControlUser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='repo',
            field=models.ForeignKey(default=0, to='sourceControlApp.UserGitStore'),
            preserve_default=False,
        ),
    ]

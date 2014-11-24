# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0016_auto_20141119_0343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeauthor',
            name='repository',
            field=models.ForeignKey(blank=True, to='sourceControlApp.GitStore', null=True),
        ),
        migrations.AlterField(
            model_name='commit',
            name='repository',
            field=models.ForeignKey(blank=True, to='sourceControlApp.GitStore', null=True),
        ),
        migrations.AlterField(
            model_name='usergitstore',
            name='git_store',
            field=models.ForeignKey(blank=True, to='sourceControlApp.GitStore', null=True),
        ),
    ]

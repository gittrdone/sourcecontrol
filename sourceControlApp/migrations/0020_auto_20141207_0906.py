# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0019_remove_usergitstore_git_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='break_build_status',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitrepo',
            name='jenkins_url',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gitrepo',
            name='job_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usergitstore',
            name='num_break_build',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

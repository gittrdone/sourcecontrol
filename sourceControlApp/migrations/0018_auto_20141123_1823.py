# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0017_auto_20141119_0507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commit',
            name='git_branch',
        ),
        migrations.AddField(
            model_name='commit',
            name='branches',
            field=models.ManyToManyField(to='sourceControlApp.GitBranch'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commit',
            name='commit_id',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commit',
            name='git_repo',
            field=models.ForeignKey(blank=True, to='sourceControlApp.GitRepo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitrepo',
            name='num_commits',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

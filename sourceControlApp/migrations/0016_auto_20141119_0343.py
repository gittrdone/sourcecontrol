# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0015_gitbranch_gitrepo'),
    ]

    operations = [
        migrations.AddField(
            model_name='codeauthor',
            name='git_branch',
            field=models.ForeignKey(blank=True, to='sourceControlApp.GitBranch', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commit',
            name='git_branch',
            field=models.ForeignKey(blank=True, to='sourceControlApp.GitBranch', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usergitstore',
            name='git_repo',
            field=models.ForeignKey(blank=True, to='sourceControlApp.GitRepo', null=True),
            preserve_default=True,
        ),
    ]

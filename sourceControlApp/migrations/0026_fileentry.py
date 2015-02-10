# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0025_gitbranch_is_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=300)),
                ('additions', models.IntegerField(default=0)),
                ('deletions', models.IntegerField(default=0)),
                ('num_edit', models.IntegerField(default=0)),
                ('in_current_built', models.BooleanField(default=False)),
                ('git_branch', models.ForeignKey(to='sourceControlApp.GitBranch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

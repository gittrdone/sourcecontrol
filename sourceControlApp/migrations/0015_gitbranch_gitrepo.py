# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0014_auto_20141112_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitBranch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('git_repository_url', models.CharField(max_length=300)),
                ('branch_name', models.CharField(max_length=50)),
                ('num_files', models.IntegerField(default=0)),
                ('num_commits', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GitRepo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('git_repository_url', models.CharField(max_length=300)),
                ('status', models.IntegerField(default=0)),
                ('branches', models.ManyToManyField(to='sourceControlApp.GitBranch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

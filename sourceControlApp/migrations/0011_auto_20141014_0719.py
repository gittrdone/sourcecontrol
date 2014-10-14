# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0010_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGitStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('repo_description', models.CharField(max_length=1000)),
                ('git_store', models.ForeignKey(to='sourceControlApp.GitStore')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='gitstore',
            name='repoDescription',
        ),
        migrations.RemoveField(
            model_name='gitstore',
            name='repoName',
        ),
        migrations.AddField(
            model_name='gitstore',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gitstore',
            name='gitRepositoryURL',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='sourcecontroluser',
            name='ownedRepos',
            field=models.ManyToManyField(to=b'sourceControlApp.UserGitStore'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0004_auto_20141001_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('num_commits', models.IntegerField(default=0)),
                ('repo', models.ManyToManyField(to='sourceControlApp.GitStore')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gitstore',
            name='numCommits',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0006_auto_20141001_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commit_time', models.DateTimeField()),
                ('author', models.ForeignKey(to='sourceControlApp.CodeAuthor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Patch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('addition', models.IntegerField(default=0)),
                ('deletion', models.IntegerField(default=0)),
                ('next', models.ForeignKey(blank=True, to='sourceControlApp.Patch', null=True)),
                ('repository', models.ForeignKey(to='sourceControlApp.GitStore')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='commit',
            name='repository',
            field=models.ForeignKey(to='sourceControlApp.GitStore'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gitstore',
            name='repoDescription',
            field=models.CharField(default=b'', max_length=1000, null=True, blank=True),
        ),
    ]

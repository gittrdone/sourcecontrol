# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repoManager', '0002_sourcecontroluser'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitstore',
            name='repoDescription',
            field=models.CharField(default=b'', max_length=1000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitstore',
            name='repoName',
            field=models.CharField(max_length=30, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sourcecontroluser',
            name='ownedRepos',
            field=models.ManyToManyField(to='repoManager.GitStore'),
            preserve_default=True,
        ),
    ]

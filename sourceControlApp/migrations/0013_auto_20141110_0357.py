# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0012_gitstore_branch_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitstore',
            name='branch_list',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commit',
            name='patches',
            field=models.ManyToManyField(to=b'sourceControlApp.Patch', null=True, blank=True),
        ),
    ]

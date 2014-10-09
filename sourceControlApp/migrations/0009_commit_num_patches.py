# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0008_commit_patches'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='num_patches',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

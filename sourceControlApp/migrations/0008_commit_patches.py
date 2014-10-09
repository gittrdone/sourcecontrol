# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0007_auto_20141008_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='patches',
            field=models.ManyToManyField(to='sourceControlApp.Patch'),
            preserve_default=True,
        ),
    ]

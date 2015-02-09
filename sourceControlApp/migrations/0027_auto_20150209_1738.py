# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0026_fileentry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileentry',
            old_name='file_name',
            new_name='file_path',
        ),
    ]

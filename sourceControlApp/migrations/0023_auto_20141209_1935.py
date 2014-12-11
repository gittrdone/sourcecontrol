# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sourceControlApp', '0022_auto_20141207_0917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gitrepo',
            old_name='job_name',
            new_name='jenkins_job_name',
        ),
    ]

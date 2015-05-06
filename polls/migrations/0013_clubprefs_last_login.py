# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20150501_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubprefs',
            name='last_login',
            field=models.IntegerField(default=0),
        ),
    ]

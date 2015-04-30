# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20150415_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubprefs',
            name='club_name',
        ),
    ]

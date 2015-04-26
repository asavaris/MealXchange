# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20150402_0214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubprefs',
            name='choice_text',
        ),
        migrations.RemoveField(
            model_name='clubprefs',
            name='votes',
        ),
    ]

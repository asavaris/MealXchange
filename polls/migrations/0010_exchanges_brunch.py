# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20150430_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchanges',
            name='brunch',
            field=models.IntegerField(default=0),
        ),
    ]

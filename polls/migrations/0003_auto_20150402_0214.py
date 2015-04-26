# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20150402_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchanges',
            name='month',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]

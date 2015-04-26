# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20150402_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchanges',
            name='month',
            field=models.DateTimeField(default=4),
        ),
    ]

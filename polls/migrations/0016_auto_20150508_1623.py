# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_confirmguest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchanges',
            name='month',
            field=models.IntegerField(default=5),
        ),
    ]

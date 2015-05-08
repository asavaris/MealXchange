# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_auto_20150508_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmexchange',
            name='hostClub',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AddField(
            model_name='confirmexchange',
            name='meal',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AddField(
            model_name='confirmexchange',
            name='month',
            field=models.IntegerField(default=5),
        ),
    ]

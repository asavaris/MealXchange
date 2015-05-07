# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_clubprefs_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmexchange',
            name='guest',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AddField(
            model_name='confirmexchange',
            name='host',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]

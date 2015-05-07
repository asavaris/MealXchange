# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20150506_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmGuest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostHasConfirmed', models.BooleanField(default=False)),
                ('host', models.CharField(default=b'', max_length=30)),
                ('hostConfirmString', models.CharField(default=b'', max_length=100)),
            ],
        ),
    ]

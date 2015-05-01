# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_exchanges_brunch'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmExchange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostConfirm', models.BooleanField(default=False)),
                ('guestConfirm', models.BooleanField(default=False)),
                ('exchange_str', models.CharField(default=b'', max_length=b'400')),
            ],
        ),
        migrations.AlterField(
            model_name='exchanges',
            name='month',
            field=models.DateTimeField(default=5),
        ),
    ]

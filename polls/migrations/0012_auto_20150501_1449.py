# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20150501_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='confirmexchange',
            old_name='guestConfirm',
            new_name='guestHasConfirmed',
        ),
        migrations.RenameField(
            model_name='confirmexchange',
            old_name='hostConfirm',
            new_name='hostHasConfirmed',
        ),
        migrations.AddField(
            model_name='confirmexchange',
            name='guestConfirmString',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='confirmexchange',
            name='hostConfirmString',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='confirmexchange',
            name='exchange_str',
            field=models.CharField(default=b'', max_length=400),
        ),
    ]

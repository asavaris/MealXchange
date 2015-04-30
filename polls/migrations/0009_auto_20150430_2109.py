# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exchanges',
            old_name='club2',
            new_name='guestClub',
        ),
        migrations.RenameField(
            model_name='exchanges',
            old_name='name2',
            new_name='guestName',
        ),
        migrations.RenameField(
            model_name='exchanges',
            old_name='club1',
            new_name='hostClub',
        ),
        migrations.RenameField(
            model_name='exchanges',
            old_name='name1',
            new_name='hostName',
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='club_name',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20150402_2207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clubprefs',
            old_name='maxguests',
            new_name='max_guests',
        ),
        migrations.RemoveField(
            model_name='clubprefs',
            name='btime',
        ),
        migrations.RemoveField(
            model_name='clubprefs',
            name='club',
        ),
        migrations.RemoveField(
            model_name='clubprefs',
            name='dtime',
        ),
        migrations.RemoveField(
            model_name='clubprefs',
            name='ltime',
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='b_end',
            field=models.TimeField(default=b'00:00'),
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='b_start',
            field=models.TimeField(default=b'00:00'),
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='br_end',
            field=models.TimeField(default=b'00:00'),
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='br_start',
            field=models.TimeField(default=b'00:00'),
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='club_name',
            field=models.CharField(default=b'name', max_length=30),
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='d_end',
            field=models.TimeField(default=b'00:00'),
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='d_start',
            field=models.TimeField(default=b'00:00'),
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='l_end',
            field=models.TimeField(default=b'00:00'),
        ),
        migrations.AddField(
            model_name='clubprefs',
            name='l_start',
            field=models.TimeField(default=b'00:00'),
        ),
    ]

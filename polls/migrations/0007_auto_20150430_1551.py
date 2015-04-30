# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20150415_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubprefs',
            name='club_name',
        ),
        migrations.AlterField(
            model_name='clubprefs',
            name='b_end',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='clubprefs',
            name='b_start',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='clubprefs',
            name='br_end',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='clubprefs',
            name='br_start',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='clubprefs',
            name='d_end',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='clubprefs',
            name='d_start',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='clubprefs',
            name='l_end',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='clubprefs',
            name='l_start',
            field=models.TimeField(default='00:00'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClubPrefs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('club', models.CharField(max_length=30)),
                ('btime', models.CharField(max_length=30)),
                ('ltime', models.CharField(max_length=30)),
                ('dtime', models.CharField(max_length=30)),
                ('maxguests', models.IntegerField(default=0)),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Exchanges',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name1', models.CharField(max_length=30)),
                ('club1', models.CharField(max_length=30)),
                ('name2', models.CharField(max_length=30)),
                ('club2', models.CharField(max_length=30)),
                ('breakfast', models.IntegerField(default=0)),
                ('lunch', models.IntegerField(default=0)),
                ('dinner', models.IntegerField(default=0)),
                ('month', models.DateTimeField(verbose_name=b'month')),
            ],
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('club', models.CharField(max_length=30)),
                ('year', models.IntegerField(default=0)),
                ('netID', models.CharField(max_length=30)),
                ('numguests', models.IntegerField(default=0)),
            ],
        ),
    ]

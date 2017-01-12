# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-10 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loggers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ses_id', models.IntegerField()),
            ],
            options={
                'db_table': 'loggers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ses_id', models.IntegerField()),
                ('msg', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'messages',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_id', models.IntegerField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('t_ms', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('lat_pos', models.CharField(max_length=1)),
                ('longitude', models.FloatField()),
                ('lon_pos', models.CharField(max_length=1)),
                ('course', models.FloatField()),
                ('gps_altitude', models.FloatField()),
                ('speed', models.FloatField()),
                ('temperature', models.IntegerField()),
                ('pressure', models.IntegerField()),
                ('gps_state', models.IntegerField()),
                ('sat_num', models.IntegerField()),
                ('ses_id', models.IntegerField()),
            ],
            options={
                'db_table': 'packages',
                'managed': False,
            },
        ),
    ]

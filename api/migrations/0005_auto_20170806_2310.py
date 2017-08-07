# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-06 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_landmark_indoor_nav'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landmark',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='landmark',
            name='long',
            field=models.FloatField(default=0),
        ),
    ]

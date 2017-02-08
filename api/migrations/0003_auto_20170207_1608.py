# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 00:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170207_2303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='landmark',
            old_name='nw_coord_lat',
            new_name='ctr_coord_lat',
        ),
        migrations.RenameField(
            model_name='landmark',
            old_name='nw_coord_long',
            new_name='ctr_coord_long',
        ),
        migrations.RemoveField(
            model_name='landmark',
            name='se_coord_lat',
        ),
        migrations.RemoveField(
            model_name='landmark',
            name='se_coord_long',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-29 16:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_merge_20170729_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landmark',
            name='indoor_nav',
        ),
    ]

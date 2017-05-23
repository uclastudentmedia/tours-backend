# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 23:46
from __future__ import unicode_literals

from django.db import migrations
import sortedm2m.fields
from sortedm2m.operations import AlterSortedManyToManyField


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20170517_0149'),
    ]

    operations = [
        AlterSortedManyToManyField(
            model_name='tour',
            name='landmarks',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='api.Landmark', verbose_name='list of landmarks'),
        ),
    ]

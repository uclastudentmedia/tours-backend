# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-08 07:25
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indoor', '0004_auto_20170706_0635'),
    ]

    operations = [
        migrations.CreateModel(
            name='POI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('type', models.CharField(max_length=80)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.DeleteModel(
            name='Point',
        ),
    ]
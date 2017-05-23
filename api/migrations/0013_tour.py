# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-16 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_landmark_photo_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('distance', models.FloatField()),
                ('duration', models.DurationField()),
                ('landmarks', models.ManyToManyField(to='api.Landmark', verbose_name='list of landmarks')),
            ],
        ),
    ]
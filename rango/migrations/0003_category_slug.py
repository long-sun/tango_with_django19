# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 16:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20160610_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2016, 6, 12, 16, 49, 39, 337295, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-04 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reuse', '0006_auto_20160831_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='score',
            field=models.IntegerField(default='0'),
        ),
    ]
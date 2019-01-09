# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-29 14:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reuse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pswd_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pswd', models.CharField(default='123456', max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='guest',
            name='pswd',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='reuse.Pswd_table'),
        ),
    ]
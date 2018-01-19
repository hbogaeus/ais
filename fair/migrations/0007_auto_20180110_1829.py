# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-10 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0006_auto_20170831_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fair',
            name='description',
            field=models.TextField(default='Armada 2018', max_length=500),
        ),
        migrations.AlterField(
            model_name='fair',
            name='name',
            field=models.CharField(default='Armada 2018', max_length=100),
        ),
        migrations.AlterField(
            model_name='fair',
            name='year',
            field=models.IntegerField(default=2018),
        ),
    ]
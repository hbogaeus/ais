# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-05 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_profiles', '0009_auto_20171105_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='nickname',
            field=models.CharField(blank=True, default='Student', max_length=512),
        ),
    ]

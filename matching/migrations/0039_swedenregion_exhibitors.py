# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-04 23:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0071_auto_20171030_2040'),
        ('matching', '0038_auto_20171102_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='swedenregion',
            name='exhibitors',
            field=models.ManyToManyField(to='exhibitors.Exhibitor'),
        ),
    ]
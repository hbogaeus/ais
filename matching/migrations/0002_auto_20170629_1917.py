# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-29 17:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]

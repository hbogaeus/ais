# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-06 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0021_auto_20170304_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='alternative_email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='cell_phone',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-28 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0004_remove_transportationorder_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportationorder',
            name='contact_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='transportationorder',
            name='contact_phone_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
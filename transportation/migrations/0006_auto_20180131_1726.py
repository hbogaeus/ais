# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-31 16:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0005_auto_20180128_1843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transportationorder',
            old_name='nuber_of_packages',
            new_name='number_of_packages',
        ),
        migrations.RenameField(
            model_name='transportationorder',
            old_name='nuber_of_pallets',
            new_name='number_of_pallets',
        ),
    ]
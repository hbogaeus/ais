# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-24 14:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_product_included_for_all'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'permissions': (('base', 'Products'),)},
        ),
    ]
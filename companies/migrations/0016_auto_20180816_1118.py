# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-16 09:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0015_auto_20180816_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='invoice_zipcode',
            new_name='invoice_zip_code',
        ),
    ]